# Redshift Cluster Setup

[Terraform](https://www.terraform.io/) is used as infrastructure as code (IaC) to set up Redshift cluster required
resources.

Notes:

* Default VPC is used. So you need to have a default VPC before continue.
* The infrastructure setup defined on the course is mainly applied on Terraform configuration files

## 1. Install Terraform

I have used a Terraform version manager [tfenv](https://github.com/tfutils/tfenv) to install Terraform.

Install via Homebrew

```commandline
$ brew install tfenv

$ tfenv install 1.2.6
$ tfenv use 1.2.6

# Checking installed Terraform:
$ terraform --version
```

## 2. Terraform Setup

The following part will set up the Terraform and its local state under this `~/infrastructure` folder.

All terraform commands for this project must be executed under `~/infrastructure` folder.

```commandline
$ cd infrastructure
$ terraform init
```


## 3. Set Terraform Env. Variables

We need to use Terraform variable file `dev.tfvars` to pass desired variables to Terraform configuration files.

Please set the following values under [dev.tfvars](./dev.tfvars) as you desired.

`aws_access_key` & `aws_secret_key` should belong to the user which has admin access for programmatic usage:

```terraform
redshift_cluster_identifier = "dwh-cluster"
redshift_database_name      = "dwh_redshift_sparkify"
redshift_master_username    = "XXX"
redshift_master_password    = "XXX"

redshift_node_type       = "dc2.large"
redshift_cluster_type    = "multi-node"
redshift_number_of_nodes = 1

aws_region     = "us-west-2"
aws_access_key = "XXX"
aws_secret_key = "XXX"
```

## 4. Apply Terraform Infrastructure

The following code calculates the state changes between last executed state & current AWS state.

If anything is changed, it will ask you to apply changes:

```commandline
$ terraform apply -var-file="dev.tfvars"
```

It will prompt the change set and waits for your confirmation:

```terraform
Terraform will perform the following actions:

# aws_iam_role.redshift_role will be created
...
# aws_iam_role_policy.redshift_s3_policy will be created
...
# aws_redshift_cluster.default will be created
...
# aws_security_group.redshift_security_group will be created
...

Plan : 4 to add, 0 to change, 0 to destroy.
...

Do you want to perform these actions?
Terraform will perform the actions described above.
Only 'yes' will be accepted to approve.
```

Please type `yes` at this point. It will apply the changes and outputs the required config values for the next steps:

```terraform
Apply complete! Resources : 4 added, 0 changed, 0 destroyed.

Outputs :

ARN = "arn:aws:iam::XXX"
DB_NAME = "XXX"
DB_PASSWORD = "XXX"
DB_PORT = 5439
DB_USER = "XXX"
HOST = "XXX"

```

**You need to apply the output values** to the [./dwh.cfg](./../dwh.cfg) python config file!

# Remove Redshift Cluster

Again, under `~/infrastructure` folder:

```commandline
$ terraform destroy -var-file="dev.tfvars"
```

It will ask for confirmation, please type `yes`.

All resources created by Terraform will be deleted:

```terraform
aws_iam_role_policy.redshift_s3_policy : Destroying... [id = ...]
...

Destroy complete!Resources : 4 destroyed.
```

# Notes about Terraform

In an ideal Terraform configuration:

* Terraform state should be stored remotely under a S3 bucket for different environments (s.t. dev, staging, prod, etc.)
* DB Password should be randomly created and stored into AWS SecretManager
* VPC & network setup should be done

