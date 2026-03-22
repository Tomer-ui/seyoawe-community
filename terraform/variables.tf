variable "region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "us-east-2"
}

variable "cluster_name" {
  description = "Name for the EKS cluster and all related resources"
  type        = string
  default     = "seyoawe-cluster"
}

variable "node_instance_type" {
  description = "EC2 instance type for worker nodes"
  type        = string
  default     = "t3.small"
}

variable "node_count" {
  description = "Number of worker nodes"
  type        = number
  default     = 2
}
