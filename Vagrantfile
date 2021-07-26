Vagrant.configure("2") do |config|
  config.vm.define "app" do |app|  
    app.vm.box = "hashicorp/bionic64"
    app.vm.network "private_network", ip: "192.168.10.100"
    app.hostsupdater.aliases = ["development.local"]
    app.vm.synced_folder ".", "/home/vagrant/project"
    app.vm.provision "shell", path: "provision.sh"
  end
end
