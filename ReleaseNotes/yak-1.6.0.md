
[yak 1.6.0  ]
  [Enhancements]
  - #94  Windows server disk C is to small 
  - #102 Add parameter .vimrc from the YaK container to allow copy/paste with the mouse
  - #81  Generate inventory dynamically per component based on variables.yml/manifest.yml
  - #67  Move filesystem setting to components
  - #86  Add additional aliases and functions in the profile
  - #85  Add the Alfresco component in the ansible.cfg file
  - #66  New Parameter management for the Component
  - #65  Update yak dockerfile to use also the tagging for the yakenv container
  - #49  Update /etc/hosts with ansible_fqdn
  - #55  AWS:Possibility to give the AMI Name instead the AMI Id
  - #37  Artifact synchronisation from AWS to Azure and OCI
  - #36  Automatic TAG assignment during instance creation

  [Fixes]
  - #99  yak Inventory error, don't display the file which contains the error
  - #110 Remove legacy storage templates. Storage is now defined at the component level 
  - #38  Windows Instance deployment isn't idempodent 
  - #83  YaK Core - lvm2 package not installed for Rocky Linux
  - #79  Ansible user password stored in the <vmname>_winrm_script.ps1 file
  - #69  Review solution to install winrm.ps1 for an Windows OnPremise server
