################################################################################
# Main Terraform Configuration
#
# This file serves as the entry point and documents the overall architecture.
################################################################################

# This Terraform configuration provisions the following AWS infrastructure:
#
# ┌─────────────────────────────────────────────────────────────────────────────┐
# │                                 VPC                                         │
# │  ┌────────────────────────┐    ┌────────────────────────┐                  │
# │  │   Public Subnet (AZ1)  │    │   Public Subnet (AZ2)  │                  │
# │  │                        │    │                        │                  │
# │  │  ┌──────────────────┐  │    │  ┌──────────────────┐  │                  │
# │  │  │   ECS Fargate    │  │    │  │   ECS Fargate    │  │                  │
# │  │  │   (Backend)      │  │    │  │   (Backend)      │  │                  │
# │  │  └────────┬─────────┘  │    │  └────────┬─────────┘  │                  │
# │  │           │            │    │           │            │                  │
# │  └───────────┼────────────┘    └───────────┼────────────┘                  │
# │              │                             │                               │
# │              └──────────┬──────────────────┘                               │
# │                         │                                                  │
# │              ┌──────────▼──────────┐                                       │
# │              │        ALB          │◄──── Internet (HTTP :80)              │
# │              └─────────────────────┘                                       │
# │                                                                            │
# │  ┌─────────────────────┐    ┌─────────────────────┐                       │
# │  │    RDS PostgreSQL   │    │  ElastiCache Redis  │                       │
# │  │    (mattilda_db)    │    │    (optional)       │                       │
# │  └─────────────────────┘    └─────────────────────┘                       │
# └─────────────────────────────────────────────────────────────────────────────┘
#
# Files:
#   - providers.tf  : Terraform & AWS provider configuration
#   - variables.tf  : Input variables
#   - outputs.tf    : Output values
#   - network.tf    : VPC, subnets, internet gateway, route tables
#   - security.tf   : Security groups for ALB, ECS, RDS, Redis
#   - rds.tf        : PostgreSQL RDS instance
#   - redis.tf      : ElastiCache Redis cluster (optional)
#   - ecs.tf        : ECS cluster, task definition, service, ALB
