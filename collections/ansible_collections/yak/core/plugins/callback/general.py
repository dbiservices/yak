# Make coding more python3-ish, this is required for contributions to Ansible
from __future__ import (absolute_import, division, print_function)
from os import environ
from ..modules.yak_inventory_update import api_update_server
from ..modules.yak_component_state_update import api_update_component
__metaclass__ = type

# Ref. https://technekey.com/how-to-write-a-simple-callback-plugin-for-ansible/

# not only visible to ansible-doc, it also 'declares' the options the plugin requires and how to configure them.
DOCUMENTATION = '''
name: general
callback_type: aggregate
requirements:
    - enable in configuration
short_description: Adds time to play stats
version_added: "2.0"  # for collections, use the collection version, not the Ansible version
description:
    - This callback extend the default Ansible behaviour with YaK Core logic.
options:
  boolean:
    description: Is a YaK Core db environment?
    ini:
      - section: yak_ansible_mode_db
        key: boolean
    env:
      - name: YAK_INVENTORY_TYPE
    default: false
'''
from datetime import datetime

from ansible.plugins.callback import CallbackBase


class CallbackModule(CallbackBase):
    """
    This callback module tells you how long your plays ran for.
    """
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'aggregate'
    CALLBACK_NAME = 'yak.core.general'

    # only needed if you ship it and don't want to enable by default
    CALLBACK_NEEDS_ENABLED = True

    def __init__(self):

        # make sure the expected objects are present, calling the base's __init__
        super(CallbackModule, self).__init__()

        self.mode = "file"
        if environ.get('YAK_INVENTORY_TYPE') is not None:
            if str(environ.get('YAK_INVENTORY_TYPE').lower()) == "database":
                self.mode = "database"
        self.is_component_specific = False
        if "YAK_CORE_COMPONENT" in environ:
            self.is_component_specific = True
            self.component_name = environ["YAK_CORE_COMPONENT"]

        self.output_separator = "==============================================================================="

    def yak_api_update_server(self, server_name, server_state):
        if self.mode == "database" and not self.is_component_specific:
            self._display.display(self.output_separator)
            self._display.display(f"= YaK Core: update server '{server_name}' state to '{server_state}'.")
            self._display.display(self.output_separator)
            api_update_server(
                server_name = server_name,
                server_state = server_state
            )
    
    def yak_api_update_component_state(self, component_state_name: str):
        """Updates the state of the component

        :param component_state_name: Name of the component state, possible values : declared deploying running stopping stopped terminating terminated failed
        :type component_state_name: str
        """
        if self.mode == "database" and self.is_component_specific:
            self._display.display(self.output_separator)
            self._display.display(f"= YaK Core: update component '{self.component_name}' state to '{component_state_name}'.")
            self._display.display(self.output_separator)
            api_update_component(self.component_name, component_state_name= component_state_name)


    def yak_display_playbook_info(self, playbook):
        self._display.display(self.output_separator)
        self._display.display("= YaK Core: starting in mode '{}'.".format(self.mode))
        self._display.display("= YaK Core: is_component_specific '{}'.".format(self.is_component_specific))
        self._display.display("= Thanks for using YaK :)")
        self._display.display(self.output_separator)

    #
    # Manage start of playbook
    #
    def v2_playbook_on_start(self, playbook):
        self.yak_display_playbook_info(playbook)
        self.yak_api_update_component_state("deploying")
    #
    # Manage end of playbook
    #
    def v2_playbook_on_stats(self, playbook):
        self.yak_display_playbook_info(playbook)

        if playbook.failures != {}:
        #     self.yak_api_update_component_state("running")
        # else:
            self.yak_api_update_component_state("failed")

    #
    # Manage failures
    #
    def v2_runner_on_unreachable(self, result):
        self.yak_api_update_server(
           server_name = str(result._host),
           server_state = "failed"
        )
        self.yak_api_update_component_state("failed")


    def v2_runner_on_failed(self, result, ignore_errors=False):
        self.yak_api_update_server(
           server_name = str(result._host),
           server_state = "failed"
        )
        self.yak_api_update_component_state("failed")

    def v2_runner_item_on_failed(self, result):
        self.yak_api_update_server(
           server_name = str(result._host),
           server_state = "failed"
        )
        self.yak_api_update_component_state("failed")

    def v2_runner_on_async_failed(self, result):
        self.yak_api_update_server(
           server_name = str(result._host),
           server_state = "failed"
        )
        self.yak_api_update_component_state("failed")
