#!/usr/bin/python
# Copyright: (c) 2023, dbi services, distributed without any warranty under the terms of the GNU General Public License v3
from __future__ import (absolute_import, division, print_function)
from ansible.errors import AnsibleError
from ansible.module_utils.basic import AnsibleModule

__metaclass__ = type

DOCUMENTATION = r'''
---
module: derive_pv_list

short_description: Provide a list of PVs of the VM for volumes attached by
                   YaK (excluding root volume).

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This is my longer description explaining my test module.

options:
    vol_info:
        description: the return of module 'vol_info' filtered
                     by the volume attached by YaK (excluding root volume).
        required: true
        type: dict
    ansible_devices:
        description: the variable 'ansible_devices' after the re-collection
                     of the facts on Linux hosts.
        required: false
        type: dict
    ansible_disks:
        description: the variable 'ansible_disks' after the re-collection
                     of the facts on Windows hosts.
        required: false
        type: dict
    provider:
        description: the provider name to derive the disk accordingly.
        required: true
        type: str
    os_type:
        description: the type of OS (linux/windows) to derive the
                     disk accordingly.
        required: true
        type: str
'''


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        vol_info=dict(type='dict', required=True),
        ansible_devices=dict(type='dict', required=False),
        ansible_disks=dict(type='list', required=False),
        provider=dict(type='str', required=True),
        os_type=dict(type='str', required=True),
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        original_message='',
        message='',
        pvs_in_vm=[],
        pv_list_extended=[],
        pv_list=[],
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # Ensure provider and os_type exists
    supported_provider = ["aws", "azure", "oci"]
    if module.params["provider"] not in supported_provider:
        raise AnsibleError(
            "provided 'provider' not supported: '{}'. Please use one of: '{}'\n"
            .format(module.params["provider"], supported_provider)
        )
    supported_os_type = ["linux", "windows"]
    if module.params["os_type"] not in supported_os_type:
        raise AnsibleError(
            "provided 'os_type' not supported: '{}'. Please use one of: '{}'\n"
            .format(module.params["os_type"], supported_os_type)
        )

    # Start
    if module.params["provider"] == "aws":
        if module.params["os_type"] == "linux":
            aws_volume = ""
            for key in module.params["ansible_devices"]:
                print(key)
                if module.params["ansible_devices"][key]["model"] == "Amazon Elastic Block Store":
                    for link in module.params["ansible_devices"][key]["links"]["ids"]:
                        print(link)
                        if link.startswith("nvme-Amazon_Elastic_Block_Store_vol"):
                            aws_volume = {
                                "path": "/dev/{}".format(key),
                                "aws_vol_id": "vol-{}".format(link.split('_vol')[1])
                            }
                            result["pvs_in_vm"].append(aws_volume)
                            for item in module.params["vol_info"]["volumes"]:
                                if item["id"] == aws_volume["aws_vol_id"]:
                                    result["pv_list_extended"].append(aws_volume)
                                    result["pv_list"].append(aws_volume["path"])

        if module.params["os_type"] == "windows":
            aws_volume = ""
            for disk in module.params["ansible_disks"]:
                aws_volume = "vol-{}".format(disk["physical_disk"]["serial_number"].split("_")[0][3:])
                aws_volume = {
                    "windows_disk_number": disk["physical_disk"]["device_id"],
                    "guid": disk["guid"],
                    "aws_vol_id": "vol-{}".format(disk["physical_disk"]["serial_number"].split("_")[0][3:])
                }
                for item in module.params["vol_info"]["volumes"]:
                    if item["id"] == aws_volume["aws_vol_id"]:
                        aws_volume["drive_letter"] = item["tags"]["Drive_letter"]
                        aws_volume["partition_label"] = item["tags"]["Partition_label"]
                        result["pv_list_extended"].append(aws_volume)
                        result["pv_list"].append(aws_volume["drive_letter"])

    if module.params["provider"] == "azure":
        if module.params["os_type"] == "linux":
            pass
        if module.params["os_type"] == "windows":
            pass
    if module.params["provider"] == "oci":
        if module.params["os_type"] == "linux":
            pass
        if module.params["os_type"] == "windows":
            pass

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

def main():
    run_module()


if __name__ == '__main__':
    main()