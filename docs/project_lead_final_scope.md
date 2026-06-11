# Project Lead Final Scope

Owner: Project Lead

Má»¥c tiĂªu pháº§n nĂ y lĂ  chá»‘t láº¡i cĂ¢u chuyá»‡n demo cuá»‘i cĂ¹ng: cĂ¡i gĂ¬ Ä‘Ă£ cháº¡y tháº­t, cĂ¡i gĂ¬ khĂ´ng cáº§n Ä‘Æ°a vĂ o demo, vĂ  trainer sáº½ Ä‘i qua luá»“ng nĂ o Ä‘á»ƒ tháº¥y BudgetBot hoáº¡t Ä‘á»™ng end-to-end.

## 1. Nhá»¯ng GĂ¬ ÄĂ£ Cháº¡y

### Háº¡ táº§ng vĂ  safety

- AWS region Ä‘Ă£ dĂ¹ng: `ap-southeast-1`.
- CloudFormation stack Ä‘Ă£ deploy: `team14-budgetbot-iac`.
- Budget alert Ä‘Ă£ táº¡o: `W7-Team14-HardCap-100USD`, cáº£nh bĂ¡o khi actual cost vÆ°á»£t `$80`.
- SNS email alert Ä‘Ă£ confirm: `your-email@example.com`.
- Cost Anomaly Detection Ä‘Ă£ báº­t vĂ  Ä‘Ă£ thĂªm subscriber.
- Tagging convention Ä‘Ă£ thá»‘ng nháº¥t:
  - `Project=W7Capstone`
  - `Team=G14`
  - `Owner=<member-name>`
  - `Environment=hackathon`

### Foundation resources

- S3 frontend bucket Ä‘Ă£ táº¡o, báº­t Block Public Access vĂ  encryption.
- S3 raw statements bucket Ä‘Ă£ táº¡o, báº­t Block Public Access vĂ  encryption.
- ÄĂ£ xĂ³a 2 bucket S3 cÅ© bá»‹ trĂ¹ng chá»©c nÄƒng:
  - `team14-budgetbot-frontend-123456789012`
  - `team14-budgetbot-raw-123456789012`
- S3 buckets cĂ²n dĂ¹ng cho demo:
  - `team14-budgetbot-cfn-frontend-123456789012-ap-southeast-1` cho static frontend.
  - `team14-budgetbot-cfn-raw-123456789012-ap-southeast-1` cho raw statement uploads vĂ  Lambda artifacts Ä‘Ă£ deploy thá»§ cĂ´ng.
  - `team14-budgetbot-artifacts-123456789012-ap-southeast-1` cho GitHub Actions Lambda artifacts náº¿u dĂ¹ng CI/CD.
- DynamoDB table Ä‘Ă£ táº¡o: `team14-budgetbot-cfn-transactions`.
- Lambda execution role Ä‘Ă£ táº¡o theo hÆ°á»›ng least privilege.
- VPC Ä‘Ă£ táº¡o vá»›i private Lambda subnets across two AZs.
- VPC endpoints Ä‘Ă£ táº¡o cho S3, DynamoDB, Bedrock Runtime, vĂ  CloudWatch Monitoring.
- CloudFront distribution Ä‘Ă£ táº¡o Ä‘á»ƒ serve frontend báº±ng HTTPS.
- API Gateway HTTP API Ä‘Ă£ táº¡o Ä‘á»ƒ expose backend endpoints.

### Core application

- Lambda backend Ä‘Ă£ deploy: `team14-budgetbot-cfn-backend`.
- API routes Ä‘Ă£ cháº¡y:
  - `GET /health`
  - `POST /upload`
  - `GET /transactions`
  - `GET /summary`
  - `GET /review-queue`
- Frontend Ä‘Ă£ cáº¥u hĂ¬nh gá»i API tháº­t.
- Upload CSV tháº­t Ä‘Ă£ cháº¡y Ä‘Æ°á»£c vá»›i S3 raw storage.
- Bedrock InvokeModel Ä‘Ă£ cháº¡y tháº­t báº±ng Amazon Nova Micro.
- DynamoDB write/read Ä‘Ă£ cháº¡y tháº­t.
- Duplicate upload Ä‘Ă£ xá»­ lĂ½: upload cĂ¹ng má»™t file khĂ´ng nhĂ¢n báº£n transaction.
- Low-confidence review queue Ä‘Ă£ cháº¡y qua API Gateway vĂ  hiá»ƒn thá»‹ trĂªn frontend.
- File `bank_statement_q2_2026.csv` Ä‘Ă£ test thĂ nh cĂ´ng vá»›i `83` transaction.
- Data Owner proof Ä‘Ă£ cháº¡y vá»›i `user_id=data-owner-1779934940`: upload lÆ°u 83 categorized transactions, query `month=2026-03` tráº£ 30 transactions, DynamoDB query cĂ¹ng key condition cÅ©ng tráº£ count 30, vĂ  summary tráº£ category breakdown.
- CloudWatch logs Ä‘Ă£ cĂ³ evidence tá»« Lambda vĂ  Bedrock classification path.
- Observability Owner proof Ä‘Ă£ cháº¡y vá»›i `user_id=observability-1779935557`: custom metrics cĂ³ datapoints `UploadSucceeded=1`, `TransactionsCategorized=83`, `LowConfidenceTransactions=7`, `BedrockLatencyMsâ‰ˆ6102`; dashboard `team14-budgetbot-cfn-observability` tá»“n táº¡i; alarm `team14-budgetbot-cfn-low-confidence-transactions` á»Ÿ tráº¡ng thĂ¡i `OK`; saved Logs Insights query `team14-budgetbot-cfn/upload-classification-path` cháº¡y ra 5 rows.

