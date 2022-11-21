output "HOST" {
  value = aws_redshift_cluster.default.dns_name
}

output "DB_NAME" {
  value = aws_redshift_cluster.default.database_name
}

output "DB_USER" {
  value = var.redshift_master_username
}

output "DB_PASSWORD" {
  value = var.redshift_master_password
}

output "DB_PORT" {
  value = aws_redshift_cluster.default.port
}

output "ARN" {
  value = aws_iam_role.redshift_role.arn
}