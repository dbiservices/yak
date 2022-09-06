# New infrastructure

In this example we will deploy a Linux server on AWS Cloud

## Create new infrastructure from an existing provider example

To create a new infrastructure aws_testing, you can simply copy an existing variables.yml template file, and adapt the parameters

```
cdh
mkdir ./configuration/infrastructure/aws_testing
cp  ./configuration/infrastructure_sample/aws/variables.yml  ./configuration/infrastructure/aws_testing
```

## Update the variables from the created new infrastructure

At least the below parameter must be adapted
- security_group_id
- subnet_id

```
cdh
vi ./configuration/infrastructure/aws_testing/variables.yml

# Copyright: (c) 2022, dbi services, distributed without any warranty under the terms of the GNU General Public License v3
is_cloud_environment: yes
environment: aws-testing
provider: aws
availability_zone: eu-central-1a
instance_type: t3.large
operating_system: OL8.5-x86_64-HVM-2021-11-24
ami_id: ami-07e51b655b107cd9b
region_id: eu-central-1
security_group_id: sg-*****
subnet_id: subnet-**********
```

## New server

### Create a server in you infrastructure from an existing template

To create a new server srv01, you can simply copy an existing variables.yml template file, and adapt the parameters

```
cdh
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
yak@68053b883b16:~/yak$ vi ./configuration/infrastructure/aws_testing/srv01/variables.yml

hostname: srv01
is_physical_server: no
ansible_user: ec2-user
host_ip_access: private_ip
private_ip:
   mode: auto
   ip: 
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


