# Evidence Screenshot Checklist

Luu screenshot vao dung path ben duoi de Evidence Pack co bang chung ro rang. Ten file nen giu dung nhu checklist de de chen vao `docs/W7_evidence.md` va slides.

## Cost

| File path | Chup o dau | Noi dung can thay |
|---|---|---|
| `docs/evidence_screenshots/cost/01_budget_alert.png` | AWS Console -> Billing and Cost Management -> Budgets -> `W7-Team14-HardCap-100USD` | Budget $100, notification threshold $80, email/SNS subscription |
| `docs/evidence_screenshots/cost/02_sns_confirmed.png` | AWS Console -> SNS -> Topics -> `W7-Team14-BudgetAlerts` -> Subscriptions | Endpoint `your-email@example.com`, status confirmed/subscription ARN khong con PendingConfirmation |
| `docs/evidence_screenshots/cost/03_cost_anomaly_detection.png` | AWS Console -> Cost Management -> Cost Anomaly Detection | Monitor/subscription enabled |
| `docs/evidence_screenshots/cost/04_cost_explorer_day1_eod.png` | AWS Console -> Cost Explorer -> Daily cost, Group by Service | Day 1 EOD cost breakdown |
| `docs/evidence_screenshots/cost/05_cost_explorer_day2_eod.png` | AWS Console -> Cost Explorer -> Daily cost, Group by Service | Day 2 EOD cost breakdown |
| `docs/evidence_screenshots/cost/06_cost_explorer_friday_predemo.png` | AWS Console -> Cost Explorer -> Daily cost, Group by Service | Friday pre-demo total spend and top services |

## Security

| File path | Chup o dau | Noi dung can thay |
|---|---|---|
| `docs/evidence_screenshots/security/01_root_mfa_enabled.png` | AWS Console -> IAM -> Security credentials / Account security | Root MFA enabled |
| `docs/evidence_screenshots/security/02_lambda_role_policy.png` | AWS Console -> IAM -> Roles -> `team14-budgetbot-cfn-lambda-role` -> Permissions | `BudgetBotLambdaLeastPrivilegePolicy` with scoped S3/DynamoDB/Bedrock/CloudWatch actions |
| `docs/evidence_screenshots/security/03_frontend_bucket_private.png` | AWS Console -> S3 -> `team14-budgetbot-cfn-frontend-...` -> Permissions | Block Public Access ON, bucket not public |
| `docs/evidence_screenshots/security/04_raw_bucket_encryption.png` | AWS Console -> S3 -> `team14-budgetbot-cfn-raw-...` -> Properties | Default encryption AES256/SSE-S3 enabled |
| `docs/evidence_screenshots/security/05_cloudfront_https_acm.png` | AWS Console -> CloudFront -> Distribution `E349TWP6TRPSOC` -> General/Security | Alternate domain `your-domain.example.com`, ACM cert, TLSv1.2_2021 |
| `docs/evidence_screenshots/security/06_dynamodb_encryption_pitr.png` | AWS Console -> DynamoDB -> Tables -> `team14-budgetbot-cfn-transactions` | SSE enabled, PITR/continuous backups enabled |
| `docs/evidence_screenshots/security/07_vpc_private_subnets_endpoints.png` | AWS Console -> VPC -> Endpoints / Route tables | S3/DynamoDB/Bedrock/CloudWatch endpoints, private route table without NAT route |

## Monitoring

