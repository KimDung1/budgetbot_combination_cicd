# Infrastructure

Team 14 uses CloudFormation YAML for bonus path **E. Infrastructure as Code**.

Template:

- `cloudformation.yaml`

The template defines the BudgetBot serverless infrastructure:

- S3 frontend bucket with Block Public Access and SSE-S3 encryption
- CloudFront distribution with Origin Access Control
- S3 raw statements bucket with Block Public Access and SSE-S3 encryption
- DynamoDB transaction table with on-demand billing and PITR
- VPC with two public subnets and two private Lambda subnets across two AZs
- S3 and DynamoDB Gateway Endpoints
- Bedrock Runtime and CloudWatch Monitoring Interface Endpoints
- Lambda execution role with least-privilege inline policy
- Optional Lambda + API Gateway HTTP API when a Lambda zip artifact is provided
- CloudWatch dashboard and low-confidence transaction alarm
- Required W7 tags on supported resources

## Deploy Foundation Resources

This deploys the network, buckets, DynamoDB, IAM role, CloudFront, dashboard, and alarm.
It does not deploy Lambda/API Gateway until `DeployApplication=true`.

```bash
aws cloudformation deploy \
  --profile hackathon \
  --region ap-southeast-1 \
  --stack-name team14-budgetbot-iac \
  --template-file infrastructure/cloudformation.yaml \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides \
    ResourceNamePrefix=team14-budgetbot-cfn \
    OwnerTag=Team14 \
    EnvironmentTag=hackathon \
    DeployApplication=false
```

## Deploy Application Resources

After packaging the backend Lambda zip and uploading it to S3, redeploy with:

```bash
aws cloudformation deploy \
  --profile hackathon \
  --region ap-southeast-1 \
  --stack-name team14-budgetbot-iac \
  --template-file infrastructure/cloudformation.yaml \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides \
    ResourceNamePrefix=team14-budgetbot-cfn \
    OwnerTag=Team14 \
    EnvironmentTag=hackathon \
    DeployApplication=true \
    LambdaCodeS3Bucket=<artifact-bucket> \
    LambdaCodeS3Key=<lambda-zip-key>
```

## Inspect Outputs

```bash
aws cloudformation describe-stacks \
  --profile hackathon \
  --region ap-southeast-1 \
  --stack-name team14-budgetbot-iac \
  --query 'Stacks[0].Outputs'
```

## GitHub Actions Deployment

The repository includes `.github/workflows/build-and-deploy.yml`.
It runs on every push to `main` and can also be started manually from the GitHub Actions tab.

Required GitHub secrets:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `LAMBDA_ARTIFACT_BUCKET` — an existing S3 bucket used only to store Lambda zip artifacts.

Optional GitHub variables:

- `AWS_REGION` — defaults to `ap-southeast-1`
- `CFN_STACK_NAME` — defaults to `team14-budgetbot-iac`
- `RESOURCE_NAME_PREFIX` — defaults to `team14-budgetbot-cfn`
- `OWNER_TAG` — defaults to `Team14`
- `ENVIRONMENT_TAG` — defaults to `hackathon`
- `LAMBDA_ARTIFACT_PREFIX` — defaults to `lambda-artifacts`
- `BEDROCK_MODEL_ARN` — defaults to the Nova Micro inference profile used by the template.

The workflow builds the Lambda package from `requirements.txt` and `src/`, uploads it to the artifact bucket, deploys CloudFormation with `DeployApplication=true`, syncs `frontend/` to the frontend S3 bucket output, and invalidates CloudFront.

## Teardown

Empty S3 buckets first, then delete the stack:

```bash
aws cloudformation delete-stack \
  --profile hackathon \
  --region ap-southeast-1 \
  --stack-name team14-budgetbot-iac
```
