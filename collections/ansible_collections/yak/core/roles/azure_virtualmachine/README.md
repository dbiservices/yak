azure_virtualmachine
====================

Create, start, stop, delete a Linux or Windows Azure server on an existing Network Infrastructure

Requirements
------------

- Ansible Azure collection must be installed
- AZURE Account and Network parameter must be available

Variables
---------

This the defaults section

state
- Define the instance state (present, absent, started, stopped)

debug:
- Enable or disable debug mode (true, false)

image_id
- Define the ID of the Amazon Machine Image (AMI) to be used


Dependencies
------------

n/a


Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

