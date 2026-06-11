# W7 Evidence Pack â€” Team 14 BudgetBot â€” Báº£n Tiáº¿ng Viá»‡t

## 1. Trang BĂ¬a

| Má»¥c | GiĂ¡ trá»‹ |
|---|---|
| NhĂ³m | Team 14 / G14 |
| Domain | FinTech â€” AI Money Coach / BudgetBot |
| Live public URL | https://your-domain.example.com |
| CloudFront URL | https://xxxxxxxxxxxx.cloudfront.net |
| API endpoint | https://xxxxxxxxxx.execute-api.ap-southeast-1.amazonaws.com |
| GitHub repo | https://github.com/your-github-username/team14-repo |
| AWS account | 123456789012 |
| AWS region | ap-southeast-1 |
| CloudFormation stack | team14-budgetbot-iac |
| Tá»•ng chi phĂ­ | TODO: Ä‘iá»n tá»« Cost Explorer screenshot sĂ¡ng demo |
| Hard cap | $100/nhĂ³m |
| Budget alert | W7-Team14-HardCap-100USD, monthly cost budget $100 |
| Email SNS Ä‘Ă£ confirm | your-email@example.com |

### Artifact Báº¯t Buá»™c

| Artifact | Tráº¡ng thĂ¡i | Báº±ng chá»©ng |
|---|---:|---|
| Live HTTPS URL | Xong | `https://your-domain.example.com` tráº£ HTTP 200 qua CloudFront |
| GitHub repo | Xong | `https://github.com/your-github-username/team14-repo` |
| SÆ¡ Ä‘á»“ kiáº¿n trĂºc cuá»‘i | Xong | `docs/architecture.png` |
| Evidence Pack | Xong | `docs/W7_evidence.md` vĂ  `docs/W7_evidence.vi.md` |
| Video demo | TODO | ThĂªm `docs/demo.mp4` hoáº·c link YouTube unlisted |
| Slides PDF | TODO | ThĂªm `docs/slides.pdf` |
| Teardown confirmation | ÄĂ£ lĂªn káº¿ hoáº¡ch | `docs/teardown_confirmation.md` sau háº¡n Sun 1/6 EOD |

## 2. Pitch VĂ  Táº§m NhĂ¬n

BudgetBot lĂ  má»™t AI Money Coach giĂºp ngÆ°á»i dĂ¹ng hiá»ƒu nhanh tiá»n cá»§a mĂ¬nh Ä‘Ă£ Ä‘i Ä‘Ă¢u. NgÆ°á»i dĂ¹ng upload sao kĂª ngĂ¢n hĂ ng dáº¡ng CSV; BudgetBot lÆ°u file gá»‘c, phĂ¢n loáº¡i tá»«ng giao dá»‹ch báº±ng Amazon Bedrock, lÆ°u káº¿t quáº£ vĂ o DynamoDB, hiá»ƒn thá»‹ summary theo category vĂ  Ä‘Æ°a cĂ¡c giao dá»‹ch low-confidence vĂ o review queue.

NgÆ°á»i dĂ¹ng má»¥c tiĂªu lĂ  sinh viĂªn, ngÆ°á»i má»›i Ä‘i lĂ m, freelancer vĂ  chá»§ doanh nghiá»‡p nhá» cáº§n nhĂ¬n nhanh tĂ¬nh hĂ¬nh chi tiĂªu mĂ  khĂ´ng muá»‘n tá»± gáº¯n nhĂ£n tá»«ng dĂ²ng giao dá»‹ch. Sáº£n pháº©m tÆ°Æ¡ng tá»± ngoĂ i Ä‘á»i gá»“m Money Lover, YNAB, Spendee, Monzo/Revolut spending insights vĂ  Cake by VPBank. Domain nĂ y quan trá»ng vĂ¬ dá»¯ liá»‡u tĂ i chĂ­nh thá»±c táº¿ ráº¥t báº©n: mĂ´ táº£ giao dá»‹ch ngáº¯n, tĂªn merchant khĂ´ng thá»‘ng nháº¥t, nhiá»u dĂ²ng mÆ¡ há»“ hoáº·c khĂ´ng Ä‘á»§ thĂ´ng tin. VĂ¬ váº­y AI chá»‰ há»¯u Ă­ch khi há»‡ thá»‘ng cĂ³ confidence score vĂ  cho phĂ©p ngÆ°á»i dĂ¹ng sá»­a káº¿t quáº£ khĂ´ng cháº¯c cháº¯n.