### Public endpoints

- Frontend URL: `https://xxxxxxxxxxxx.cloudfront.net`
- API endpoint: `https://xxxxxxxxxx.execute-api.ap-southeast-1.amazonaws.com`

## 2. Cáº¯t Nhá»¯ng Pháº§n KhĂ´ng Cáº§n Thiáº¿t

Nhá»¯ng pháº§n dÆ°á»›i Ä‘Ă¢y khĂ´ng Ä‘Æ°a vĂ o demo chĂ­nh Ä‘á»ƒ giá»¯ demo gá»n, giáº£m rá»§i ro, vĂ  táº­p trung vĂ o 7 mandatory capabilities cá»™ng optional Full Observability.

### Cáº¯t khá»i scope build/demo

- KhĂ´ng lĂ m banking integration tháº­t.
- KhĂ´ng dĂ¹ng dá»¯ liá»‡u tĂ i chĂ­nh tháº­t cá»§a ngÆ°á»i dĂ¹ng.
- KhĂ´ng lĂ m Cognito signup/login.
- KhĂ´ng lĂ m multi-user auth flow phá»©c táº¡p.
- KhĂ´ng lĂ m Bedrock Knowledge Base hoáº·c RAG.
- KhĂ´ng lĂ m vector database.
- KhĂ´ng lĂ m RDS/Postgres migration.
- KhĂ´ng lĂ m mobile app.
- KhĂ´ng lĂ m custom domain.
- KhĂ´ng lĂ m multi-region failover.
- KhĂ´ng lĂ m NAT Gateway vĂ¬ private subnets dĂ¹ng VPC endpoints.
- KhĂ´ng demo full CI/CD náº¿u khĂ´ng cáº§n; GitHub Actions chá»‰ lĂ  bonus/supporting evidence.
- KhĂ´ng dĂ¹ng láº¡i S3 buckets thá»§ cĂ´ng cÅ©. App demo chá»‰ dĂ¹ng bucket Ä‘Æ°á»£c quáº£n lĂ½ bá»Ÿi CloudFormation.

### KhĂ´ng nháº¥n máº¡nh trong presentation

- KhĂ´ng giáº£i thĂ­ch quĂ¡ sĂ¢u pháº§n subnet route table náº¿u trainer khĂ´ng há»i.
- KhĂ´ng nĂ³i app lĂ  production banking app.
- KhĂ´ng claim cĂ³ authentication hoáº·c data privacy chuáº©n ngĂ¢n hĂ ng.
- KhĂ´ng claim DynamoDB náº±m trong VPC. DynamoDB lĂ  AWS managed regional service, Lambda truy cáº­p riĂªng qua Gateway Endpoint.
- KhĂ´ng claim Bedrock náº±m trong VPC. Bedrock Runtime lĂ  AWS managed service, Lambda truy cáº­p qua Interface Endpoint.
- KhĂ´ng claim Claude Haiku Ä‘ang cháº¡y náº¿u account chÆ°a Ä‘Æ°á»£c approve. Demo hiá»‡n dĂ¹ng Amazon Nova Micro qua Bedrock Runtime.

## 3. Demo Path Cuá»‘i CĂ¹ng

ÄĂ¢y lĂ  luá»“ng demo chĂ­nh, nĂªn Ä‘i Ä‘Ăºng thá»© tá»± Ä‘á»ƒ Ă­t lá»—i vĂ  dá»… ghi Ä‘iá»ƒm.

### Path 1: User-facing demo

1. Má»Ÿ frontend public HTTPS URL:

   ```text
   https://xxxxxxxxxxxx.cloudfront.net
   ```

2. Upload file CSV máº«u:

   ```text
   sample_data/bank_statement_q2_2026.csv
   ```

3. XĂ¡c nháº­n UI hiá»ƒn thá»‹ upload success.

4. XĂ¡c nháº­n transaction list cĂ³ dá»¯ liá»‡u Ä‘Ă£ phĂ¢n loáº¡i category.

5. XĂ¡c nháº­n summary theo category hiá»ƒn thá»‹ Ä‘Æ°á»£c.

6. Má»Ÿ Review queue Ä‘á»ƒ chá»©ng minh low-confidence classifications cĂ³ hĂ ng chá» review.

7. Refresh browser vĂ  má»Ÿ láº¡i transaction/summary Ä‘á»ƒ chá»©ng minh dá»¯ liá»‡u Ä‘Æ°á»£c lÆ°u trong DynamoDB, khĂ´ng chá»‰ náº±m trong memory.

