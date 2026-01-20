# Terraform Infrastructure for Mattilda Backend

> ⚠️ **DISCLAIMER**: This Terraform configuration has **NOT been tested on a real AWS account**. It is provided as a reference implementation for the code challenge. Review and adjust before deploying to production.

## Architecture Overview

This Terraform configuration provisions the following AWS infrastructure:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                 VPC                                         │
│  ┌────────────────────────┐    ┌────────────────────────┐                  │
│  │   Public Subnet (AZ1)  │    │   Public Subnet (AZ2)  │                  │
│  │                        │    │                        │                  │
│  │  ┌──────────────────┐  │    │  ┌──────────────────┐  │                  │
│  │  │   ECS Fargate    │  │    │  │   ECS Fargate    │  │                  │
│  │  │   (Backend)      │  │    │  │   (Backend)      │  │                  │
│  │  └────────┬─────────┘  │    │  └────────┬─────────┘  │                  │
│  │           │            │    │           │            │                  │
│  └───────────┼────────────┘    └───────────┼────────────┘                  │
│              │                             │                               │
│              └──────────┬──────────────────┘                               │
│                         │                                                  │
│              ┌──────────▼──────────┐                                       │
│              │        ALB          │◄──── Internet (HTTP :80)              │
│              └─────────────────────┘                                       │
│                                                                            │
│  ┌─────────────────────┐    ┌─────────────────────┐                       │
│  │    RDS PostgreSQL   │    │  ElastiCache Redis  │                       │
│  │    (mattilda_db)    │    │    (optional)       │                       │
│  └─────────────────────┘    └─────────────────────┘                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Components

| Component | Service | Description |
|-----------|---------|-------------|
| **Networking** | VPC, Subnets, IGW | VPC with 2 public subnets across AZs |
| **Compute** | ECS Fargate | Serverless container orchestration |
| **Load Balancer** | ALB | Application Load Balancer on port 80 |
| **Database** | RDS PostgreSQL | Managed PostgreSQL 15.x |
| **Caching** | ElastiCache Redis | Optional Redis cluster |
| **Logging** | CloudWatch Logs | Container logs with 7-day retention |

## Prerequisites

1. **Terraform** >= 1.0.0 installed
   ```bash
   # macOS
   brew install terraform
   
   # Linux
   wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
   unzip terraform_1.6.0_linux_amd64.zip
   sudo mv terraform /usr/local/bin/
   ```

2. **AWS CLI** configured with credentials
   ```bash
   aws configure
   # Or set environment variables:
   export AWS_ACCESS_KEY_ID="your-access-key"
   export AWS_SECRET_ACCESS_KEY="your-secret-key"
   export AWS_REGION="us-east-1"
   ```

3. **Docker image** pushed to ECR or Docker Hub
   ```bash
   # Example: Push to ECR
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
   docker build -t mattilda-backend .
   docker tag mattilda-backend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/mattilda-backend:latest
   docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/mattilda-backend:latest
   ```

## Usage

### 1. Initialize Terraform

```bash
cd terraform
terraform init
```

### 2. Create Variables File

Create a `terraform.tfvars` file with your values:

```hcl
# terraform.tfvars

# Required
backend_image = "your-account-id.dkr.ecr.us-east-1.amazonaws.com/mattilda-backend:latest"
db_password   = "your-secure-database-password"
api_key       = "your-secure-api-key"

# Optional (have defaults)
aws_region        = "us-east-1"
environment       = "dev"
db_username       = "mattilda_user"
db_name           = "mattilda_db"
ecs_desired_count = 1
redis_enabled     = true
```

> ⚠️ **Security**: Never commit `terraform.tfvars` to version control. Add it to `.gitignore`.

### 3. Review the Plan

```bash
terraform plan
```

### 4. Apply Infrastructure

```bash
terraform apply
```

Type `yes` when prompted to confirm.

### 5. Get Outputs

After successful apply:

```bash
# Get the API URL
terraform output api_url

# Get all outputs
terraform output

# Get sensitive outputs
terraform output -json | jq
```