### Demo Flow

1. Trainer má»Ÿ `https://your-domain.example.com`.
2. Upload `sample_data/bank_statement_q2_2026.csv`.
3. Lambda lÆ°u raw CSV vĂ o S3.
4. Lambda gá»­i mĂ´ táº£ giao dá»‹ch sang Amazon Bedrock InvokeModel.
5. Bedrock tráº£ JSON-only gá»“m `category` vĂ  `confidence`.
6. Lambda lÆ°u categorized transactions vĂ o DynamoDB.
7. UI refresh summary, transaction list, AI performance, failure cases vĂ  review queue.
8. Sau khi refresh browser, dá»¯ liá»‡u váº«n cĂ²n vĂ¬ state Ä‘Æ°á»£c lÆ°u trong DynamoDB.

## 3. Kiáº¿n TrĂºc

![Team 14 BudgetBot AWS Architecture](architecture.png)

### TĂ³m Táº¯t Kiáº¿n TrĂºc

Luá»“ng runtime:

`Users -> Route 53 -> CloudFront HTTPS -> private S3 frontend -> API Gateway HTTP API -> Lambda FastAPI -> S3 raw bucket / Bedrock Runtime / DynamoDB / CloudWatch`

Luá»“ng deployment:

`Developer push -> GitHub Actions -> pytest -> build Lambda zip -> S3 artifact bucket -> CloudFormation deploy -> S3 frontend sync -> CloudFront invalidation`

### 7 Mandatory Capabilities

| # | Capability | Service Ä‘Ă£ triá»ƒn khai | Báº±ng chá»©ng / Resource | LĂ½ do chá»n |
|---:|---|---|---|---|
| 1 | User-Facing Entry | Route 53 + CloudFront + S3 static frontend + API Gateway HTTP API | `your-domain.example.com`, CloudFront `XXXXXXXXXXXX`, API `xxxxxxxxxx` | CloudFront cung cáº¥p HTTPS public vĂ  truy cáº­p S3 private qua OAC. API Gateway HTTP API ráº» vĂ  Ä‘Æ¡n giáº£n hÆ¡n REST API cho Lambda proxy. |
| 2 | Application Compute | AWS Lambda cháº¡y FastAPI qua Mangum | `team14-budgetbot-cfn-backend`, Python 3.12, 512 MB, timeout 30s | Upload CSV vĂ  classify lĂ  request-driven workload. Lambda khĂ´ng cĂ³ idle server cost vĂ  deploy nhanh trong hackathon 48 giá». |
| 3 | AI / ML Feature | Amazon Bedrock Runtime InvokeModel | `AI_MODEL_ID=apac.amazon.nova-micro-v1:0` | BudgetBot cáº§n classify tá»«ng transaction, khĂ´ng cáº§n RAG. InvokeModel Ä‘Æ¡n giáº£n vĂ  tiáº¿t kiá»‡m hÆ¡n Knowledge Base. |
| 4 | Data Persistence | DynamoDB | `team14-budgetbot-cfn-transactions`, PK `user_id`, SK `sk`, PAY_PER_REQUEST, PITR enabled | Access pattern lĂ  query theo user/month vĂ  summary category. DynamoDB giáº£m váº­n hĂ nh vĂ  trĂ¡nh chi phĂ­ RDS instance/proxy. |
| 5 | Object Storage | Amazon S3 | raw bucket `team14-budgetbot-cfn-raw-123456789012-ap-southeast-1`, frontend bucket `team14-budgetbot-cfn-frontend-123456789012-ap-southeast-1`, artifact bucket `team14-budgetbot-artifacts-123456789012-ap-southeast-1` | S3 phĂ¹ há»£p Ä‘á»ƒ lÆ°u raw CSV, static frontend vĂ  Lambda artifact. |
| 6 | Network Foundation | VPC, private subnets 2 AZ, security groups, VPC endpoints, khĂ´ng dĂ¹ng NAT Gateway | VPC `vpc-044f26a2a760491ba`; private subnets `subnet-0acedaa53e5480c96`, `subnet-0f404f193e6534efd`; endpoints cho S3, DynamoDB, Bedrock Runtime, CloudWatch Monitoring | Lambda khĂ´ng cĂ³ public IP. Private subnets gá»i AWS services qua endpoint Ä‘á»ƒ giáº£m chi phĂ­ vĂ  giá»¯ traffic private. |
| 7 | Identity & Access | IAM least-privilege Lambda execution role | `arn:aws:iam::123456789012:role/team14-budgetbot-cfn-lambda-role` | Rule yĂªu cáº§u IAM least privilege. User login lĂ  optional, nĂªn app dĂ¹ng demo `X-User-Id` thay vĂ¬ tá»‘n thá»i gian triá»ƒn khai Cognito Ä‘áº§y Ä‘á»§. |

