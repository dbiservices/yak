
[yak 1.7.0  ]
  [Enhancements]
  - #31		CI/CD entry point change
  - #70		The host name on AWS is a generic name
  - #71		container image builder	
  - #78		Provide a command to display the Yak version in the container
  - #89		Add AD integration if configured directly for the windows server when created [Azure]
  - #90		YaK Core - Handle lvm2 package installation for Red Hat family OS
  - #91		Handle name resolution for YaK core in multi server environment
  - #106	Generate the winrm script for on-premise windows server
  - #112	Minify the yakenv image
  - #114	Configure ssh connection to another port for the Linux Machine deployment
  - #131	YaK Backend : Parameter table to define the variables per providers
  - #135	Additional UltraSSD disks for /u01, /u02 and /u90 not visible
  - #136	AWS EBS Volume encryption with default key
  - #143	Naming conventions of components in Azure
  - #144	UltraSSD on Azure
  - #145	review identical naming on the infrastructure sample and the infrastructure quickstart
  - #148	Optional AWS EBS + encryption of root device volume
  - #151	Add Tags in the pipeline jobs for AWS,OCI and AZURE
  - #152	AWS Pipeline : verify that we don't use CI_JOB_JWT and if we use it, it must be replaces by ID_TOKENS
  - #154	Ansible password not display any more while creating a server
  - #158	Extend /etc/hosts
  - #159	Delete AD entry when a Windows server is decommissioned is not working
  - #163	Azure allow instance creation with availability_zone parameter "zones"
  - #126	Implement Automatic Testing for YaK Core on AWS using the linux server aws/srv-linux-01/variables.yml

  [Fixes]
  - #92		target_type is not correctly populated
  - #96		Unable to configure storage for Ubuntu on AWS - /dev/sdb already in use
  - #97		Storage parameter should be set per default
  - #98		update doc about ping commands  under yak/docs
  - #100	Deploy on AWS node fails if volume_type not defined
  - #104	servers/start.yml doesn't work for servers deployed in Azure Cloud
  - #107	Windows Server on-premises issue with layout variable
  - #116	start.yml playbook does not work for AWS
  - #121	deploying again an existing server which is stopped
  - #122	server/start.yml no longer working
  - #127	server/stop.yml don't work completely on AZURE, because he only stop the instance but they are no  Stopped it (deallocated)
  - #128	Wrong Public IP information written when host_ip_access: private_ip and Public_IP = auto
  - #129	Cannot create 2 VM with sqlserver_instance component installation
  - #134	Docker image issue
  - #142	ssh OnPrem issues
  - #146	OCI Windows Instance Shape config missing
  - #150	Instance can no longer be deleted on Azure
  - #156	Mistake with default value for AWS volume type for yak 1.7.5-beta
  - #162	Storage_devices on Azure are used for the ROOT disks, which must not be the case
  - #167	Windows additional disks are not automatically delete on OCI
  - #125	Documentation setup missing line
