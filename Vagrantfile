# -*- mode: ruby -*-
# vi: set ft=ruby :
Vagrant.require_version ">= 1.5"

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"
  config.ssh.forward_agent = true

  # Provider-specific configuration
  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--memory", "1024"]
  end

  config.vm.define :api do |api|
    config.vm.hostname = "api"
    config.vm.network :private_network, ip: "192.168.56.101"

    config.vm.provision :shell, :path => "vagrant/salt_dependencies.sh"
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
    config.vm.provision :shell, :path => "vagrant/mysql.sh"
    config.vm.provision :shell, :path => "vagrant/salt_bootstrap.sh"
    config.vm.provision :shell, :path => "vagrant/api_bootstrap.sh"
  end

  config.vm.define :worker do |worker|
    config.vm.hostname = "worker"
    config.vm.network :private_network, ip: "192.168.56.102"

    config.vm.provision :shell, :path => "vagrant/salt_dependencies.sh"
    config.vm.provision :salt do |salt|
      salt.install_master = true
      salt.master_config = "salt/master"
      salt.minion_config = "salt/minion-worker"
      salt.verbose = true

      salt.master_key = "salt/key/master.pem"
      salt.master_pub = "salt/key/master.pub"
      salt.minion_key = "salt/key/worker.pem"
      salt.minion_pub = "salt/key/worker.pub"

      salt.seed_master = {worker: "salt/key/worker.pub"}
    end

    # run salt/bootstrap
    config.vm.provision :shell, :path => "vagrant/salt_bootstrap.sh"
    config.vm.provision :shell, :path => "vagrant/worker_bootstrap.sh"
  end

end
