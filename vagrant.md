# Vagrant tip

## ssh

* config.ssh.insert_key = false
  * 머쉰들이 공통으로 ~/vagrant.d/insecure-key 를 사용 즉 ansible-contoller에 private 키만 옴기면 됨.   if true key pairs are generated for each machine

## network

* Virtualbox natsystem을 vagrant에서 아직 사용 불가능
* 따라서 nat + host-oly(vboxnet4 을 현재 사용) 해야함.
* nat은  vb.customize ['modifyvm', :id, '--natdnshostresolver1', 'on']  추가 하면 사용.
* vagrant가 설정 host-only virtualbox에서 선택 dhcp 는 disable 시켜야함

## provider

* vb.customize ['modifyvm', :id, '--cpuexecutioncap', resource['cpu']] # 20% 씩 사용


## Ruby grammar 

### String 
 
#### String arary 
you dno't need to put '' in string
%w(dcos_masters dcos_slaves dcos_slaves_public dcos_cli dcos_bootstrap)

### Interpolation
when referncing variable - "[#{variable}]" in string 

"" <---  it allows intepoation including excape character "\n"
'' <---  it allows no inteplation including excape character like '\n' not working 
"[dcos_nodes:children]\ndcos_masters\ndcos_slaves\ndcos_slaves_public"