### Optional Capability ÄĂ£ Chá»n

Team 14 chá»n **Optional #8 â€” Full Observability**.

| YĂªu cáº§u | Triá»ƒn khai | Tráº¡ng thĂ¡i |
|---|---|---:|
| CloudWatch dashboard | `team14-budgetbot-cfn-observability` | Xong |
| Custom metric qua `PutMetricData` | `UploadSucceeded`, `TransactionsCategorized`, `LowConfidenceTransactions`, `BedrockLatencyMs` trong namespace `BudgetBot/Team14` | Xong |
| Alarm á»Ÿ OK/ALARM | `team14-budgetbot-cfn-low-confidence-transactions`, state `OK`, `TreatMissingData=notBreaching` | Xong |
| Saved Logs Insights query | `team14-budgetbot-cfn/upload-classification-path`, id `81030937-11c7-4d22-900e-b13f51a6c9d8` | Xong |

### Bonus Paths ÄĂ£ LĂ m

| Bonus Path | Báº±ng chá»©ng |
|---|---|
| B. CI/CD pipeline | `.github/workflows/build-and-deploy.yml`; latest runs trĂªn `main` Ä‘Ă£ success |
| C. Custom domain + HTTPS | Route 53 `your-domain.example.com`, ACM certificate á»Ÿ `us-east-1`, CloudFront alias |
| E. IaC full coverage | `infrastructure/cloudformation.yaml` táº¡o VPC, endpoints, S3, CloudFront, DynamoDB, IAM, Lambda, API Gateway, CloudWatch dashboard/alarm/query |
| H. Cost under $30 | Chá» Cost Explorer screenshot cuá»‘i vĂ  teardown sáº¡ch |

### Quyáº¿t Äá»‹nh Service ChĂ­nh

| Quyáº¿t Ä‘á»‹nh | Lá»±a chá»n | PhÆ°Æ¡ng Ă¡n cĂ¢n nháº¯c | LĂ½ do |
|---|---|---|---|
| Compute | Lambda | ECS/Fargate hoáº·c EC2 | Lambda há»£p vá»›i request upload/API, khĂ´ng cĂ³ idle cost. ECS/EC2 thĂªm váº­n hĂ nh server/container khĂ´ng cáº§n thiáº¿t cho demo. |
| API entry | API Gateway HTTP API | REST API hoáº·c ALB | HTTP API Ä‘á»§ cho Lambda proxy routes vĂ  ráº» hÆ¡n REST API. ALB phĂ¹ há»£p hÆ¡n cho service cháº¡y lĂ¢u. |
| Frontend | S3 + CloudFront | Amplify hoáº·c backend-served frontend | HTML/JS static Ä‘á»§ cho demo. CloudFront giáº£i quyáº¿t HTTPS vĂ  caching. |
| AI path | Bedrock InvokeModel | Bedrock KB/Agent | BudgetBot classify transaction rows, khĂ´ng retrieve knowledge tá»« tĂ i liá»‡u upload. |
| Model | Amazon Nova Micro | Model lá»›n hÆ¡n nhÆ° Claude/Sonnet | Nova Micro ráº» hÆ¡n vĂ  Ä‘á»§ cho category classification khi cĂ³ JSON-only prompt + review queue fallback. |
| Database | DynamoDB | RDS PostgreSQL | DynamoDB trĂ¡nh chi phĂ­ instance vĂ  Ä‘Ă¡p á»©ng access pattern user/month. Aggregation trong app cháº¥p nháº­n Ä‘Æ°á»£c á»Ÿ quy mĂ´ hackathon. |
| Network | KhĂ´ng NAT, dĂ¹ng VPC endpoints | NAT Gateway | S3/DynamoDB gateway endpoints miá»…n phĂ­; Bedrock/CloudWatch interface endpoints ráº» hÆ¡n NAT cho traffic AWS-only. |
| Identity | IAM least privilege + demo user header | Full Cognito flow | Rule yĂªu cáº§u IAM least privilege; Cognito optional. Bá» Cognito giĂºp giá»¯ scope Ä‘Ăºng 48 giá». |
| Observability | CloudWatch dashboard/metrics/alarm/query | Monitoring ngoĂ i AWS | CloudWatch native, Ä‘Ă£ há»c W1-W6, Ä‘Ă¡p á»©ng trá»±c tiáº¿p Optional #8. |

