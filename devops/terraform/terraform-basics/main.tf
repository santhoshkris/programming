provider "aws" {
  region = "us-east-1"
}

resource "aws_iam_user" "my_iam_user_abc" {
  name = "my_iam_user_abc_67893"
}

resource "aws_s3_bucket" "my_aws_s3_bucket" {
  bucket = "my-aws-s3-bucket-sanaws-12345"
}

output "my_aws_s3_bucket_details" {
  value = aws_s3_bucket.my_aws_s3_bucket
}
