require 'yaml'
require 'vagrant/ui'

UI = Vagrant::UI::Colored.new

guest_home_dir = '/home/vagrant'
dcos_config = YAML.load_file('ansible/inventories/dev/group_vars/all.yml')
settings = YAML.load_file 'vagrantConf.yml'
dcos_version = dcos_config['dcos_version']
dcos_installer_package = dcos_config['dcos_is_enterprise'] ? "dcos_generate_config.ee.#{dcos_version}.sh" : "dcos_generate_config.#{dcos_version}.sh"

# Check if vagrant confile is in valid order. dcos_bootstrap should be at the bottom of config file
UI.info 'Checking if the location of dcos_boostrap of vagrantConf.xml is valid...', bold: true
if settings[settings.keys.last]['type'] != 'dcos_bootstrap'
  UI.error 'Please put dcos_bootstrap at the bottom of vagrantConf.yml because of provisioning order ', bold: true
  exit(-1)
end

# create dynamic inventory file. ansible provisioner 's dynamic inventory got some bugs
UI.info 'Create ansible dynamic inventory...', bold: true
inventory_file = 'ansible/inventories/dev/hosts'
File.open(inventory_file, 'w') do |f|
  %w(dcos_masters dcos_slaves dcos_slaves_public dcos_cli dcos_bootstrap).each do |section|
    f.puts("[#{section}]")
    section = 'dcos_bootstrap' if section == 'dcos_cli'

    settings.each do |_, machine_info|
      f.puts(machine_info['ip']) if machine_info['type'] == section
    end
    f.puts('')
  end
  f.write("[dcos_nodes:children]\ndcos_masters\ndcos_slaves\ndcos_slaves_public")
end

Vagrant.configure('2') do |config|
  config.vm.box = 'centos/7'
  config.ssh.insert_key = false
  config.vm.synced_folder '.', '/vagrant', type: 'virtualbox'

  required_plugins = %w( vagrant-hostmanager vagrant-cachier vagrant-vbguest )
  required_plugins.each do |plugin|
    exec "vagrant plugin install #{plugin};vagrant #{ARGV.join(' ')}" unless Vagrant.has_plugin?(plugin) || ARGV[0] == 'plugin'
  end

  config.hostmanager.enabled = true
  config.hostmanager.manage_guest = true
  config.hostmanager.ignore_private_ip = false
  config.hostmanager.include_offline = true
  config.cache.scope = :machine
  config.vbguest.auto_update = true

  if Vagrant.has_plugin?('vagrant-proxyconf')
    config.proxy.http = 'http://web-proxy.corp.hp.com:8080'
    config.proxy.https = 'http://web-proxy.corp.hp.com:8080'

    no_proxy = 'localhost,127.0.0.1,' + settings.map { |_, v| "#{v['ip']},#{v['name']}" }.join(',')
    UI.info "no proxies: #{no_proxy}"
    config.proxy.no_proxy = no_proxy
  end

  if Vagrant.has_plugin?('vagrant-registration')
    config.registration.proxy = 'mongo:8080'
    config.registration.proxyUser = 'flash'
    config.registration.proxyPassword = 'zarkov'
  end

  settings.each do |name, machine_info|
    config.vm.define name do |node|
      node.vm.hostname = machine_info['name']
      node.vm.network :private_network, ip: machine_info['ip']
      !machine_info['box'].nil? && node.vm.box = machine_info['box']

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
        UI.info 'Insert vagrant insecure key to bootstreap node...', bold: true
        node.vm.provision 'shell' do |sh|
          sh.inline = <<-SHELL
            [ !  -d /dcos ] && sudo mkdir /dcos && chown vagrant:vagrant /dcos
            [ ! -e /dcos/#{dcos_installer_package} ] && cp /vagrant/#{dcos_installer_package}  /dcos && chown vagrant:vagrant /dcos/#{dcos_installer_package}
            [ ! -e /home/vagrant/.ssh/id_rsa ] && echo "#{ssh_prv_key}" > /home/vagrant/.ssh/id_rsa && chown vagrant:vagrant /home/vagrant/.ssh/id_rsa && chmod 600 /home/vagrant/.ssh/id_rsa
            echo Provisioning of ssh keys completed [Success].
          SHELL
        end

        # Check ansible vault password
        if dcos_config['dcos_is_enterprise']
          UI.info 'Install DC/OS enterprise version? yes', bold: true
          if !File.exist?('password')
            echo 'Input Ansible vault password: '
            password = STDIN.gets.chomp
            File.open('password', 'w').write(password)
          else
            password = File.read('password')
          end
        end

        node.vm.provision 'shell', inline: "echo #{password} > #{guest_home_dir}/password"

        node.vm.provision :ansible_local do |ansible|
          ansible.install_mode = :pip # or default( by os package manager)
          ansible.version = '2.4.3.0'
          ansible.config_file = 'ansible/ansible.cfg'
          ansible.inventory_path = inventory_file
          ansible.limit = 'all'

          # ansible.playbook = 'ansible/playbooks/util-config-ohmyzsh.yml'
          ansible.playbook = 'ansible/vagrantSite.yml'
          ansible.verbose = 'true'
          ansible.vault_password_file = guest_home_dir + '/password' if dcos_config['dcos_is_enterprise']
        end
      end
    end
  end
end