## 4. Ká»· Luáº­t Chi PhĂ­

### Safety Báº¯t Buá»™c

| YĂªu cáº§u | Tráº¡ng thĂ¡i | Báº±ng chá»©ng |
|---|---:|---|
| AWS Budget alert | Xong | `W7-Team14-HardCap-100USD`, monthly COST budget $100 |
| SNS email confirmed | Xong | `your-email@example.com`, subscription ARN Ä‘Ă£ confirm |
| Cost Anomaly Detection | Xong | Monitor `Default-Services-Monitor`; gáº¯n `docs/evidence_screenshots/cost/03_cost_anomaly_detection.png` |
| Tagging convention | Xong | `Project=W7Capstone`, `Team=G14`, `Owner=Team14`, `Environment=hackathon` trong CloudFormation resources |
| Bedrock access | Xong | Lambda health tráº£ `ai=bedrock`; InvokeModel cháº¡y qua app Ä‘Ă£ deploy |
| Cost Explorer screenshots | TODO | Day 1 EOD, Day 2 EOD, Friday pre-demo |

### Screenshot Cáº§n Gáº¯n VĂ o Evidence

| Screenshot | File cáº§n thĂªm | Ghi chĂº |
|---|---|---|
| Day 1 EOD Cost Explorer | `docs/evidence_screenshots/cost/04_cost_explorer_day1_eod.png` | Group by Service, filter theo Team/G14 náº¿u cost allocation tag Ä‘Ă£ active |
| Day 2 EOD Cost Explorer | `docs/evidence_screenshots/cost/05_cost_explorer_day2_eod.png` | CĂ³ tá»•ng chi phĂ­ |
| Friday pre-demo Cost Explorer | `docs/evidence_screenshots/cost/06_cost_explorer_friday_predemo.png` | Sá»‘ chĂ­nh thá»©c trÆ°á»›c demo |
| Budget alert | `docs/evidence_screenshots/cost/01_budget_alert.png` | Show budget $100 / threshold $80 |
| SNS confirmation | `docs/evidence_screenshots/cost/02_sns_confirmed.png` | Show email subscription confirmed |
| Cost Anomaly Detection | `docs/evidence_screenshots/cost/03_cost_anomaly_detection.png` | Show monitor/subscription active |

### Cost Drivers Dá»± Kiáº¿n

| Driver | VĂ¬ sao phĂ¡t sinh | CĂ¡ch kiá»ƒm soĂ¡t |
|---|---|---|
| Bedrock Runtime | AI classification khi upload vĂ  cháº¡y accuracy test | DĂ¹ng Nova Micro, batch classification, prompt ngáº¯n JSON-only, trĂ¡nh loop model Ä‘áº¯t |
| CloudFront + S3 | Public frontend, raw CSV, Lambda artifacts | Static site vĂ  file volume tháº¥p |
| VPC Interface Endpoints | Lambda private gá»i Bedrock Runtime vĂ  CloudWatch Monitoring | TrĂ¡nh NAT Gateway; S3/DynamoDB dĂ¹ng gateway endpoints miá»…n phĂ­ |
| DynamoDB | LÆ°u transaction state | PAY_PER_REQUEST, item count nhá», khĂ´ng provision capacity |
| Lambda + API Gateway | Backend compute vĂ  API entry | Serverless, khĂ´ng cĂ³ idle EC2/RDS cost |

### Ghi Nháº­n Cost

Khi soáº¡n evidence, AWS Cost Explorer tráº£ `DataUnavailableException`, thÆ°á»ng xáº£y ra khi Cost Explorer má»›i báº­t hoáº·c dá»¯ liá»‡u ngĂ y chÆ°a ingest xong. TrÆ°á»›c khi ná»™p, cáº§n thay ghi chĂº nĂ y báº±ng tá»•ng chi phĂ­ sĂ¡ng demo vĂ  top 3 cost drivers tá»« Cost Explorer.

## 5. Báº£o Máº­t

### Security Controls ÄĂ£ Triá»ƒn Khai

