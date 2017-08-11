
Vagrant.configure('2') do |config|
  config.vm.box = 'centos/7'
  config.vm.synced_folder '.', '/vagrant', type: 'virtualbox'
  config.ssh.insert_key = false

  if Vagrant.has_plugin?('vagrant-hostmanager')
    config.hostmanager.manage_guest = true
    config.hostmanager.ignore_private_ip = false
    config.hostmanager.include_offline = true
  end
  # for one line if based onruby guideline
  Vagrant.has_plugin?('vagrant-cachier') && config.cache.scope = :box
  Vagrant.has_plugin?('vagrant-vbguest') && config.vbguest.auto_update = true
  # if Vagrant.has_plugin?('vagrant-proxyconf')
  #   config.proxy.http = 'http://web-proxy.corp.hp.com:8080'
  #   config.proxy.https = 'http://web-proxy.corp.hp.com:8080'
  #   config.proxy.no_proxy = 'localhost, 127.0.0.1'
  # end

  {
    'slavepublic1' => { 'ip' => '10.0.15.41', 'cpus' => 3, 'mem' => 2000 },
    'slave3' => { 'ip' => '10.0.15.33', 'cpus' => 4, 'mem' => 3000 },
    'slave2' => { 'ip' => '10.0.15.32', 'cpus' => 4, 'mem' => 3000 },
    'slave1' => { 'ip' => '10.0.15.31', 'cpus' => 4, 'mem' => 3000 },
    'master3' => { 'ip' => '10.0.15.23', 'cpus' => 1, 'mem' => 1000 },
    'master2' => { 'ip' => '10.0.15.22', 'cpus' => 1, 'mem' => 1000 },
    'master1' => { 'ip' => '10.0.15.21', 'cpus' => 2, 'mem' => 2000 },
    'bootstrap' => { 'ip' => '10.0.15.11', 'cpus' => 2, 'mem' => 1000 }
  }.each do |name, resource|
    config.vm.define name do |node|
      node.vm.hostname = name
      node.vm.network :private_network, ip: resource['ip']
      node.vm.provider 'virtualbox' do |vb|
        vb.linked_clone = true
        vb.memory = resource['mem']
        vb.cpus = resource['cpus']
        vb.customize ['modifyvm', :id, '--natdnshostresolver1', 'on']
        # for dcos ntptime
        vb.customize ['guestproperty', 'set', :id, '/VirtualBox/GuestAdd/VBoxService/--timesync-set-threshold', 1000]
      end

      if name == 'bootstrap'
        ssh_prv_key = File.read("#{Dir.home}/.vagrant.d/insecure_private_key")
        node.vm.provision 'shell' do |sh|
          sh.inline = <<-SHELL
            [ !  -d /dcos ] && sudo mkdir /dcos && chown vagrant:vagrant /dcos
            [ ! -e /dcos/dcos_generate_config.ee.sh ] && cp /vagrant/dcos_generate_config.ee.sh /dcos && chown vagrant:vagrant /dcos/dcos_generate_config.ee.sh
            [ ! -e /home/vagrant/.ssh/id_rsa ] && echo "#{ssh_prv_key}" > /home/vagrant/.ssh/id_rsa && chown vagrant:vagrant /home/vagrant/.ssh/id_rsa && chmod 600 /home/vagrant/.ssh/id_rsa
            echo Provisioning of ssh keys completed [Success].
          SHELL
        end

        node.vm.provision :ansible_local do |ansible|
          ansible.install_mode = :pip # or default( by os package manager)
          ansible.version = '2.3.1'
          ansible.config_file = 'ansible/ansible.cfg'
          ansible.inventory_path = 'ansible/inventories/dev/hosts'
          # ansible.playbook = 'ansible/playbooks/util-config-ohmyzsh.yml'
          ansible.playbook = 'ansible/site.yml'
          ansible.limit = 'all'
          ansible.verbose = 'true'
          ansible.vault_password_file = 'password'
        end
      end
    end
  end
end
