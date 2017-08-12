require 'yaml'

# dynamic inventory based on vagrant config file(vagrant.yml)
settings = YAML.load_file 'vagrant.yml'
inventory_file = 'ansible/inventories/dev/hosts'
File.open(inventory_file, 'w') do |f|
  %w(dcos_masters dcos_slaves dcos_slaves_public dcos_cli dcos_bootstrap).each do |section|
    f.puts("[#{section}]")
    section = 'dcos_bootstrap' if section == 'dcos_cli'

    settings.each do |name, machine_info|
      f.puts(machine_info['ip']) if machine_info['type'] == section
    end
    f.puts('')
  end
end


Vagrant.configure('2') do |config|
  config.vm.box = 'centos/7'
  config.vm.synced_folder '.', '/vagrant', type: 'virtualbox'
  config.ssh.insert_key = false

  required_plugins = %w( vagrant-hostmanager vagrant-cachier vagrant-vbguest )
  required_plugins.each do |plugin|
    exec "vagrant plugin install #{plugin};vagrant #{ARGV.join(' ')}" unless Vagrant.has_plugin?(plugin) || ARGV[0] == 'plugin'
  end

  config.hostmanager.manage_guest = true
  config.hostmanager.ignore_private_ip = false
  config.hostmanager.include_offline = true
  config.cache.scope = :box
  config.vbguest.auto_update = true

  if Vagrant.has_plugin?('vagrant-proxyconf')
    config.proxy.http = 'http://web-proxy.corp.hp.com:8080'
    config.proxy.https = 'http://web-proxy.corp.hp.com:8080'
    config.proxy.no_proxy = 'localhost, 127.0.0.1'
  end

  settings.each do |name, machine_info|
    config.vm.define name do |node|
      node.vm.hostname = machine_info['name']
      node.vm.network :private_network, ip: machine_info['ip']
      node.vm.provider 'virtualbox' do |vb|
        vb.linked_clone = true
        vb.cpus = machine_info['cpus']
        vb.memory = machine_info['mem']
        vb.customize ['modifyvm', :id, '--natdnshostresolver1', 'on']
        # for dcos ntptime
        vb.customize ['guestproperty', 'set', :id, '/VirtualBox/GuestAdd/VBoxService/--timesync-set-threshold', 1000]
      end

      if machine_info['name'] == 'bootstrap'
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
          ansible.inventory_path = inventory_file
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