| Máº£ng | Triá»ƒn khai | Báº±ng chá»©ng |
|---|---|---|
| Root account safety | Root MFA lĂ  pre-flight requirement | Gáº¯n `docs/evidence_screenshots/security/01_root_mfa_enabled.png` tá»« account owner |
| HTTPS public entry | Route 53 + CloudFront + ACM certificate | `your-domain.example.com`; ACM cert `arn:aws:acm:us-east-1:123456789012:certificate/5aece9cc-fd4b-4ebc-a6a5-24ab429455de`; CloudFront TLS minimum `TLSv1.2_2021` |
| Frontend bucket private | S3 Block Public Access + CloudFront OAC | `team14-budgetbot-cfn-frontend-123456789012-ap-southeast-1`, OAC `E3U013UCJVZJJW` |
| Raw statement storage | S3 Block Public Access + SSE-S3 | `team14-budgetbot-cfn-raw-123456789012-ap-southeast-1`, AES256 encryption |
| Data encryption | DynamoDB SSE enabled + PITR enabled | `team14-budgetbot-cfn-transactions`, `SSE=ENABLED`, continuous backups `ENABLED` |
| Network isolation | Lambda trong private subnets, khĂ´ng public IP, private route table khĂ´ng cĂ³ internet default route | private subnets `subnet-0acedaa53e5480c96`, `subnet-0f404f193e6534efd`; khĂ´ng NAT Gateway |
| Least privilege | Lambda role chá»‰ cĂ³ action cáº§n thiáº¿t | `BudgetBotLambdaLeastPrivilegePolicy` |
| Cost safety | Budget + SNS + Cost Anomaly Detection | Budget `W7-Team14-HardCap-100USD`; SNS confirmed |

### IAM Scope Cá»§a Lambda

Lambda execution role chá»‰ cho phĂ©p cĂ¡c action cáº§n cho demo path:

- S3 raw bucket: `s3:PutObject`, `s3:GetObject`, `s3:ListBucket`
- DynamoDB transactions table: `dynamodb:PutItem`, `dynamodb:GetItem`, `dynamodb:Query`, `dynamodb:UpdateItem`
- Bedrock: `bedrock:InvokeModel` trĂªn Nova Micro inference profile/foundation model Ä‘Ă£ chá»n vĂ  má»™t fallback model ARN Ä‘Æ°á»£c liá»‡t kĂª rĂµ
- CloudWatch Logs: `logs:CreateLogGroup`, `logs:CreateLogStream`, `logs:PutLogEvents`
- CloudWatch custom metrics: `cloudwatch:PutMetricData` chá»‰ cho namespace `BudgetBot/Team14`
- Lambda VPC attachment: EC2 network-interface actions cáº§n cho Lambda ENI

Trade-off: má»™t sá»‘ quyá»n nhÆ° CloudWatch metrics vĂ  Lambda ENI váº«n cáº§n `Resource: "*"`, vĂ¬ AWS API Ä‘Ă³ khĂ´ng há»— trá»£ resource-level scoping giá»‘ng S3/DynamoDB. Äiá»u kiá»‡n namespace giá»›i háº¡n pháº§n CloudWatch metric.

## 6. Monitoring

Team 14 triá»ƒn khai **Full Observability**.

### CloudWatch Dashboard

| Má»¥c | GiĂ¡ trá»‹ |
|---|---|
| Dashboard name | `team14-budgetbot-cfn-observability` |
| Dashboard ARN | `arn:aws:cloudwatch::123456789012:dashboard/team14-budgetbot-cfn-observability` |
| Region | ap-southeast-1 |
| Widgets | BudgetBot demo path metrics |

### Custom Metrics

| Metric | Namespace | Unit | Ă nghÄ©a |
|---|---|---|---|
| `UploadSucceeded` | `BudgetBot/Team14` | Count | Má»™t upload CSV hoĂ n táº¥t thĂ nh cĂ´ng |
| `TransactionsCategorized` | `BudgetBot/Team14` | Count | Sá»‘ transaction Ä‘Ă£ classify vĂ  persist |
| `LowConfidenceTransactions` | `BudgetBot/Team14` | Count | Sá»‘ classification low-confidence Ä‘Æ°á»£c Ä‘Æ°a vĂ o review |
| `BedrockLatencyMs` | `BudgetBot/Team14` | Milliseconds | Latency classify cho batch upload |

### Alarm

| Má»¥c | GiĂ¡ trá»‹ |
|---|---|
| Alarm name | `team14-budgetbot-cfn-low-confidence-transactions` |
| State khi validate | `OK` |
| Metric | `LowConfidenceTransactions` |
| Threshold | `>= 1` trong 300 giĂ¢y |
| Treat missing data | `notBreaching` |
| VĂ¬ sao quan trá»ng | BĂ¡o rá»§i ro cháº¥t lÆ°á»£ng classification khi upload cĂ³ transaction low-confidence. |

