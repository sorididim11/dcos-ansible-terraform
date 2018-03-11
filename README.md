# Enviornment

* DC/OS: 1.10 (1.9.* is not supported anymore)
* Docker: 17.03 (for beta-kubernetes on DC/OS)
* OS: Centos above 7.4 (DC/OS requirement)
* ansible:  2.3.1
* vagrant: 1.9.7
* terraform: 0.9.3

# DC/OS infra consideration 
dns_search - add local dns servers to config
public IP - moidfy detect-ip-pub. default is the same ip with private ip
use proxy - change dcos_is_use_proxy to true and add proxy config ex) proxy_env.http_proxy
docker_credentials 
docker_registyr_url
custom ca cert

# ToDo
1) portus registry to dcos pods (but  pods is not suppored in  strict mode)


# Features
  
* Support vagrant, terraform for openstack
* Install DC/OS cluster based on advanced custom installation of DC/OS which is upgradable
  - Install/configure prerequisites of DC/OS including docker
  - Generate config.yml file
  - Generate ip detec files 
  - Deploy DC/OS cluster 
* Support both Enterprise and Commmunity  DC/OS 
  - Install Open source or Enterprise DC/OS based on group variable of ansible, dcos_is_enterprise(True or False)
* Enterprise DC/OS
  - Upgrade security mode after installation
  - version upgrade supported
  - Reserve resources dynamically, create service accout with secret, assign permissions to the service accounts and install packages based on description files called pkg-desc in playbooks with any security mode.
  - fix DC/OS 1.9 bug in strict mode, when reserving resource dynamically (offically blocked by DC/OS)
  - Installing Custom marathon with role, dynamic reservation 
  - Supported private registry - Portus, cesanta
* Add/remove nodes after installation. 
* Install packages 
  - Install dcos cli & enterprise
  - Install secure/insecure docker registy by creating/updating certificate automactically on each node. 
  - Install monitoring platform based on cadvisor, influxdb and grafana


## Private registry 

3) marathon-ee
modify repo for bootstrap ip
repo: "cluster-registry.marathon.l4lb.thisdcos.directory:5000",

## Getting started
### General options 
0) generate ssh-key - input path of  private-key in ansible.cfg (default: ~/.ssh/dcos, dcos.pub) 
0) distributed keys to authorized_key on each node using "ansible-playbook playbooks/util-ssh-key.yml"
1) update ansible host file when not using vagrant or terrraform. check out <project-dir>/ansible/inventories/dev/hosts file.
2) (Enterprise only) Modify dcos_is_enterprise: True or False - enterprise dcos or open source(default: True)
3) (Enterprise only) Input dcos_license
4) (Enterprise only) Select edcos_security_mode: permissive  # security type  disabed, permissive, strict (default: strict)


### vagrant
1) Clone the project
2) Modify vagrantConf.yml to configure the number of nodes such as masters, slaves, slave_public(defulat 3 masters, 3 slaves, 1 slave public)
  - start with 'm' is master.
  - start with 's' is slave.
  - start with 'sp' is slave_public
  - boot is bootstrap node
3) create password file for license.
4) run - vagrant up

### terraform 
1) Clone the project 
2) install terraform 
3) go to dcos-ansible-terraform/terraform
3) source ihos.osrc - set credential for openstack for example. 
4) modify number of masters/slaves/slaves_public in variable.tf
5-1) check out security you wanna set. -  ansible/inventories/helion/group_vars/all.yml
5-1) check out dcos license in case you use enterprise DC/OS. -  ansible/inventories/helion/group_vars/all.yml 
6) terraform apply


## General Parameters for both community and enterprise version 

* dcos_is_enterprise: True or False - enterprise dcos or open source 
* dcos_cluster_name:               - user-defined cluster name
* dcos_bootstrap_root_path: /dcos  - bootstrap installation home   
* docs_boostrap_port: 9000         - bootstrap web server port for distributing installer files 
* dcos_is_use_proxy: false         - define when proxy is used 
* dcos_resolver1:                  - dns1 ex) 8.8.8.8
* dcos_resolver2:                  - dns2 
* proxy_env:
  + example)
    proxy_env:
      dummy: dummy
      http_proxy: http://web-proxy.corp.hp.com:8080
      https_proxy: http://web-proxy.corp.hp.com:8080
      no_proxy: ".mesos,.thisdcos.directory,.dcos.directory,.zk,127.0.0.1,localhost,{{ groups['all'] | map('extract', hostvars, ['ansible_' + dcos_nic_name, 'ipv4', 'address']) | join(',') }}"


