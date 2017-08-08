
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
    command = "echo '[dcos_bootstrap]\n${join("\n",openstack_compute_floatingip_v2.floatip-dcos-bootstrap.*.address)}\n' > ansible_dcos_hosts"
  }

  provisioner "local-exec" {
    command = "echo '[dcos_masters]\n${join("\n",openstack_compute_floatingip_v2.floatip-dcos-master.*.address)}\n' >> ansible_dcos_hosts"
  }

  provisioner "local-exec" {
    command = "echo '[dcos_slaves]\n${join("\n",openstack_compute_floatingip_v2.floatip-dcos-slave.*.address)}\n' >> ansible_dcos_hosts"
  }

  provisioner "local-exec" {
    command = "echo '[dcos_slaves_public]\n${join("\n",openstack_compute_floatingip_v2.floatip-dcos-slave-public.*.address)}\n' >> ansible_dcos_hosts"
  }


  //run ansible

  # provisioner "local-exec" {
  #   command = "ANSIBLE_HOST_KEY_CHECKING=False ANSIBLE_CONFIG=../playbooks/ansible.cfg ansible-playbook --private-key=${var.hos_keyfile} -i ansible_dcos_hosts ../playbooks/util-helion-collect_ip.yml -u hos"
  # }



  provisioner "local-exec" {
    command = "ANSIBLE_HOST_KEY_CHECKING=False ANSIBLE_CONFIG=../playbooks/ansible.cfg ansible-playbook --private-key=${var.hos_keyfile} -i ansible_dcos_hosts ../playbooks/step1-deploy-preconditions.yml -u hos"
  }
  
  provisioner "local-exec" {
    command = "ANSIBLE_HOST_KEY_CHECKING=False ANSIBLE_CONFIG=../playbooks/ansible.cfg ansible-playbook --private-key=${var.hos_keyfile} -i ansible_dcos_hosts ../playbooks/step2-deploy-docker.yml -u hos "
  }
  
  provisioner "local-exec" {
    command = "ANSIBLE_HOST_KEY_CHECKING=False ANSIBLE_CONFIG=../playbooks/ansible.cfg ansible-playbook --private-key=${var.hos_keyfile} -i ansible_dcos_hosts ../playbooks/step3-build-bootfiles.yml -u hos "
  }

  provisioner "local-exec" {
    command = "ANSIBLE_HOST_KEY_CHECKING=False ANSIBLE_CONFIG=../playbooks/ansible.cfg ansible-playbook --private-key=${var.hos_keyfile} -i ansible_dcos_hosts ../playbooks/step4-deploy-cluster.yml -u hos "
  }
  
  provisioner "local-exec" {
    command = "ANSIBLE_HOST_KEY_CHECKING=False ANSIBLE_CONFIG=../playbooks/ansible.cfg ansible-playbook --private-key=${var.hos_keyfile} -i ansible_dcos_hosts ../playbooks/pkg-install-cli.yml -u hos "
  }
  
  provisioner "local-exec" {
    command = "ANSIBLE_HOST_KEY_CHECKING=False ANSIBLE_CONFIG=../playbooks/ansible.cfg ansible-playbook --private-key=${var.hos_keyfile} -i ansible_dcos_hosts ../playbooks/pkg-install-docker-registry.yml -u hos "
  }
  
  provisioner "local-exec" {
    command = "ANSIBLE_HOST_KEY_CHECKING=False ANSIBLE_CONFIG=../playbooks/ansible.cfg ansible-playbook --private-key=${var.hos_keyfile} -i ansible_dcos_hosts ../playbooks/pkg-install-monitoring.yml -u hos "
  }


}
