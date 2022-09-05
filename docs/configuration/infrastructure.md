# New infrastructure

## Create new infrastructure from an existing example

To create a new infrastructure aws_testing, you can simply copy a new template, and adapt all parameters:

```
mkdir ./configuration/infrastructure/aws_testing
cp  ./configuration/infrastructure_sample/aws/variables.yml  ./configuration/infrastructure/aws_testing
```

## Update the variable from the create new infrastructure

At least the below parameter must be adapted
- security_group_id
- subnet_id
- bucket_name

```
is_cloud_environment: yes
operating_system: Oracle Linux 8.3
provider: aws
availability_zone: eu-central-1a
instance_type: t3.large
ami_id: ami-0211d10fb4a04824a
region_id: eu-central-1
security_group_id: sg-*****
subnet_id: subnet-**********
```

## New server

### Create a new server from a existing template

To create a new server srv01, you can simple copy  existing template and the adapt all parameters

```
mkdir ./configuration/infrastructure/aws_testing/srv01
cp ./configuration/infrastructure_sample/aws/srv-linux-test-01/variables.yml ./configuration/infrastructure/aws_testing/srv01
```

### Update the variable from the created new server

At least the below parameter must be adapted
- hostname
- host_ip_access: private_ip|public_ip
- private_ip
  - mode : manual | auto
  - ip : ip_address_value | or leave_it_empty_with_auto
- public_ip
  - mode : manual | auto | none
    - ip : ip_address_value | or leave_it_empty_with_auto_or_none

```
hostname: srv01
is_physical_server: no
ansible_user: ec2-user
host_ip_access: private_ip
private_ip:
   mode: manual
   ip: ********
public_ip:
   mode: none
   ip:
operating_system: OL8.5-x86_64-HVM-2021-11-24
ami_id: ami-07e51b655b107cd9b
instance_type: t3.large
ec2_volumes_params:
  - device_name: /dev/sda1
    ebs:
      volume_type: gp2
      volume_size: 10
      delete_on_termination: true
```