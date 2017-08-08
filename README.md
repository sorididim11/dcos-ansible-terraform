# todo 
1) config.yml template - handling no_proxy tokens - spliting string to array

# docs-install
ansible version 2.3.1
terraform version

#parameters of dcos setup in <dcos-setup-home>/bootstrap/defaults/main.yml

0) 
# enterprise dcos or open source : True or False 
# diffrent installer file used  according to the param
dcos_is_enterprise: False 

1) 
# for enterprise dcos only, dcos license
dcos_license: <license>

2) 
# for enterprise dcos only, dcos admin account
dcos_superuser: root
dcos_superuser_pwd: root

3) 
# installation permission for ansible become_user
dcos_bootstrap_root_path: /dcos   
docs_boostrap_port: 80
ssh_superuser: root


4) 
# name of network interface card for ip detection  of all nodes
dcos_nic_name: eno1 # for ip-detect
dcos_nic_pub_name: eno1 # for ip-detect-public