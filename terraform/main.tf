terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~>3.69.0"
    }
  }
  required_version = ">=1.0.0"
  backend "s3" {
    bucket = "iiharanrlhyclpbcizqw"
    key    = "terraform/nullproject-state"
    region = "eu-west-1"
  }
}

provider "aws" {
  region  = "eu-west-1"
  default_tags {
    tags = {
      project = var.common_tag
    }
  }
}

