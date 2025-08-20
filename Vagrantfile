Vagrant.configure("2") do |config|
  # Use a more recent Ubuntu version
  config.vm.box = "ubuntu/focal64"
  
  # Configure VM settings
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "1024"
    vb.cpus = 1
  end

  config.vm.define "machine1" do |machine1|
    machine1.vm.network "private_network", ip: "192.168.56.10"
    machine1.vm.hostname = "weather-app-1"
    
    # Use relative path that works on any system
    if Vagrant::Util::Platform.windows?
      machine1.vm.synced_folder ".", "/vagrant", type: "virtualbox"
    else
      machine1.vm.synced_folder ".", "/vagrant"
    end
  end

  config.vm.define "machine2" do |machine2|
    machine2.vm.network "private_network", ip: "192.168.56.11"
    machine2.vm.hostname = "weather-app-2"
    
    # Use relative path that works on any system
    if Vagrant::Util::Platform.windows?
      machine2.vm.synced_folder ".", "/vagrant", type: "virtualbox"
    else
      machine2.vm.synced_folder ".", "/vagrant"
    end
  end

  # Provision both machines with basic setup
  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y curl wget
  SHELL
end
