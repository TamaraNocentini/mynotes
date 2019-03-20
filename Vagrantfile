# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"
  config.vm.network "private_network", ip: "192.168.33.10"

  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y build-essential postgresql-10 libpq-dev python3-venv python3 python3-dev python3-wheel moreutils tree

    sudo -iu postgres createuser my_notes ||:
    sudo -iu postgres createdb -O my_notes my_notes ||:

    echo 'vagrant  vagrant  my_notes' >> /etc/postgresql/10/main/pg_ident.conf
    sed -i '/TYPE/a local  my_notes  my_notes    peer map=vagrant' /etc/postgresql/10/main/pg_hba.conf
    systemctl reload postgresql
  SHELL
end
