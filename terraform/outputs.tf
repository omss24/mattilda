################################################################################
# Outputs
#
# Exposes key infrastructure information for developers and CI/CD pipelines.
################################################################################

# ------------------------------------------------------------------------------
# Networking
# ------------------------------------------------------------------------------

output "vpc_id" {
  description = "ID of the VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "IDs of public subnets"
  value       = aws_subnet.public[*].id
}

# ------------------------------------------------------------------------------
# RDS PostgreSQL
# ------------------------------------------------------------------------------

output "rds_endpoint" {
  description = "RDS PostgreSQL endpoint (host:port)"
  value       = aws_db_instance.postgres.endpoint
}

output "rds_hostname" {
  description = "RDS PostgreSQL hostname"
  value       = aws_db_instance.postgres.address
}

output "rds_port" {
  description = "RDS PostgreSQL port"
  value       = aws_db_instance.postgres.port
}

output "rds_db_name" {
  description = "RDS database name"
  value       = aws_db_instance.postgres.db_name
}

output "rds_username" {
  description = "RDS master username"
  value       = aws_db_instance.postgres.username
  sensitive   = true
}

output "database_url" {
  description = "Full DATABASE_URL for the application"
  value       = local.database_url
  sensitive   = true
}

# ------------------------------------------------------------------------------
# Redis (ElastiCache)
# ------------------------------------------------------------------------------

output "redis_endpoint" {
  description = "Redis ElastiCache endpoint"
  value       = var.redis_enabled ? aws_elasticache_cluster.redis[0].cache_nodes[0].address : null
}

output "redis_port" {
  description = "Redis port"
  value       = var.redis_enabled ? 6379 : null
}

output "redis_url" {
  description = "Full REDIS_URL for the application"
  value       = var.redis_enabled ? local.redis_url : null
}

# ------------------------------------------------------------------------------
# ECS
# ------------------------------------------------------------------------------

output "ecs_cluster_name" {
  description = "ECS cluster name"
  value       = aws_ecs_cluster.main.name
}

output "ecs_service_name" {
  description = "ECS service name"
  value       = aws_ecs_service.backend.name
}

# ------------------------------------------------------------------------------
# Load Balancer
# ------------------------------------------------------------------------------

output "alb_dns_name" {
  description = "ALB DNS name (API public URL)"
  value       = aws_lb.main.dns_name
}

output "api_url" {
  description = "Full API URL"
  value       = "http://${aws_lb.main.dns_name}"
}

# ------------------------------------------------------------------------------
# CloudWatch
# ------------------------------------------------------------------------------

output "cloudwatch_log_group" {
  description = "CloudWatch log group for ECS tasks"
  value       = aws_cloudwatch_log_group.ecs.name
}