### Path 2: Backend/API proof

1. Gá»i health check:

   ```bash
   curl https://xxxxxxxxxx.execute-api.ap-southeast-1.amazonaws.com/health
   ```

2. Káº¿t quáº£ mong Ä‘á»£i:

   ```json
   {
     "status": "ok",
     "backends": {
       "ai": "bedrock",
       "storage": "s3",
       "userstore": "dynamodb"
     }
   }
   ```

3. Náº¿u cáº§n chá»©ng minh duplicate fix, upload cĂ¹ng file hai láº§n vá»›i cĂ¹ng `X-User-Id`, sau Ä‘Ă³ gá»i `/transactions`. Káº¿t quáº£ Ä‘Ăºng lĂ  váº«n `83` transaction, khĂ´ng tÄƒng lĂªn `166`.

4. Náº¿u cáº§n chá»©ng minh review queue:

   ```bash
   curl -H "X-User-Id: <demo-user>" https://xxxxxxxxxx.execute-api.ap-southeast-1.amazonaws.com/review-queue
   ```

### Path 3: AWS evidence proof

1. Má»Ÿ CloudFormation stack `team14-budgetbot-iac`.
2. Show tab Resources Ä‘á»ƒ tháº¥y S3, DynamoDB, Lambda, API Gateway, CloudFront, VPC endpoints.
3. Show tab Outputs Ä‘á»ƒ láº¥y Frontend URL vĂ  API endpoint.
4. Má»Ÿ DynamoDB table `team14-budgetbot-cfn-transactions` Ä‘á»ƒ chá»©ng minh transaction Ä‘Ă£ persist.
5. Má»Ÿ S3 raw bucket `team14-budgetbot-cfn-raw-123456789012-ap-southeast-1` Ä‘á»ƒ chá»©ng minh CSV gá»‘c Ä‘Ă£ Ä‘Æ°á»£c lÆ°u.
6. Má»Ÿ CloudWatch Logs cá»§a Lambda Ä‘á»ƒ chá»©ng minh Bedrock classification path cháº¡y tháº­t.
7. Má»Ÿ CloudWatch dashboard/alarm Ä‘á»ƒ chá»©ng minh optional capability Full Observability.
8. Má»Ÿ Budget/SNS/Cost Anomaly Detection screenshot hoáº·c console náº¿u trainer há»i vá» cost safety.
9. Náº¿u trainer há»i vĂ¬ sao cĂ²n nhiá»u S3 buckets, tráº£ lá»i: app chĂ­nh dĂ¹ng 2 bucket `team14-budgetbot-cfn-*`; bucket `team14-budgetbot-artifacts-*` phá»¥c vá»¥ CI/CD artifact; bucket `cf-templates-*` do CloudFormation Console tá»± táº¡o khi upload template.

## 4. Final Scope Statement

BudgetBot lĂ  má»™t serverless AI Money Coach cho FinTech. NgÆ°á»i dĂ¹ng upload bank statement CSV qua CloudFront frontend, frontend gá»i API Gateway, Lambda parse giao dá»‹ch, lÆ°u CSV gá»‘c vĂ o S3, gá»i Amazon Bedrock Runtime Ä‘á»ƒ phĂ¢n loáº¡i giao dá»‹ch, ghi káº¿t quáº£ vĂ o DynamoDB, vĂ  frontend Ä‘á»c láº¡i transactions/summary. Há»‡ thá»‘ng Ä‘Æ°á»£c deploy báº±ng CloudFormation, cháº¡y trong private Lambda subnets vá»›i VPC endpoints, dĂ¹ng IAM least privilege, vĂ  cĂ³ CloudWatch observability lĂ m optional capability.

## 5. Presenter Checklist

- [ ] Public URL má»Ÿ Ä‘Æ°á»£c.
- [ ] `/health` tráº£ `status=ok`.
- [ ] Upload CSV thĂ nh cĂ´ng.
- [ ] Transactions hiá»ƒn thá»‹ Ä‘Ăºng category.
- [ ] Summary hiá»ƒn thá»‹ Ä‘Æ°á»£c.
- [ ] Review queue load Ä‘Æ°á»£c qua UI hoáº·c `/review-queue`.
- [ ] Upload láº¡i cĂ¹ng file khĂ´ng táº¡o duplicate.
- [ ] CloudWatch logs cĂ³ Bedrock classification evidence.
- [ ] DynamoDB cĂ³ transaction records.
- [ ] S3 raw bucket cĂ³ uploaded CSV.
- [ ] S3 duplicate buckets cÅ© Ä‘Ă£ Ä‘Æ°á»£c xĂ³a, chá»‰ cĂ²n bucket CloudFormation/artifact/template cáº§n thiáº¿t.
- [ ] CloudFormation outputs cĂ³ Frontend URL vĂ  API endpoint.
- [ ] Budget alert, SNS confirmation, Cost Anomaly Detection cĂ³ screenshot/evidence.

