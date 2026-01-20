################################################################################
# RDS PostgreSQL
#
# Creates a PostgreSQL RDS instance for the application database.
# Uses a DB subnet group spanning multiple AZs for high availability.
################################################################################

# ------------------------------------------------------------------------------
# DB Subnet Group
# ------------------------------------------------------------------------------

resource "aws_db_subnet_group" "main" {
  name        = "${var.project_name}-db-subnet-group"
  description = "Subnet group for RDS PostgreSQL"
  subnet_ids  = aws_subnet.public[*].id

  tags = {
    Name = "${var.project_name}-db-subnet-group"
  }
}

# ------------------------------------------------------------------------------
# RDS PostgreSQL Instance
# ------------------------------------------------------------------------------

resource "aws_db_instance" "postgres" {
  identifier = "${var.project_name}-postgres"

  # Engine configuration
  engine            = "postgres"
  engine_version    = var.db_engine_version
  instance_class    = var.db_instance_class
  allocated_storage = var.db_allocated_storage
  storage_type      = "gp2"
  storage_encrypted = true

  # Database configuration
  db_name  = var.db_name
  username = var.db_username
  password = var.db_password
  port     = 5432

  # Network configuration
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  publicly_accessible    = false

  # Maintenance & backup
  backup_retention_period = 7
  backup_window           = "03:00-04:00"
  maintenance_window      = "Mon:04:00-Mon:05:00"

  # For dev/staging: allow deletion without final snapshot
  skip_final_snapshot      = true
  delete_automated_backups = true
  deletion_protection      = false

  # Performance Insights (free tier)
  performance_insights_enabled = false

  tags = {
    Name = "${var.project_name}-postgres"
  }
}
