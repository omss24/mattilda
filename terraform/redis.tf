################################################################################
# ElastiCache Redis
#
# Creates a single-node Redis cluster for caching.
# Conditionally created based on var.redis_enabled.
################################################################################

# ------------------------------------------------------------------------------
# ElastiCache Subnet Group
# ------------------------------------------------------------------------------

resource "aws_elasticache_subnet_group" "main" {
  count = var.redis_enabled ? 1 : 0

  name        = "${var.project_name}-redis-subnet-group"
  description = "Subnet group for ElastiCache Redis"
  subnet_ids  = aws_subnet.public[*].id

  tags = {
    Name = "${var.project_name}-redis-subnet-group"
  }
}

# ------------------------------------------------------------------------------
# ElastiCache Redis Cluster
# ------------------------------------------------------------------------------

resource "aws_elasticache_cluster" "redis" {
  count = var.redis_enabled ? 1 : 0

  cluster_id           = "${var.project_name}-redis"
  engine               = "redis"
  engine_version       = "7.0"
  node_type            = var.redis_node_type
  num_cache_nodes      = 1
  port                 = 6379
  parameter_group_name = "default.redis7"

  subnet_group_name  = aws_elasticache_subnet_group.main[0].name
  security_group_ids = [aws_security_group.redis[0].id]

  # Maintenance window
  maintenance_window = "sun:05:00-sun:06:00"

  # Snapshot (disabled for cost savings in dev)
  snapshot_retention_limit = 0

  tags = {
    Name = "${var.project_name}-redis"
  }
}
