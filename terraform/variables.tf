################################################################################
# Variables
################################################################################

# ------------------------------------------------------------------------------
# General
# ------------------------------------------------------------------------------

variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name (e.g., dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "project_name" {
  description = "Project name used for resource naming"
  type        = string
  default     = "mattilda"
}

# ------------------------------------------------------------------------------
# Networking
# ------------------------------------------------------------------------------

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets (one per AZ)"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "availability_zones" {
  description = "Availability zones to use for subnets"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

# ------------------------------------------------------------------------------
# RDS (PostgreSQL)
# ------------------------------------------------------------------------------

variable "db_name" {
  description = "Name of the PostgreSQL database"
  type        = string
  default     = "mattilda_db"
}

variable "db_username" {
  description = "Master username for the RDS instance"
  type        = string
  default     = "mattilda_user"
}

variable "db_password" {
  description = "Master password for the RDS instance"
  type        = string
  sensitive   = true
}

variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"
}

variable "db_allocated_storage" {
  description = "Allocated storage for RDS in GB"
  type        = number
  default     = 20
}

variable "db_engine_version" {
  description = "PostgreSQL engine version"
  type        = string
  default     = "15.4"
}

# ------------------------------------------------------------------------------
# Redis (ElastiCache)
# ------------------------------------------------------------------------------

variable "redis_enabled" {
  description = "Whether to create Redis ElastiCache cluster"
  type        = bool
  default     = true
}

variable "redis_node_type" {
  description = "ElastiCache node type"
  type        = string
  default     = "cache.t3.micro"
}

# ------------------------------------------------------------------------------
# ECS / Fargate
# ------------------------------------------------------------------------------

variable "backend_image" {
  description = "Docker image URL for the backend (e.g., ECR or Docker Hub)"
  type        = string
  # Example: "123456789.dkr.ecr.us-east-1.amazonaws.com/mattilda-backend:latest"
  # Or: "your-dockerhub-user/mattilda-backend:latest"
}

variable "ecs_task_cpu" {
  description = "CPU units for ECS task (256 = 0.25 vCPU)"
  type        = number
  default     = 256
}

variable "ecs_task_memory" {
  description = "Memory for ECS task in MB"
  type        = number
  default     = 512
}

variable "ecs_desired_count" {
  description = "Desired number of ECS tasks"
  type        = number
  default     = 1
}

variable "container_port" {
  description = "Port the container listens on"
  type        = number
  default     = 8000
}

# ------------------------------------------------------------------------------
# Application
# ------------------------------------------------------------------------------

variable "api_key" {
  description = "API key for backend authentication"
  type        = string
  sensitive   = true
}