| File path | Chup o dau | Noi dung can thay |
|---|---|---|
| `docs/evidence_screenshots/monitoring/01_cloudwatch_dashboard.png` | AWS Console -> CloudWatch -> Dashboards -> `team14-budgetbot-cfn-observability` | Dashboard widget with BudgetBot metrics |
| `docs/evidence_screenshots/monitoring/02_custom_metrics.png` | AWS Console -> CloudWatch -> Metrics -> All metrics -> `BudgetBot/Team14` | `UploadSucceeded`, `TransactionsCategorized`, `LowConfidenceTransactions`, `BedrockLatencyMs` |
| `docs/evidence_screenshots/monitoring/03_alarm_ok.png` | AWS Console -> CloudWatch -> Alarms -> `team14-budgetbot-cfn-low-confidence-transactions` | Alarm state OK or ALARM, not INSUFFICIENT_DATA |
| `docs/evidence_screenshots/monitoring/04_logs_insights_query.png` | AWS Console -> CloudWatch -> Logs Insights -> saved query `team14-budgetbot-cfn/upload-classification-path` | Query text and result rows from Lambda logs |
| `docs/evidence_screenshots/monitoring/05_lambda_logs_bedrock_result.png` | AWS Console -> CloudWatch -> Log groups -> `/aws/lambda/team14-budgetbot-cfn-backend` | `bedrock_classification_result` log lines |

## Deployment And Architecture

| File path | Chup o dau | Noi dung can thay |
|---|---|---|
| `docs/evidence_screenshots/deployment/01_cloudformation_stack_outputs.png` | AWS Console -> CloudFormation -> Stacks -> `team14-budgetbot-iac` -> Outputs | Frontend bucket, raw bucket, API endpoint, CloudFront domain, DynamoDB table, Lambda role |
| `docs/evidence_screenshots/deployment/02_cloudformation_resources.png` | AWS Console -> CloudFormation -> Stacks -> `team14-budgetbot-iac` -> Resources | Stack resources CREATE/UPDATE_COMPLETE |
| `docs/evidence_screenshots/deployment/03_github_actions_success.png` | GitHub -> repo -> Actions -> latest `Build and Deploy` run | Successful CI/CD run |
| `docs/evidence_screenshots/deployment/04_github_actions_deploy_steps.png` | GitHub Actions run detail | Tests, Lambda package upload, CloudFormation deploy, frontend sync, CloudFront invalidation |
| `docs/evidence_screenshots/deployment/05_route53_records.png` | AWS Console -> Route 53 -> Hosted zone `topjob.id.vn` | A/AAAA alias for `your-domain.example.com` and ACM validation record |
| `docs/evidence_screenshots/deployment/06_api_gateway_routes.png` | AWS Console -> API Gateway -> API `xxxxxxxxxx` -> Routes | `/upload`, `/summary`, `/transactions`, `/review-queue`, `/accuracy`, `/stats`, `/correct`, `/health` |
| `docs/evidence_screenshots/deployment/07_lambda_configuration.png` | AWS Console -> Lambda -> `team14-budgetbot-cfn-backend` -> Configuration | Runtime, VPC, env vars `AI_BACKEND=bedrock`, `STORAGE_BACKEND=s3`, `USERSTORE_BACKEND=dynamodb` |

## Demo

| File path | Chup o dau | Noi dung can thay |
|---|---|---|
| `docs/evidence_screenshots/demo/01_live_url_home.png` | Browser -> `https://your-domain.example.com` | App loads from public HTTPS URL |
| `docs/evidence_screenshots/demo/02_upload_success.png` | BudgetBot UI after uploading `sample_data/bank_statement_q2_2026.csv` | Upload success, rows parsed/inserted |
| `docs/evidence_screenshots/demo/03_transactions_persisted.png` | BudgetBot UI -> transactions section after browser refresh | Transactions still visible after refresh |
| `docs/evidence_screenshots/demo/04_summary_by_category.png` | BudgetBot UI -> summary/category section | Spending summary by category and top drivers |
| `docs/evidence_screenshots/demo/05_review_queue.png` | BudgetBot UI -> review queue | Low-confidence transactions visible |
| `docs/evidence_screenshots/demo/06_accuracy_failure_cases.png` | BudgetBot UI -> AI performance/failure cases | Accuracy test and failure cases |

## Final Deliverable Files

| File path | Noi dung |
|---|---|
| `docs/architecture.png` | Final architecture diagram |
| `docs/slides.pdf` | 12-18 slides for demo day |
| `docs/demo.mp4` | 3-minute backup demo video, or put unlisted video link in `docs/W7_evidence.md` |
| `docs/teardown_confirmation.md` | Teardown confirmation after Sun 1/6 EOD |

