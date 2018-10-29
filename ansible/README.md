# userctl/ansible

## Overview

A simple Ansible playbook for managing users. The playbook:

* Adds a user, including public key, on a remote host
* Lists users on a remote host
* Deletes the user from the remote host

To run the playbook, you may need to:

* Add the host to `/etc/ansible/hosts`
* Add the host to `~/.ssh/config`

Variables can be passed into Ansible in a variety of ways, but two default
user accounts are defined under
[roles/common/defaults/main.yml](roles/common/defaults/main.yml):

```yaml
users:
  johndoe:
    name: johndoe
    public_key_filename: ~/.ssh/fakeuser5/id_rsa.pub
  janedoe:
    name: janedoe
    public_key_filename: ~/.ssh/fakeuser5/id_rsa.pub
```

## Usage

```bash
cd userctl/ansible
ansible-playbook webservers.yml -v
```