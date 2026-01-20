################################################################################
# Terraform & Provider Configuration
################################################################################

terraform {
  required_version = ">= 1.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Local backend for simplicity in this challenge.
  # For production, switch to S3 backend:
  #
  # backend "s3" {
  #   bucket         = "your-terraform-state-bucket"
  #   key            = "mattilda/terraform.tfstate"
  #   region         = "us-east-1"
  #   encrypt        = true
  #   dynamodb_table = "terraform-locks"
  # }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "mattilda"
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}
