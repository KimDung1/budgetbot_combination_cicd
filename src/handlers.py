"""Endpoint business logic for BudgetBot."""
import csv
import hashlib
import io
import logging
import time
from typing import Optional

from src.config import config
from src.adapters.safety import check_safety


logger = logging.getLogger(__name__)


def _parse_csv(data: bytes) -> list:
    """Expect CSV columns: date, description, amount. Header row optional."""
    text = data.decode("utf-8-sig", errors="replace")
    reader = csv.reader(io.StringIO(text))
    rows = list(reader)
    if not rows:
        return []
    # Detect header
    header = [c.lower().strip() for c in rows[0]]
    if "date" in header and "amount" in header:
        idx = {col: i for i, col in enumerate(header)}
        data_rows = rows[1:]
    else:
        idx = {"date": 0, "description": 1, "amount": 2}
        data_rows = rows
    parsed = []
    for r in data_rows:
        if len(r) < 3 or not r[idx.get("date", 0)].strip():
            continue
        try:
            parsed.append({
                "date": r[idx.get("date", 0)].strip(),
                "description": r[idx.get("description", 1)].strip(),
                "amount": float(r[idx.get("amount", 2)].strip().replace(",", "")),
            })
        except (ValueError, IndexError):
            continue
    return parsed


def handle_upload(
    user_id: str,
    filename: str,
    data: bytes,
    ai_client,
    storage,
    userstore,
) -> dict:
    """Parse CSV → categorize each row via AI → persist to userstore."""
    key = f"{user_id}/{filename}"
    location = storage.put(key, data)
    rows = _parse_csv(data)
    inserted = 0
    samples = []
    classify_rows = []
    safe_rows = []
    blocked_rows = []
    safety_blocked = 0
    for i, row in enumerate(rows):
        row_id = hashlib.sha1(
            f"{filename}|{i}|{row['date']}|{row['description']}|{row['amount']}".encode("utf-8")
        ).hexdigest()[:12]
        enriched = {"row_id": row_id, **row}
        # --- AI Safety Check ---
        safety = check_safety(row["description"])
        if not safety["safe"]:
            logger.warning(
                "safety_blocked user_id=%s description=%s threat=%s pattern=%s",
                user_id, row["description"][:50], safety["threat_type"], safety["pattern"],
            )
            blocked_rows.append(enriched)
            safety_blocked += 1
        else:
            safe_rows.append(enriched)
    classify_rows = safe_rows
    classify_started = time.perf_counter()
    if hasattr(ai_client, "categorize_many"):
        category_results = ai_client.categorize_many(classify_rows)
    else:
        category_results = [
            ai_client.categorize(description=row["description"], amount=row["amount"], date=row["date"])
            for row in classify_rows
        ]
    bedrock_latency_ms = (time.perf_counter() - classify_started) * 1000
    for row, cat_result in zip(classify_rows, category_results):
        logger.warning(
            "bedrock_classification_result user_id=%s category=%s confidence=%s",
            user_id,
            cat_result["category"],
            cat_result["confidence"],
        )
        txn = {
            "date": row["date"],
            "description": row["description"],
            "amount": row["amount"],
            "category": cat_result["category"],
            "confidence": cat_result["confidence"],
            "source_file": filename,
            "txn_id": row["row_id"],
        }
        userstore.add_transaction(user_id, txn)
        inserted += 1
        if len(samples) < 5:
            samples.append(txn)
    # Store blocked rows with safety flag
    for row in blocked_rows:
        txn = {
            "date": row["date"],
            "description": row["description"],
            "amount": row["amount"],
            "category": "Other",
            "confidence": "blocked",
            "source_file": filename,
            "txn_id": row["row_id"],
        }
        userstore.add_transaction(user_id, txn)
        inserted += 1
    low_confidence_count = sum(
        1 for result in category_results
        if result.get("confidence") == "low"
    )
    _put_upload_metrics(
        upload_succeeded=1,
        transactions_categorized=inserted,
        low_confidence_transactions=low_confidence_count,
        bedrock_latency_ms=bedrock_latency_ms,
    )
    return {
        "filename": filename,
        "stored_at": location,
        "rows_parsed": len(rows),
        "rows_inserted": inserted,
        "low_confidence_count": low_confidence_count,
        "safety_blocked": safety_blocked,
        "sample_categorized": samples,
    }


def handle_summary(user_id: str, month: Optional[str], userstore) -> dict:
    summary = userstore.summary(user_id, month=month)
    total = sum(v["total"] for v in summary.values())
    sorted_cats = sorted(summary.items(), key=lambda kv: -abs(kv[1]["total"]))
    return {
        "user_id": user_id,
        "month": month,
        "total_spend": total,
        "by_category": dict(sorted_cats),
        "top_3_drivers": [
            {"category": cat, "total": v["total"], "count": v["count"]}
            for cat, v in sorted_cats[:3]
        ],
    }


