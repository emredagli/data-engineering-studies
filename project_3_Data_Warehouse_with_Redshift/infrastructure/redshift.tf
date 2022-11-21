resource "aws_redshift_cluster" "default" {
  cluster_identifier = var.redshift_cluster_identifier
  database_name      = var.redshift_database_name
  master_username    = var.redshift_master_username
  master_password    = var.redshift_master_password

  node_type       = var.redshift_node_type
  cluster_type    = var.redshift_cluster_type
  number_of_nodes = var.redshift_number_of_nodes

  iam_roles              = [aws_iam_role.redshift_role.arn]
  vpc_security_group_ids = [aws_security_group.redshift_security_group.id]
  publicly_accessible    = true
  skip_final_snapshot    = true

  depends_on = [
    aws_iam_role.redshift_role,
    aws_security_group.redshift_security_group
  ]
}