### Logs Insights Query

Saved query:

```sql
fields @timestamp, @message
| filter @message like /bedrock_classification_result|cloudwatch_put_metric_data_failed|upload|summary|review/
| sort @timestamp desc
| limit 50
```

Báº±ng chá»©ng:

- Query definition name: `team14-budgetbot-cfn/upload-classification-path`
- Query definition id: `81030937-11c7-4d22-900e-b13f51a6c9d8`
- Log group: `/aws/lambda/team14-budgetbot-cfn-backend`

## 6.5 Äo LÆ°á»ng VĂ  Quyáº¿t Äá»‹nh

### DECISION 1 â€” Chá»n DynamoDB Thay VĂ¬ RDS PostgreSQL

**QUYáº¾T Äá»NH:** DĂ¹ng DynamoDB PAY_PER_REQUEST table `team14-budgetbot-cfn-transactions` Ä‘á»ƒ lÆ°u categorized transactions.

**PHÆ¯Æ NG ĂN CĂ‚N NHáº®C:**

- RDS PostgreSQL: máº¡nh hÆ¡n vá» SQL aggregation, nhÆ°ng cĂ³ chi phĂ­ instance, subnet group, backup lifecycle vĂ  connection management.
- SQLite/local file: tá»‘t cho local dev, nhÆ°ng khĂ´ng phĂ¹ há»£p deployed Lambda vĂ¬ khĂ´ng pháº£i shared persistent state.

**ÄO LÆ¯á»œNG:**

- Table state: `ACTIVE`.
- Item count khi validate: `91`.
- Billing mode: `PAY_PER_REQUEST`.
- Key schema: `user_id` hash key + `sk` range key.
- Persistent state test: upload data, refresh browser, gá»i `GET /transactions` hoáº·c `GET /summary`, dá»¯ liá»‡u váº«n Ä‘á»c Ä‘Æ°á»£c tá»« DynamoDB.

**Báº°NG CHá»¨NG:**

- AWS CLI: `aws dynamodb describe-table --table-name team14-budgetbot-cfn-transactions`
- CloudFormation: `TransactionsTable` trong `infrastructure/cloudformation.yaml`
- API routes: `GET /transactions`, `GET /summary`, `GET /stats`

**TRADE-OFF CHáº¤P NHáº¬N:**

DynamoDB khĂ´ng cĂ³ SQL `GROUP BY`, nĂªn app aggregate summary trong application code sau khi query transactions cá»§a user. Vá»›i sample hackathon, trade-off nĂ y há»£p lĂ½ vĂ  trĂ¡nh idle cost cá»§a RDS. Náº¿u scale lá»›n hÆ¡n, nhĂ³m sáº½ thĂªm GSI hoáº·c precomputed monthly summary items.

### DECISION 2 â€” Amazon Bedrock InvokeModel Vá»›i Nova Micro Batch Classification

**QUYáº¾T Äá»NH:** DĂ¹ng Amazon Bedrock Runtime `InvokeModel` vá»›i `apac.amazon.nova-micro-v1:0` Ä‘á»ƒ classify transaction. Prompt báº¯t model tráº£ JSON-only gá»“m `category` vĂ  `confidence`.

**PHÆ¯Æ NG ĂN CĂ‚N NHáº®C:**

- Local rule-based classifier: khĂ´ng tá»‘n AI cost nhÆ°ng yáº¿u vá»›i merchant chÆ°a tháº¥y nhÆ° `Vietnam Airlines HAN-SGN`, `KFC District 1`, `Cursor Pro` vĂ  opaque POS rows.
- Bedrock Knowledge Base/Agent: há»£p vá»›i document retrieval, nhÆ°ng BudgetBot lĂ  classification trĂªn CSV rows, khĂ´ng pháº£i RAG.
- Model lá»›n hÆ¡n: cĂ³ thá»ƒ tá»‘t hÆ¡n nhÆ°ng tá»‘n token cost hÆ¡n, chÆ°a cáº§n cho scoped demo.

**ÄO LÆ¯á»œNG:**

- Labeled test set local: 40 transactions.
- Accuracy report trong repo: `28/40 = 70.0%` cho baseline path Ä‘Æ°á»£c Ä‘Ă¡nh giĂ¡.
- Known-brand improvement: LocalAI `0/7` trĂªn unseen brands Ä‘Ă£ liá»‡t kĂª; Bedrock Æ°á»›c tĂ­nh khoáº£ng `6/7`.
- Upload metric validation: sample upload publish `TransactionsCategorized` vĂ  `LowConfidenceTransactions`.
- Low-confidence fallback: dĂ²ng cĂ³ `confidence="low"` xuáº¥t hiá»‡n trong `GET /review-queue`.

