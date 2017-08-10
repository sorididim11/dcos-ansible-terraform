
resource "null_resource" "provision" {
  count = 1
  depends_on = ["openstack_compute_instance_v2.dcos-slave", "openstack_compute_instance_v2.dcos-master", "openstack_compute_floatingip_v2.floatip-dcos-master"]
  triggers = {
    trigger1 = "${var.num_masters}"
    trigger2 = "${var.num_slaves}"
    trigger3 = "${var.num_slaves_public}"
  }
  // create ansible host files
  provisioner "local-exec" {
    command = "echo '[dcos_bootstrap]\n${join("\n",openstack_compute_floatingip_v2.floatip-dcos-bootstrap.*.address)}\n' > ${var.ansible_inventory_home}/hosts"
  }

  provisioner "local-exec" {
    command = "echo '[dcos_masters]\n${join("\n",openstack_compute_floatingip_v2.floatip-dcos-master.*.address)}\n' >> ${var.ansible_inventory_home}/hosts"
  }

  provisioner "local-exec" {
    command = "echo '[dcos_slaves]\n${join("\n",openstack_compute_floatingip_v2.floatip-dcos-slave.*.address)}\n' >> ${var.ansible_inventory_home}/hosts"
  }

  provisioner "local-exec" {
    command = "echo '[dcos_slaves_public]\n${join("\n",openstack_compute_floatingip_v2.floatip-dcos-slave-public.*.address)}\n' >> ${var.ansible_inventory_home}/hosts"
  }

 provisioner "local-exec" {
    command = "echo '[dcos_nodes:children]\ndcos_masters\ndcos_slaves\ndcos_slaves_public' >> ${var.ansible_inventory_home}/hosts"
  }


  //run ansible

  # provisioner "local-exec" {
  #   command = "ANSIBLE_CONFIG=../playbooks/ansible.cfg ansible-playbook --private-key=${var.hos_keyfile} -i ansible_dcos_hosts ../playbooks/util-helion-collect_ip.yml -u hos"
  # }

  provisioner "local-exec" {
    command = "ANSIBLE_CONFIG=${var.ansible_inventory_home}/ansible.cfg ansible-playbook -i ${var.ansible_inventory_home}/hosts --private-key=${var.hos_keyfile}  ../ansible/playbooks/util-helion-chores.yml --valut-password-file=../password"
  }

  provisioner "local-exec" {
    command = "ANSIBLE_CONFIG=.${var.ansible_inventory_home}/ansible.cfg ansible-playbook -i ${var.ansible_inventory_home}/hosts --private-key=${var.hos_keyfile}  ../ansible/playbooks/step1-deploy-preconditions.yml --valut-password-file=../password"
  }
  
  provisioner "local-exec" {
    command = "ANSIBLE_CONFIG=${var.ansible_inventory_home}/ansible.cfg ansible-playbook -i ${var.ansible_inventory_home}/hosts -i ${var.ansible_inventory_home}/hosts --private-key=${var.hos_keyfile}  ../ansible/playbooks/step2-deploy-docker.yml --valut-password-file=../password"
  }
  
  provisioner "local-exec" {
    command = "ANSIBLE_CONFIG=${var.ansible_inventory_home}/ansible.cfg ansible-playbook -i ${var.ansible_inventory_home}/hosts --private-key=${var.hos_keyfile}  ../ansible/playbooks/step3-build-bootfiles.yml --valut-password-file=../password"
  }

  provisioner "local-exec" {
    command = "ANSIBLE_CONFIG=${var.ansible_inventory_home}/ansible.cfg ansible-playbook -i ${var.ansible_inventory_home}/hosts --private-key=${var.hos_keyfile}  ../ansible/playbooks/step4-deploy-cluster.yml --valut-password-file=../password"
  }
  
  provisioner "local-exec" {
    command = "ANSIBLE_CONFIG=${var.ansible_inventory_home}/ansible.cfg ansible-playbook -i ${var.ansible_inventory_home}/hosts --private-key=${var.hos_keyfile} ../ansible/playbooks/pkg-install-cli.yml --valut-password-file=../password"
  }
  
  provisioner "local-exec" {
    command = "ANSIBLE_CONFIG=${var.ansible_inventory_home}/ansible.cfg ansible-playbook -i ${var.ansible_inventory_home}/hosts --private-key=${var.hos_keyfile} ../ansible/playbooks/pkg-install-docker-registry.yml --valut-password-file=../password"
  }
  
  provisioner "local-exec" {
    command = "ANSIBLE_CONFIG=${var.ansible_inventory_home}/ansible.cfg ansible-playbook -i ${var.ansible_inventory_home}/hosts --private-key=${var.hos_keyfile}  ../ansible/playbooks/pkg-install-monitoring.yml --valut-password-file=../password"
  }


}
