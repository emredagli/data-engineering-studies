variable "aws_access_key" {
  type = string
}

variable "aws_secret_key" {
  type = string
}

variable "aws_region" {
  type = string
}

variable "redshift_cluster_identifier" {
  type = string
}

variable "redshift_database_name" {
  type = string
}

variable "redshift_master_username" {
  type = string
}

variable "redshift_master_password" {
  type = string
}

variable "redshift_node_type" {
  type = string
}

variable "redshift_cluster_type" {
  type = string
}

variable "redshift_number_of_nodes" {
  type = number
}