**Báº°NG CHá»¨NG:**

- `docs/accuracy_report.txt`
- `docs/failure_cases.md`
- `src/adapters/ai.py` JSON-only prompts
- `src/handlers.py` review queue vĂ  custom metrics
- CloudWatch metric `LowConfidenceTransactions`

**TRADE-OFF CHáº¤P NHáº¬N:**

Há»‡ thá»‘ng khĂ´ng claim AI tá»± Ä‘á»™ng Ä‘Ăºng 100%. Thay vĂ o Ä‘Ă³, app hiá»ƒn thá»‹ confidence vĂ  Ä‘Æ°a case khĂ´ng cháº¯c cháº¯n vĂ o review queue. CĂ¡ch nĂ y an toĂ n hÆ¡n cho dá»¯ liá»‡u tĂ i chĂ­nh.

### DECISION 3 â€” KhĂ´ng DĂ¹ng NAT Gateway, DĂ¹ng VPC Endpoints

**QUYáº¾T Äá»NH:** Cháº¡y Lambda trong private subnets á»Ÿ 2 AZ vĂ  truy cáº­p AWS services qua VPC endpoints thay vĂ¬ NAT Gateway.

**PHÆ¯Æ NG ĂN CĂ‚N NHáº®C:**

- NAT Gateway: Ä‘Æ¡n giáº£n cho internet egress chung, nhÆ°ng cĂ³ hourly cost vĂ  data processing cost.
- Lambda ngoĂ i VPC: network Ä‘Æ¡n giáº£n hÆ¡n, nhÆ°ng yáº¿u hÆ¡n vá» evidence Network Foundation vĂ  private service access.

**ÄO LÆ¯á»œNG:**

- VPC `vpc-044f26a2a760491ba`.
- Private subnets 2 AZ: `10.0.2.0/24` vĂ  `10.0.102.0/24`.
- S3 Gateway Endpoint: `vpce-0fa20050fb908c907`.
- DynamoDB Gateway Endpoint: `vpce-021f8d076fea679f5`.
- Bedrock Runtime Interface Endpoint: `vpce-0cf470982a94fec03`.
- CloudWatch Monitoring Interface Endpoint: `vpce-0e765088be49cb20d`.

**Báº°NG CHá»¨NG:**

- CloudFormation resources `S3GatewayEndpoint`, `DynamoDbGatewayEndpoint`, `BedrockRuntimeEndpoint`, `CloudWatchMonitoringEndpoint`.
- Private route table cĂ³ local route vĂ  Gateway Endpoint routes; khĂ´ng cĂ³ NAT route `0.0.0.0/0`.

**TRADE-OFF CHáº¤P NHáº¬N:**

Interface endpoints cĂ³ hourly cost theo AZ, nhÆ°ng giá»¯ backend private vĂ  trĂ¡nh NAT Gateway cost. VĂ¬ app chá»‰ gá»i AWS services, khĂ´ng cáº§n internet egress chung.

## 7. BĂ i Há»c RĂºt Ra

BĂ i há»c lá»›n nháº¥t lĂ  má»™t AI SaaS demo cháº¡y Ä‘Æ°á»£c phá»¥ thuá»™c nhiá»u vĂ o kiá»ƒm soĂ¡t scope vĂ  evidence, khĂ´ng pháº£i thĂªm tháº­t nhiá»u tĂ­nh nÄƒng. BudgetBot báº¯t Ä‘áº§u tá»« starter app, nhÆ°ng nhĂ³m pháº£i Ä‘Æ°a ra cĂ¡c quyáº¿t Ä‘á»‹nh triá»ƒn khai tháº­t: Lambda thay vĂ¬ ECS/EC2, DynamoDB thay vĂ¬ RDS, Bedrock InvokeModel trá»±c tiáº¿p thay vĂ¬ Knowledge Base, vĂ  VPC endpoints thay vĂ¬ NAT Gateway. CĂ¡c lá»±a chá»n nĂ y giĂºp há»‡ thá»‘ng Ä‘á»§ nhá» Ä‘á»ƒ ship, nhÆ°ng váº«n cover Ä‘á»§ 7 mandatory capabilities.

