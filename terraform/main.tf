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
  image_uri     = "129033205317.dkr.ecr.eu-west-2.amazonaws.com/brink_of_extinction_plants_application:latest" 
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
      ACCESS_KEY_ID     = var.access_key_id
      SECRET_ACCESS_KEY = var.secret_access_key
      EMAIL             = var.email
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
  image_uri     = "129033205317.dkr.ecr.eu-west-2.amazonaws.com/ontheb-rink-ofextinction-archive:latest"
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



/*
resource "aws_ecs_cluster" "cluster" {
  name = "ontheb-rink-ofextinction-cluster"
}

resource "aws_ecs_task_definition" "dashboard-task-definition" {
  family       = "ontheb-rink-ofextinction-dashboard-task-definition"
  network_mode = "awsvpc"

  requires_compatibilities = ["FARGATE"]

  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "X86_64"
  }

  cpu    = "1024"
  memory = "3072"

  execution_role_arn = "arn:aws:iam::129033205317:role/ecsTaskExecutionRole"

  container_definitions = jsonencode([
    {
      name      = "ontheb-rink-ofextinction-dashboard",
      image     = "EXAMPLEEXAMPLEEXAMPLEEXAMPLEEXAMPLE",
      essential = true

      portMappings = [
        {
          containerPort : 80,
          hostPort : 80
          protocol    = "tcp"
          appProtocol = "http"
        },
        {
          containerPort : 8501,
          hostPort : 8501
          protocol    = "tcp"
          appProtocol = "http"
        }
      ]

      environment = [
        {
          name  = "DATABASE_NAME"
          value = var.database_name
        },
        {
          name  = "DATABASE_IP"
          value = var.database_ip
        },
        {
          name  = "DATABASE_PORT"
          value = var.database_port
        },
        {
          name  = "DATABASE_USERNAME"
          value = var.database_username
        },
        {
          name  = "DATABASE_PASSWORD"
          value = var.database_password
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-create-group"  = "true"
          "awslogs-group"         = "/ecs/"
          "awslogs-region"        = "eu-west-2"
          "awslogs-stream-prefix" = "ecs"
        }
      }
    }
  ])
}

resource "aws_security_group" "security-group-dashboard" {
  name        = "ontheb-rink-ofextinction-security-group-dashboard"
  description = "A security group for the dashboard allowing access to port 80 and 8501, made using terraform"

  vpc_id = data.aws_vpc.cohort-8-VPC.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8501
    to_port     = 8501
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_ecs_service" "dashboard-ecs-service" {
  name            = "ontheb-rink-ofextinction-dashboard-service"
  cluster         = aws_ecs_cluster.cluster.id
  task_definition = aws_ecs_task_definition.dashboard-task-definition.arn
  launch_type     = "FARGATE"
  desired_count   = 1

  network_configuration {
    subnets = [
      data.aws_subnet.cohort-8-public-subnet-1.id,
      data.aws_subnet.cohort-8-public-subnet-2.id,
      data.aws_subnet.cohort-8-public-subnet-3.id
    ]
    security_groups  = [resource.aws_security_group.security-group-dashboard.id]
    assign_public_ip = true
  }
}
*/



resource "aws_iam_role" "scheduler-role" {
  name = "ontheb-rink-ofextinction-scheduler-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "scheduler.amazonaws.com",
        },
        Action = "sts:AssumeRole",
      },
    ],
  })
}

resource "aws_scheduler_schedule" "live-pipeline-scheduler" {
  name                         = "ontheb-rink-ofextinction-live-pipeline-scheduler"
  schedule_expression_timezone = "Europe/London"
  description                  = "Schedule to run ETL pipeline every minute"
  state                        = "ENABLED"

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression = "cron(* * * * ? *)"

  target {
    arn      = "arn:aws:lambda:eu-west-2:129033205317:function:ontheb-rink-ofextinction-live-pipeline-lambda-tf"
    role_arn = "arn:aws:iam::129033205317:role/ontheb-rink-ofextinction-scheduler-role"
  }
}

resource "aws_scheduler_schedule" "archive-pipeline-schedule" {
  name                         = "ontheb-rink-ofextinction-archive-pipeline-schedule"
  schedule_expression_timezone = "Europe/London"
  description                  = "Schedule to run ETL pipeline every day"
  state                        = "ENABLED"

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression = "cron(5 0 * * ? *)"

  target {
    arn      = "arn:aws:lambda:eu-west-2:129033205317:function:ontheb-rink-ofextinction-archive-lambda-tf"
    role_arn = "arn:aws:iam::129033205317:role/ontheb-rink-ofextinction-scheduler-role"
  }
}
