# -*- mode: ruby -*-
# vi: set ft=ruby :
Vagrant.require_version ">= 1.4.1"

Vagrant.configure("2") do |config|
  # All Vagrant configuration is done here. The most common configuration
  # options are documented and commented below. For a complete reference,
  # please see the online documentation at vagrantup.com.

  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = "precise64"
  #config.vm.box = "trusty64"

  # The url from where the 'config.vm.box' box will be fetched if it
  # doesn't already exist on the user's system.
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"
  #config.vm.box_url = "http://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  config.vm.provider :virtualbox do |vb|
    # Use VBoxManage to customize the VM. For example to change memory:
    vb.customize ["modifyvm", :id, "--memory", "512"]
  end

  config.vm.define :api do |api|
    config.vm.hostname = "api"
    config.vm.network :private_network, ip: "192.168.56.101"

    # copy ssh keys
    config.vm.provision "shell", inline: "mkdir -p /root/.ssh"
    config.vm.provision "shell", inline: "cat /vagrant/salt/key/known_hosts >> /root/.ssh/known_hosts"
    config.vm.provision "shell", inline: "cp /vagrant/salt/key/id_deployment /root/.ssh/id_rsa"
    config.vm.provision "shell", inline: "cp /vagrant/salt/key/id_deployment.pub /root/.ssh/id_rsa.pub"
    config.vm.provision "shell", inline: "chmod 0600 /root/.ssh/id_rsa"

    # install python-git (required for saltstack gitfs)
    config.vm.provision "shell", inline: "apt-get update"
    config.vm.provision "shell", inline: "apt-get -y install python-software-properties"
    config.vm.provision "shell", inline: "apt-add-repository ppa:pabelanger/zuul"
    config.vm.provision "shell", inline: "apt-get update"
    config.vm.provision "shell", inline: "apt-get -y install python-git"

    config.vm.provision :salt do |salt|
      salt.install_master = true
      salt.master_config = "salt/master"
      salt.minion_config = "salt/minion-api"
      salt.verbose = true

      salt.master_key = "salt/key/master.pem"
      salt.master_pub = "salt/key/master.pub"

      salt.minion_key = "salt/key/api.pem"
      salt.minion_pub = "salt/key/api.pub"

      salt.seed_master = {api: "salt/key/api.pub"}
    end

    # run salt/bootstrap
    config.vm.provision :shell, inline: "salt-run fileserver.update" # force refresh the gitfs states
    config.vm.provision :shell, inline: "echo 'Running salt.highstate... (may take several minutes)'; salt '*' state.highstate"
    config.vm.provision :shell, :path => "script/vagrant_api_bootstrap.sh"
  end

  config.vm.define :worker do |worker|
    config.vm.hostname = "worker"
    config.vm.network :private_network, ip: "192.168.56.102"

    # copy ssh keys
    config.vm.provision "shell", inline: "mkdir -p /root/.ssh"
    config.vm.provision "shell", inline: "cat /vagrant/salt/key/known_hosts >> /root/.ssh/known_hosts"
    config.vm.provision "shell", inline: "cp /vagrant/salt/key/id_deployment /root/.ssh/id_rsa"
    config.vm.provision "shell", inline: "cp /vagrant/salt/key/id_deployment.pub /root/.ssh/id_rsa.pub"
    config.vm.provision "shell", inline: "chmod 0600 /root/.ssh/id_rsa"

    # install python-git (required for saltstack gitfs)
    config.vm.provision "shell", inline: "apt-get update"
    config.vm.provision "shell", inline: "apt-get -y install python-software-properties"
    config.vm.provision "shell", inline: "apt-add-repository ppa:pabelanger/zuul"
    config.vm.provision "shell", inline: "apt-get update"
    config.vm.provision "shell", inline: "apt-get -y install python-git"

    config.vm.provision :salt do |salt|
      salt.install_master = true
      salt.master_config = "salt/master"
      salt.minion_config = "salt/minion-worker"
      salt.install_type = "git"
      salt.verbose = true

      salt.master_key = "salt/key/master.pem"
      salt.master_pub = "salt/key/master.pub"

      salt.minion_key = "salt/key/worker.pem"
      salt.minion_pub = "salt/key/worker.pub"

      salt.seed_master = {worker: "salt/key/worker.pub"}
    end

    # run salt/bootstrap
    config.vm.provision :shell, inline: "salt-run fileserver.update" # force refresh the gitfs states
    config.vm.provision :shell, inline: "echo 'Running salt.highstate... (may take several minutes)'; salt '*' state.highstate"
    config.vm.provision :shell, inline: "rabbitmq-plugins enable rabbitmq_management && service rabbitmq-server restart"
    config.vm.provision :shell, inline: "su - vagrant -c '~/api/bin/pip install -v flower'"
  end

end
