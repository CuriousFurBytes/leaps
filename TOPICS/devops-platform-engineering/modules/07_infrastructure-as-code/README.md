# Module 07: Infrastructure as Code

[← Module 06: CI/CD Pipelines](../06_cicd-pipelines/) | [Topic Home](../../README.md) | [Next → Module 08: Observability](../08_observability/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Advanced-orange)
![Time](https://img.shields.io/badge/time-10--14h-orange)

> Infrastructure as Code (IaC) applies software engineering practices to infrastructure management. This module covers Terraform (providers, state, modules), Pulumi, drift detection, and IaC best practices.

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Objectives](#objectives)
4. [Theory](#theory)
5. [Key Concepts](#key-concepts)
6. [Examples](#examples)
7. [Common Pitfalls](#common-pitfalls)
8. [Cross-Links](#cross-links)
9. [Summary](#summary)

---

## Overview

> [!NOTE]
> **This module is a stub.** Full content will be added in a future update.

Infrastructure as Code transforms infrastructure management from a manual, error-prone, undocumented process into a versioned, reviewable, automated workflow. When your entire infrastructure is code, it can be peer-reviewed, tested, version-controlled, and reproduced exactly. IaC is a prerequisite for consistent multi-environment deployments, disaster recovery, and scaling infrastructure teams.

---

## Prerequisites

- Module 06: CI/CD Pipelines — running Terraform in CI/CD is the production deployment model
- Basic cloud provider knowledge (AWS, GCP, or Azure) — understanding VPCs, compute, storage, and IAM helps

---

## Objectives

By the end of this module, you will be able to:

1. Write Terraform configurations using providers, resources, variables, outputs, and data sources
2. Understand and manage Terraform state — local, remote (S3/GCS/Terraform Cloud), and state locking
3. Design and use Terraform modules to create reusable, composable infrastructure components
4. Implement a CI/CD pipeline for Terraform: `plan` in CI, `apply` with approval in CD
5. Detect and remediate infrastructure drift using `terraform plan` and drift detection tooling
6. Understand Pulumi as an alternative to Terraform that uses real programming languages
7. Apply IaC best practices: DRY principles, module boundaries, secrets handling, and testing

---

## Theory

> [!NOTE]
> Full theory content coming soon.

### Terraform Core Concepts

```hcl
# main.tf — A complete, minimal Terraform configuration

terraform {
  required_version = ">= 1.7"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  # Remote state — always use remote state in production
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "prod/vpc/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"  # prevents concurrent applies
  }
}

provider "aws" {
  region = var.aws_region
}

# Variable definition
variable "aws_region" {
  type        = string
  description = "AWS region for all resources"
  default     = "us-east-1"
}

variable "environment" {
  type        = string
  description = "Environment name (dev, staging, production)"
  validation {
    condition     = contains(["dev", "staging", "production"], var.environment)
    error_message = "Environment must be dev, staging, or production."
  }
}

# Resource
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "${var.environment}-vpc"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

# Output
output "vpc_id" {
  value       = aws_vpc.main.id
  description = "The ID of the main VPC"
}
```

### Terraform State

```bash
# State stores the mapping between Terraform resources and real-world infrastructure
# It is the source of truth for what Terraform manages

# Common state operations
terraform state list                     # list all tracked resources
terraform state show aws_vpc.main        # inspect a specific resource
terraform state rm aws_vpc.old           # stop managing a resource (does not delete it)
terraform import aws_vpc.main vpc-abc123 # import existing infrastructure into state

# State locking prevents two applies from running simultaneously
# DynamoDB table used by the S3 backend:
resource "aws_dynamodb_table" "terraform_lock" {
  name         = "terraform-state-lock"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}
```

### Terraform Modules

```hcl
# modules/network/main.tf — reusable VPC module

variable "cidr_block" { type = string }
variable "environment" { type = string }
variable "public_subnet_cidrs" { type = list(string) }
variable "private_subnet_cidrs" { type = list(string) }

resource "aws_vpc" "this" {
  cidr_block = var.cidr_block
  tags = { Name = "${var.environment}-vpc", Environment = var.environment }
}

resource "aws_subnet" "public" {
  count             = length(var.public_subnet_cidrs)
  vpc_id            = aws_vpc.this.id
  cidr_block        = var.public_subnet_cidrs[count.index]
  map_public_ip_on_launch = true
}

output "vpc_id" { value = aws_vpc.this.id }
output "public_subnet_ids" { value = aws_subnet.public[*].id }

# ─────────────────────────────────────────────

# root/main.tf — using the module
module "network" {
  source = "./modules/network"   # or a registry URL

  cidr_block           = "10.0.0.0/16"
  environment          = "production"
  public_subnet_cidrs  = ["10.0.1.0/24", "10.0.2.0/24"]
  private_subnet_cidrs = ["10.0.10.0/24", "10.0.11.0/24"]
}

# Reference module outputs
resource "aws_eks_cluster" "main" {
  name     = "production"
  vpc_config {
    subnet_ids = module.network.public_subnet_ids
  }
}
```

### Drift Detection

```bash
# Drift occurs when infrastructure changes outside Terraform (manual console changes)

# Detect drift: terraform plan shows what would change
terraform plan -detailed-exitcode
# Exit code 0 = no changes (no drift)
# Exit code 1 = error
# Exit code 2 = changes present (drift detected)

# In CI, run drift detection on a schedule:
# terraform plan -detailed-exitcode || notify_on_drift
```

### Pulumi: IaC with Real Languages

```python
# Pulumi: Infrastructure as Code in Python
import pulumi
import pulumi_aws as aws

# Create a VPC using Python
vpc = aws.ec2.Vpc(
    "main-vpc",
    cidr_block="10.0.0.0/16",
    enable_dns_hostnames=True,
    tags={"Environment": "production", "ManagedBy": "pulumi"},
)

# Create a subnet using the VPC ID (automatic dependency tracking)
public_subnet = aws.ec2.Subnet(
    "public-subnet-1",
    vpc_id=vpc.id,      # Pulumi tracks this dependency automatically
    cidr_block="10.0.1.0/24",
    map_public_ip_on_launch=True,
)

# Export outputs
pulumi.export("vpc_id", vpc.id)
pulumi.export("public_subnet_id", public_subnet.id)
```

---

## Key Concepts

**State** — Terraform's record of what infrastructure it manages and its current configuration. State must be stored remotely (S3, GCS, Terraform Cloud) for team usage. Never commit `terraform.tfstate` to Git — it may contain secrets.

**Provider** — a plugin that Terraform uses to interact with an API (AWS, GCP, Azure, Kubernetes, GitHub, etc.). Providers are downloaded by `terraform init`. Provider versions must be pinned in `required_providers`.

**Module** — a reusable, parameterized collection of Terraform resources. Root modules consume child modules. Good module design: single responsibility, clear inputs and outputs, sensible defaults.

**Idempotency** — a core IaC property. Applying the same Terraform configuration multiple times produces the same result. Terraform achieves this by comparing desired state (your .tf files) to actual state (the state file) and only making necessary changes.

---

## Examples

> Full examples coming soon. Will include: provisioning a complete AWS VPC with EKS, a GitHub Actions pipeline for Terraform (plan on PR, apply on merge), using Terraform Cloud for state and remote operations, and testing Terraform modules with Terratest.

---

## Common Pitfalls

> Full pitfalls section coming soon. Key pitfalls: storing secrets in `.tf` files or state (use Vault or cloud secrets manager), not using remote state (local state does not work for teams), using `terraform apply` without reviewing the plan, not pinning provider versions (breaking changes in minor updates), and modifying state manually without using `terraform state` commands.

---

## Cross-Links

- [[devops-platform-engineering/modules/06_cicd-pipelines]] — Terraform runs in CI/CD pipelines; plan in PR, apply on merge with approval
- [[devops-platform-engineering/modules/08_observability]] — monitoring infrastructure is configured via IaC (Prometheus Operator, Grafana, alerting rules)
- [[devops-platform-engineering/modules/11_security-and-compliance]] — IaC security scanning (Checkov, tfsec) detects misconfigured cloud resources before they are provisioned

---

## Summary

- IaC treats infrastructure configuration as code: versioned, reviewed, tested, and automated
- Terraform uses HCL to declaratively describe resources; providers bridge to cloud APIs; state tracks real-world resources
- Remote state is mandatory for teams; state locking prevents concurrent applies
- Modules enable DRY infrastructure code: single responsibility, clear interface, composable
- Drift detection compares desired state to actual state; unmanaged changes are discovered via `terraform plan`
- Pulumi is an alternative that uses TypeScript, Python, Go, or C# instead of HCL
- Never commit secrets to IaC code or state — use Vault, AWS Secrets Manager, or equivalent