def handle_list_transactions(user_id: str, month: Optional[str], userstore) -> dict:
    return {"user_id": user_id, "month": month, "transactions": userstore.list_transactions(user_id, month=month)}


def handle_review_queue(user_id: str, month: Optional[str], userstore) -> dict:
    transactions = userstore.list_transactions(user_id, month=month)
    review_items = [
        txn for txn in transactions
        if str(txn.get("confidence", "")).lower() == "low"
    ]
    return {
        "user_id": user_id,
        "month": month,
        "count": len(review_items),
        "items": review_items,
    }


VALID_CATEGORIES = [
    "Food", "Transport", "Shopping", "Utilities", "Entertainment",
    "Health", "Subscriptions", "Income", "Transfer", "Other",
]


def handle_correct_transaction(user_id: str, sk: str, new_category: str, userstore) -> dict:
    """Let user correct a misclassified transaction."""
    if new_category not in VALID_CATEGORIES:
        return {"error": f"Invalid category. Must be one of: {', '.join(VALID_CATEGORIES)}"}
    if not hasattr(userstore, "correct_transaction"):
        return {"error": "Correction not supported by current userstore backend"}
    return userstore.correct_transaction(user_id, sk, new_category)


def handle_stats(user_id: str, userstore) -> dict:
    """Compute AI performance stats from live transaction data."""
    txns = userstore.list_transactions(user_id)
    if not txns:
        return {"total": 0}

    # Confidence distribution
    conf_dist = {"high": 0, "medium": 0, "low": 0, "human": 0}
    cat_dist: dict[str, int] = {}
    corrections = 0

    for t in txns:
        c = str(t.get("confidence", "")).lower()
        if c in conf_dist:
            conf_dist[c] += 1
        else:
            conf_dist["medium"] += 1
        cat = t.get("category", "Other")
        cat_dist[cat] = cat_dist.get(cat, 0) + 1
        if c == "human":
            corrections += 1

    total = len(txns)
    return {
        "total": total,
        "confidence": conf_dist,
        "confidence_pct": {k: round(v / total * 100, 1) for k, v in conf_dist.items()} if total else {},
        "by_category": dict(sorted(cat_dist.items(), key=lambda x: -x[1])),
        "corrections": corrections,
    }


def handle_accuracy(ai_client) -> dict:
    """Run test set through current AI backend and return precision/recall."""
    from src.test_data import TEST_TRANSACTIONS
    from collections import defaultdict

    results = []
    for row in TEST_TRANSACTIONS:
        pred = ai_client.categorize(
            description=row["description"],
            amount=row["amount"],
            date=row["date"],
        )
        results.append({
            "description": row["description"],
            "human": row["human_label"],
            "predicted": pred["category"],
            "confidence": pred["confidence"],
            "correct": pred["category"] == row["human_label"],
        })

    # Per-category metrics
    all_cats = sorted(set(r["human"] for r in results) | set(r["predicted"] for r in results))
    metrics = {}
    for cat in all_cats:
        tp = sum(1 for r in results if r["predicted"] == cat and r["human"] == cat)
        fp = sum(1 for r in results if r["predicted"] == cat and r["human"] != cat)
        fn = sum(1 for r in results if r["predicted"] != cat and r["human"] == cat)
        p = tp / (tp + fp) if (tp + fp) > 0 else 0
        r_ = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * p * r_ / (p + r_) if (p + r_) > 0 else 0
        metrics[cat] = {"tp": tp, "fp": fp, "fn": fn, "precision": round(p, 3), "recall": round(r_, 3), "f1": round(f1, 3)}

    total = len(results)
    correct = sum(1 for r in results if r["correct"])
    errors = [r for r in results if not r["correct"]]

    return {
        "backend": config.ai_backend,
        "total": total,
        "correct": correct,
        "accuracy": round(correct / total * 100, 1) if total else 0,
        "per_category": metrics,
        "errors": errors[:20],
    }


def _put_upload_metrics(
    upload_succeeded: int,
    transactions_categorized: int,
    low_confidence_transactions: int,
    bedrock_latency_ms: float,
) -> None:
    if not config.cloudwatch_namespace:
        return
    try:
        import boto3

        client = boto3.client("cloudwatch", region_name=config.aws_region)
        client.put_metric_data(
            Namespace=config.cloudwatch_namespace,
            MetricData=[
                {
                    "MetricName": "UploadSucceeded",
                    "Value": upload_succeeded,
                    "Unit": "Count",
                },
                {
                    "MetricName": "TransactionsCategorized",
                    "Value": transactions_categorized,
                    "Unit": "Count",
                },
                {
                    "MetricName": "LowConfidenceTransactions",
                    "Value": low_confidence_transactions,
                    "Unit": "Count",
                },
                {
                    "MetricName": "BedrockLatencyMs",
                    "Value": bedrock_latency_ms,
                    "Unit": "Milliseconds",
                },
            ],
        )
    except Exception:
        logger.exception("cloudwatch_put_metric_data_failed")
