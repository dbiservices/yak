aws_ec2
=======

Create, start, stop, delete a Linux or Windows AWS EC2 instance on an existing Network Infrastructure

Requirements
------------

- Ansible Amazon.ec2 module must be installed
- AWS Account and Network parameter must be available

Variables
---------

This the defaults section

state
- Define the instance state (present, absent, started, stopped)

debug:
- Enable or disable debug mode (true, false)

Dependencies
------------

n/a

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - name: Deploy the cloud infrastructure
      hosts: localhost
      tasks:

    - include_role:
        name: yak.core.aws_ec2
      vars:
        state: present
        ec2_instance_base_directory: /tmp/ec2_instance
        nb_instances: 3
        debug: false
        image_id: ami-009ds8fgsd9gf8sdf

