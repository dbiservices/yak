# YaK

YaK Commnunity powered by [dbi-services](http://dbi-services.com) is a solution to deploy and configure your machines accross the Public Cloud Providers without any provider competency and dependency. 
With YaK you will have a uniq entry point to deploy, configure and manage all your machines for any Cloud provider.

Additional YaK as some products on top with subscription to deploy and manage your Oracle and PostgreSQL Database, more information on http://dbi-services.com/en/yak/components

## Design Principles

  - Source code based on Ansible and Python written in a Collextion yak.yak
  - No need to do any specific Ansible configuration.
  - YaK is fully based on Ansible Community.
  - YaK include it's own ansible inventory model.
       - Cross Cloud Provider
       - Multilevel (Environement/Server/Component)
  - Same command as ansible-playbook ansible-inventory are used.
  - Describe infrastructure for all Cloud Provider together in JSON as Ansible.
  - Manage machines instantly for differents Cloud Provider as AWS,Azure,OCI in parallel.
  - Be the easiest IT Cross Cloud Provider automation system to use, ever.
  - Allow development for additional Cloud Provider or Components


### Yak Usage

It exist 3 way to use YaK Community 

   - **YaK Demo**
      Easiest way to try and see how Yak Community is working, only follow the DEMO by press enter (can't be simplier)
      But if you want to make your own configuration please switch to YaK Testing, where your configuration remain persistente

   - **YaK Testing**
     Allow to Install and use YaK in your environment. Here you will need some knowledge because you have to install the YaK Container and then configure it with your own Cloud environment

   - **YaK Contribution**
     I hope to welcome a lot's of contributor here, to use and enhance the YaK Community package with new Cloud provider and features :-)
     To contribute you have to fork the project an then start the container with mapping your local code.
    
### YaK Demo

   Access our YaK DEMO environment to get a very simple and fast introduction on it !
   Try it, to see how it works in real life 
   
[Start Demo](https://yakdemo.dbi.services.com)


| Step | GUI |
| ------ | ------ |
| Connect     |  https://yakdemo.dbi-services.com |
| Login User:yak Passwd:yak  | <img src="/install/img/YaK_login.png"  width="400" height="400"> |
| Double-click on "Yak Demo Server" <br> Enter "stardemo aws"|  <img src="/install/img/YaK_demo.png" width="600" height="300"> |

### YaK Testing

Please see [Setup Instructions](YAK_TESTING.md)

###  Yak Contribution

Please see [Contribution Instructions](YAK_CONTRIBUTION.md)

## Yak inventory

This project use a dynamic inventory build from the configuration files available in
`./configuration/infrastructure` directory.

You can have a look on the inventory content using the standard `ansible` command:

```bash
ansible-inventory all --graph
```

More details about the inventory structure can be found in the inventory
[plugin documentation](https://gitlab.com/yak4all/yak/-/tree/main/collections/ansible_collections/yak/core).

## New environment example

To get an example how setup a new environment and servers
[example](https://gitlab.com/yak4all/yak/-/blob/main/configuration/README.md).

## License

GNU General Public License v3.0 or later
See COPYING to see the full text.

