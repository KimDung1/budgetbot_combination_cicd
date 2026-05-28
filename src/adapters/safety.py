"""AI Safety — Prompt Injection Guard for BudgetBot.

Checks transaction descriptions for dangerous patterns before sending to Bedrock.
Blocks SQL injection, command injection, template injection, and prompt manipulation.
"""
import re
import logging

logger = logging.getLogger(__name__)

# Dangerous patterns grouped by threat type
THREAT_PATTERNS = {
    "sql_injection": [
        "drop table", "delete from", "union select", "insert into",
        "update set", "alter table", "truncate table",
        "';--", "' or '1'='1", "or 1=1", "exec(",
    ],
    "command_injection": [
        "&&", "||", "; rm ", "; cat ", "$(", "`", "| grep",
        "/etc/passwd", "/bin/sh", "cmd.exe", "powershell",
    ],
    "template_injection": [
        "${", "{{", "}}", "<%", "%>", "#{",
    ],
    "prompt_injection": [
        "ignore previous instructions",
        "ignore all instructions",
        "reveal system prompt",
        "forget your instructions",
        "you are now",
        "act as",
        "disregard above",
        "override safety",
        "jailbreak",
    ],
}


def check_safety(text: str) -> dict:
    """Check if text contains dangerous patterns.

    Returns:
        dict with keys:
            safe (bool): True if text is safe
            threat_type (str|None): type of threat detected
            pattern (str|None): the pattern that matched
    """
    if not text or not isinstance(text, str):
        return {"safe": True, "threat_type": None, "pattern": None}

    text_lower = text.lower().strip()

    for threat_type, patterns in THREAT_PATTERNS.items():
        for pattern in patterns:
            if pattern.lower() in text_lower:
                logger.warning(
                    "safety_block threat_type=%s pattern=%s input=%s",
                    threat_type, pattern, text[:80],
                )
                return {
                    "safe": False,
                    "threat_type": threat_type,
                    "pattern": pattern,
                }

    return {"safe": True, "threat_type": None, "pattern": None}


def sanitize_for_logging(text: str, max_len: int = 100) -> str:
    """Truncate and strip control characters for safe logging."""
    cleaned = re.sub(r"[\x00-\x1f\x7f]", "", text)
    return cleaned[:max_len]
