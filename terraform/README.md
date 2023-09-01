# Terraform

This folder contains all code and resources required for the setup of AWS resources using terraform

## Configure environment variables

The following environment variables must be supplied in a `terraform.tfvars` file.

`access_key`
`region`
`availability_zone`
`secret_key`
`initial_database`
`database_name`
`database_username`
`database_password`
`database_ip`
`database_port`
`access_key_id`
`secret_access_key`
`email`
`bucket_name`

## Run the code

```sh
terraform init
terraform plan
terraform apply
```

## Destroy the terraform

```sh
terraform destroy
```