## Enterprise Parameters when dcos_is_enterprise: True

* dcos_license: <license>          - when enterise dcos used.
* dcos_superuser: root             - enterprise dcos superuser
* dcos_superuser_pwd: root         - enterprise dcos superuser pwd
* edcos_security_mode: permissive  # security type  disabed, permissive, strict 


## docker setting 

* docker_volume_fs                  - default docker overlayfs (DC/OS 1.9 mendatory param for )
* docker_version:                   - default 1.13.1 (DC/OS 1.9 mendatory param for )
* dcos_is_secure_registry: True  - install docker private regisry in insecure or secure 
* dcos_host_volume_registry: '/tmp' - docker registry volume path. ex) /tmp/nfs-share or host diretory 


## One-touch Install  

* in <project-dir>/ansible directory, install all prerequistes, docker, DC/OS cluster, CLI, Enterprise CLI, docker private registry, monitoring platform 
    * ansible-playbook -i  playbooks/site.yml 


## Manual Install 

1) Install & configure prerequisite of DC/OS
 ansible-playbook -i <inventory file> step1-deploy-precondtions.yml 

2) Install & configure docker engine 
 ansible-playbook -i <inventory file> step2-deploy-docker.yml 

3) Generate DC/OS config and Build installers files.
 ansible-playbook -i <inventory file> step3-build-bootfiles.yml

4) Deploy cluster 
 ansible-playbook -i <inventory file> step4-deploy-cluster.yml 

5) Install DC/OS CLI + Enterprise CLI for only enterprise version & login automatically 
 ansible-playbook -i <inventory file> pkg-install-cli.yml 

6) Install secure/insecure docker private registry in the cluster (self-signed certificate)
 ansible-playbook -i <inventory file> pkg-install-docker-registry.yml 

6) Install monitoring platforom consisting of cadivior, influxdb, grafana 
 ansible-playbook -i <inventory file> pkg-install-monitoring.yml 


## Dynamic Reservation 

Reserve resources dynamically and Install custome marathon on it.
first specifiy roles including cpu, mem, gpu, disk and so on  quota.json in roles/dcos/node/quota/files/quota.json 

ansible-playbook -i <inventory file> op-add-quota.yml 

check the state of agents after the reservation 
dcos node --json


## Service account 's permission for custom marathon 
### Permissions + /users/<service-account>/operation
dcos:mesos:master:framework:role:<myrole>/users/<service-account-id>/create
dcos:mesos:master:reservation:role:<myrole>/users/<service-account-id>/create
dcos:mesos:master:volume:role:<myrole>/users/<service-account-id>/create
dcos:mesos:master:task:user:nobody/users/<service-account-id>/create
dcos:mesos:master:reservation:principal:<service-account-id>/users/<service-account-id>/delete
dcos:mesos:master:task:app_id:%252F/users/<service-account-id>/create
dcos:mesos:master:volume:principl:<service-account-id>/users/<servic

### Group/User permssions for custom marathon 
dcos:adminrouter:service:<service-name> full
dcos:service:marathon:<service-name>:services:/<service-or-group> <action>
dcos:adminrouter:ops:mesos full
dcos:adminrouter:ops:slave full
dcos:mesos:agent:executor:app_id:/<service-or-group> read
dcos:mesos:agent:framework:role:<myrole> read
dcos:mesos:agent:sandbox:app_id:/<service-or-group> read
dcos:mesos:agent:task:app_id:/<service-or-group> read
dcos:mesos:master:executor:app_id:/<service-or-group> read
dcos:mesos:master:framework:role:<myrole> read
dcos:mesos:master:task:app_id:/<service-or-group> read


### Private registry 
#### supported private registry. 
1) portus (by susue) 
2) cesante 

##### portus
portus installed in bootstrap node.  port https(443) is used basically
###### config 
1) LDAP integration - default config is not based on LDAP. to integrate LDAP, add LDAP config in role/dcos/packages/registry/templates/config-local.yml.j2 
2) registry certificate - Command name of certficate 
  update docker_private_url as domain name you use in group_vars/all.yml
3) add admin account to playbooks/pkg-des/registry-portus for ID, Password

###### install
to install portus, execute " ansible-playbook pkg-install-docker-registry-portus.yml"

steps
1) create certificates for registry 
2) install portus based on docker-compose
3) install the cert for docker daemon on each dcos agent
3) optional - download images from another registry to push them to currently installed portu registry.
4) update docker credentials for dcos mesos container runtime on each dcos agent


###### manaul login 

sudo docker login "<private registyr domain name without port>