Váº¥n Ä‘á» sáº£n pháº©m khĂ³ nháº¥t lĂ  uncertainty trong classification. Má»™t sá»‘ transaction dá»… Ä‘oĂ¡n nhÆ° coffee shop hoáº·c airline, nhÆ°ng mĂ´ táº£ nhÆ° `Unknown merchant POS` khĂ´ng Ä‘á»§ tĂ­n hiá»‡u Ä‘á»ƒ model classify cháº¯c cháº¯n. CĂ¡ch xá»­ lĂ½ khĂ´ng pháº£i lĂ  giáº£ Ä‘á»‹nh AI luĂ´n Ä‘Ăºng. App tráº£ confidence, Ä‘Æ°a low-confidence rows vĂ o review queue, vĂ  há»— trá»£ user correction qua `POST /correct`. NhÆ° váº­y failure mode cá»§a AI trá»Ÿ thĂ nh má»™t workflow minh báº¡ch.

Náº¿u cĂ³ thĂªm má»™t sprint, nhĂ³m sáº½ thĂªm Cognito auth, budget goals theo thĂ¡ng, alert khi category vÆ°á»£t cap, recurring transaction detection vĂ  precomputed monthly summary table cho dataset lá»›n hÆ¡n.

## 8. Káº¿ Hoáº¡ch Teardown

Deadline teardown: **Sunday 1/6 EOD**. Commit xĂ¡c nháº­n vĂ o `docs/teardown_confirmation.md` vĂ  thĂªm screenshot Cost Explorer ngĂ y Monday.

### Thá»© Tá»± Teardown

1. Disable hoáº·c remove custom DNS aliases náº¿u xĂ³a CloudFront.
2. Delete CloudFormation stack `team14-budgetbot-iac`.
3. Náº¿u stack deletion fail vĂ¬ S3, empty cĂ¡c bucket nĂ y trÆ°á»›c:
   - `team14-budgetbot-cfn-frontend-123456789012-ap-southeast-1`
   - `team14-budgetbot-cfn-raw-123456789012-ap-southeast-1`
   - `team14-budgetbot-artifacts-123456789012-ap-southeast-1`
4. Delete CloudFront distribution `XXXXXXXXXXXX` sau khi disable náº¿u cáº§n.
5. Delete API Gateway `xxxxxxxxxx`.
6. Delete Lambda function `team14-budgetbot-cfn-backend`.
7. Delete DynamoDB table `team14-budgetbot-cfn-transactions` náº¿u cĂ²n.
8. Delete CloudWatch dashboard, alarm, saved query vĂ  Lambda log group.
9. Delete VPC endpoints, subnets, route tables, security groups, internet gateway vĂ  VPC sau cĂ¹ng.
10. Review Route 53 hosted zones vĂ  xĂ³a hosted zone `your-domain.example.com` dÆ° náº¿u khĂ´ng cáº§n.
11. Verify Cost Explorer vĂ o Monday 2/6 vĂ  commit screenshot.

### Lá»‡nh Teardown Khá»Ÿi Äiá»ƒm

```bash
aws cloudformation delete-stack \
  --profile hackathon \
  --region ap-southeast-1 \
  --stack-name team14-budgetbot-iac

aws cloudformation wait stack-delete-complete \
  --profile hackathon \
  --region ap-southeast-1 \
  --stack-name team14-budgetbot-iac
```

## Appendix A â€” Lá»‡nh Kiá»ƒm Chá»©ng Live

```bash
curl -I https://your-domain.example.com
curl https://xxxxxxxxxx.execute-api.ap-southeast-1.amazonaws.com/health

aws cloudformation describe-stacks \
  --profile hackathon \
  --region ap-southeast-1 \
  --stack-name team14-budgetbot-iac

aws cloudwatch describe-alarms \
  --profile hackathon \
  --region ap-southeast-1 \
  --alarm-names team14-budgetbot-cfn-low-confidence-transactions

aws dynamodb describe-continuous-backups \
  --profile hackathon \
  --region ap-southeast-1 \
  --table-name team14-budgetbot-cfn-transactions
```

## Appendix B â€” TĂ i Liá»‡u YĂªu Cáº§u ÄĂ£ DĂ¹ng

Báº£n Evidence Pack nĂ y Ä‘Æ°á»£c viáº¿t theo:

- `W7/W7_project_announcement.md`
- `W7/W7_learner_guide.md`
- `W7/W7_hackathon_rules.txt`
- `W7/W7_cost_estimates.md`
- `W7/starter_apps/README.md`

