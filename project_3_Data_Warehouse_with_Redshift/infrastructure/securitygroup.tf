resource "aws_security_group" "redshift_security_group" {
  vpc_id      = data.aws_vpc.default.id
  name        = "dwh_redshift_security_group"
  description = "Authorise redshift cluster access"

  ingress {
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    from_port   = 5439
    to_port     = 5439
  }
}