## Variables Reference

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `aws_region` | string | `us-east-1` | AWS region |
| `environment` | string | `dev` | Environment name |
| `project_name` | string | `mattilda` | Project name for resource naming |
| `vpc_cidr` | string | `10.0.0.0/16` | VPC CIDR block |
| `public_subnet_cidrs` | list(string) | `["10.0.1.0/24", "10.0.2.0/24"]` | Public subnet CIDRs |
| `db_name` | string | `mattilda_db` | PostgreSQL database name |
| `db_username` | string | `mattilda_user` | PostgreSQL username |
| `db_password` | string | **required** | PostgreSQL password (sensitive) |
| `db_instance_class` | string | `db.t3.micro` | RDS instance type |
| `redis_enabled` | bool | `true` | Create Redis cluster |
| `redis_node_type` | string | `cache.t3.micro` | ElastiCache node type |
| `backend_image` | string | **required** | Docker image URL |
| `ecs_task_cpu` | number | `256` | ECS task CPU units |
| `ecs_task_memory` | number | `512` | ECS task memory (MB) |
| `ecs_desired_count` | number | `1` | Number of ECS tasks |
| `api_key` | string | **required** | API key for backend auth |

## Outputs Reference

| Output | Description |
|--------|-------------|
| `vpc_id` | VPC ID |
| `public_subnet_ids` | List of public subnet IDs |
| `rds_endpoint` | RDS endpoint (host:port) |
| `rds_hostname` | RDS hostname |
| `rds_db_name` | Database name |
| `database_url` | Full DATABASE_URL (sensitive) |
| `redis_endpoint` | Redis endpoint (if enabled) |
| `redis_url` | Full REDIS_URL (if enabled) |
| `alb_dns_name` | ALB DNS name |
| `api_url` | Full API URL (http://...) |
| `ecs_cluster_name` | ECS cluster name |
| `cloudwatch_log_group` | CloudWatch log group name |

## Connecting to the API

After deployment:

```bash
# Get the API URL
API_URL=$(terraform output -raw api_url)

# Test health endpoint
curl $API_URL/health

# Test with API key
curl -H "X-API-Key: your-api-key" $API_URL/api/v1/schools
```

## Running Migrations

The application container should run migrations on startup. If you need to run them manually:

```bash
# Get ECS cluster and service names
CLUSTER=$(terraform output -raw ecs_cluster_name)
SERVICE=$(terraform output -raw ecs_service_name)

# Execute command in running container
aws ecs execute-command \
  --cluster $CLUSTER \
  --task <task-id> \
  --container mattilda-backend \
  --interactive \
  --command "alembic upgrade head"
```

## Viewing Logs

```bash
# Get log group name
LOG_GROUP=$(terraform output -raw cloudwatch_log_group)

# View recent logs
aws logs tail $LOG_GROUP --follow
```

## Destroying Infrastructure

```bash
terraform destroy
```

Type `yes` when prompted. This will delete all resources.

## Cost Estimation

Approximate monthly costs (us-east-1, minimal config):

| Resource | Type | Est. Cost |
|----------|------|-----------|
| RDS | db.t3.micro | ~$15 |
| ElastiCache | cache.t3.micro | ~$12 |
| ECS Fargate | 0.25 vCPU, 0.5GB | ~$10 |
| ALB | Application LB | ~$16 |
| Data Transfer | Varies | ~$5+ |
| **Total** | | **~$58/month** |

> Costs may vary. Use AWS Cost Calculator for accurate estimates.

## Production Considerations

For a production deployment, consider:

1. **HTTPS**: Add ACM certificate and HTTPS listener on port 443
2. **Private Subnets**: Move RDS and ECS to private subnets with NAT Gateway
3. **Multi-AZ RDS**: Enable `multi_az = true` for database HA
4. **Auto Scaling**: Add ECS service auto-scaling policies
5. **Secrets Manager**: Store `db_password` and `api_key` in AWS Secrets Manager
6. **Remote State**: Configure S3 backend with DynamoDB locking
7. **WAF**: Add AWS WAF for additional security
8. **Monitoring**: Enable Container Insights and set up CloudWatch Alarms

## Troubleshooting

### ECS Task Fails to Start

Check CloudWatch logs:
```bash
aws logs tail /ecs/mattilda --follow
```

Common issues:
- Image not found: Verify `backend_image` is correct and accessible
- Database connection: Ensure security groups allow traffic
- Health check failing: Verify `/health` endpoint works

### Cannot Connect to RDS

- Verify ECS security group allows outbound to RDS
- Check RDS security group allows inbound from ECS
- Confirm RDS is in the same VPC

### ALB Returns 502

- Check ECS tasks are healthy in the target group
- Verify container port matches target group port
- Check application logs for startup errors
