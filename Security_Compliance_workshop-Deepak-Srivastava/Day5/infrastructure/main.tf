provider "aws" {
  region = var.region
}

# Intentional insecure S3 bucket (public)
resource "aws_s3_bucket" "public_bucket" {
  bucket = "demo-insecure-bucket-123456"
  acl    = "public-read"     # insecure for demo
  tags = {
    Name = "insecure-demo-bucket"
  }
}

# Intentional insecure RDS (publicly accessible)
resource "aws_db_instance" "demo_db" {
  allocated_storage    = 10
  engine               = "mysql"
  engine_version       = "5.7"
  instance_class       = "db.t3.micro"
  name                 = "demo"
  username             = "admin"
  password             = "P@ssw0rd123"
  skip_final_snapshot  = true
  publicly_accessible  = true   # insecure for demo
}
