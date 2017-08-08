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