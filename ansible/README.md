# userctl/ansible

## Overview

A simple Ansible playbook for managing users. The playbook:

* Adds a users on a remote host including public keys
* Lists users on a remote host
* Deletes users from the remote host

To run the playbook, you may need to:

* Add the hosts to `~/.ssh/config`

## Usage

Add the target hosts to `/etc/ansible/hosts`:

```ini
[webservers]
foo.example.com   ansible_user=ubuntu
bar.example.com   ansible_user=centos
```

If necessary generate new SSH keys. For example:

```bash
mkdir -p ~/.ssh/johndoe
chmod 700 -R ~/.ssh/johndoe
ssh-keygen -f ~/.ssh/johndoe/id_rsa -t rsa -b 4096 -N ''
```

Variables can be passed into Ansible in a variety of ways, but two default
user accounts are defined under
[roles/common/defaults/main.yml](roles/common/defaults/main.yml):

```yaml
users:
  johndoe:
    name: johndoe
    public_key_filename: ~/.ssh/johndoe/id_rsa.pub
  janedoe:
    name: janedoe
    public_key_filename: ~/.ssh/janedoe/id_rsa.pub
```

To execute the playbook:

```bash
ansible-playbook webservers.yml -v
```