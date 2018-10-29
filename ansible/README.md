# userctl/ansible

## Overview

A simple Ansible playbook for managing users. The playbook:

* Adds a user, including public key, on a remote host
* Lists users on a remote host
* Deletes the user from the remote host

To run the playbook, you may need to:

* Add the host to `/etc/ansible/hosts`
* Add the host to `~/.ssh/config`

## Usage

If necessary generate new SSH keys. For example:

```bash
mkdir -p ~/.ssh/johndoe
chmod 700 -R ~/.ssh/johndoe
ssh-keygen -f ~/.ssh/johndoe/id_rsa -t rsa -b 4096 \
    -C "johndoe@example.com" -N ''
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

The execute the playbook:

```bash
ansible-playbook webservers.yml -v
```