# todo 
1) config.yml template - handling no_proxy tokens - spliting string to array

# Ansible version 
ansible:  2.3.1
terraform 

#General Parameters for both community and enterprise version 
dcos_is_enterprise: True or False - enterprise dcos or open source 
dcos_cluster_name:               - user-defined cluster name
dcos_bootstrap_root_path: /dcos  - bootstrap installation home   
docs_boostrap_port: 9000         - bootstrap web server port for distributing installer files 
dcos_nic_name: eno1              - change Network Inferface card for private ip detection 
dcos_nic_pub_name: eno1          - change Network Inferface card for public ip detection 
dcos_is_use_proxy: false         - define when proxy is used 
dcos_resolver1:                  - dns1 ex) 8.8.8.8
dcos_resolver2:                  - dns2 
example)
proxy_env:
  dummy: dummy
  http_proxy: http://web-proxy.corp.hp.com:8080
  https_proxy: http://web-proxy.corp.hp.com:8080
  no_proxy: ".mesos,.thisdcos.directory,.dcos.directory,.zk,127.0.0.1,localhost,{{ groups['all'] | map('extract', hostvars, ['ansible_' + dcos_nic_name, 'ipv4', 'address']) | join(',') }}"


#Enterprise Parameters when dcos_is_enterprise: True
dcos_license: <license>          - when enterise dcos used.
dcos_superuser: root             - enterprise dcos superuser
dcos_superuser_pwd: root         - enterprise dcos superuser pwd
edcos_security_mode: permissive  # security type  disabed, permissive, strict 


# docker setting 
docker_volume_fs                  - default docker overlayfs (DC/OS 1.9 mendatory param for )
docker_version:                   - default 1.13.1 (DC/OS 1.9 mendatory param for )
dcos_is_insecure_registry: False  - install docker private regisry in insecure or secure 
dcos_host_volume_registry: '/tmp' - docker registry volume path. ex) /tmp/nfs-share or host diretory 


# One-touch Install  
install all prerequistes, docker, DC/OS cluster, CLI, Enterprise CLI, docker private registry, monitoring platform 
 ansible-playbook -i <inventory file> deploy-dcos.yml 


# Manual Install 
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


#Dynamic Reservation 
Reserve resources dynamically and Install custome marathon on it.
first specifiy roles including cpu, mem, gpu, disk and so on  quota.json in roles/dcos/node/quota/files/quota.json 
ansible-playbook -i <inventory file> op-add-quota.yml 

check the state of agents after the reservation 
dcos node --json