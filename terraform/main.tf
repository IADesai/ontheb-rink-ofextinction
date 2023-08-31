provider "aws" {
  region     = var.region
  access_key = var.access_key
  secret_key = var.secret_key
}

data "aws_vpc" "cohort-8-VPC" {
  id = "vpc-0e0f897ec7ddc230d"
}

data "aws_subnet" "cohort-8-public-subnet-1" {
  vpc_id            = data.aws_vpc.cohort-8-VPC.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "eu-west-2a"
}

data "aws_subnet" "cohort-8-public-subnet-2" {
  vpc_id            = data.aws_vpc.cohort-8-VPC.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "eu-west-2b"
}

data "aws_subnet" "cohort-8-public-subnet-3" {
  vpc_id            = data.aws_vpc.cohort-8-VPC.id
  cidr_block        = "10.0.3.0/24"
  availability_zone = "eu-west-2c"
}

output "cohort-8-public-subnet-ids" {
  value = [
    data.aws_subnet.cohort-8-public-subnet-1.id,
    data.aws_subnet.cohort-8-public-subnet-2.id,
    data.aws_subnet.cohort-8-public-subnet-3.id,
  ]
}

resource "aws_s3_bucket" "archive-bucket" {
  bucket = "ontheb-rink-ofextinction-archive-tf"
}

resource "aws_iam_role" "live-pipeline-lambda-role" {
  name = "ontheb-rink-ofextinction-live-pipeline-lambda-role-tf"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_lambda_function" "live-pipeline-lambda" {
  function_name = "ontheb-rink-ofextinction-live-pipeline-lambda-tf"
  role          = resource.aws_iam_role.live-pipeline-lambda-role.arn
  image_uri     = "EXAMPLEEXAMPLEEXAMPLEEXAMPLEEXAMPLE" 
  architectures = ["x86_64"]
  package_type  = "Image"

  environment {
    variables = {
      INITIAL_DATABASE  = var.initial_database
      DATABASE_NAME     = var.database_name
      DATABASE_PASSWORD = var.database_password
      DATABASE_PORT     = var.database_port
      DATABASE_USERNAME = var.database_username
      DATABASE_IP       = var.database_ip
    }
  }
}

resource "aws_iam_role" "archive-lambda-role" {
  name = "ontheb-rink-ofextinction-archive-lambda-role-tf"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_lambda_function" "archive-lambda" {
  function_name = "ontheb-rink-ofextinction-archive-lambda-tf"
  role          = resource.aws_iam_role.archive-lambda-role.arn
  image_uri     = "EXAMPLEEXAMPLEEXAMPLEEXAMPLEEXAMPLE" 
  architectures = ["x86_64"]
  package_type  = "Image"

  environment {
    variables = {
      EXAMPLE  = var.initial_database
      EXAMPLE     = var.database_name
      EXAMPLE = var.database_password
      EXAMPLE    = var.database_port
      EXAMPLE = var.database_username
      EXAMPLE    = var.database_ip
    }
  }
}