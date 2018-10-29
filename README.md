# userctl

## Overview

Userctl is a sample user management CLI written in Python using
[Invoke](https://github.com/pyinvoke/invoke) and
[Fabric](https://github.com/fabric/fabric). Userctl lets you:

* Add, list, or delete users on a remote host

A second solution is provided as an [Ansible](https://www.ansible.com/)
playbook. The code and documentation are [here](ansible).

Both Fabric and Ansible use the
[Paramiko](https://github.com/paramiko/paramiko) SSH library.

## Limitation of Scope

The solution is limited to the minimum functionality necessary to satisfy the
requirements of the assignment. For example, Windows and most Unix-like
platforms are not currently supported.

## Prerequisites

The user should be configured with sufficient permissions to execute commands
using sudo on the remote host via SSH, `ssh-agent`, and `.ssh/config`. It is
possible to pass alternative SSH credentials via the CLI, but that's not
documented here.

## Installation

```bash
git clone https://github.com/abennion/userctl.git
# create python virtual environment and install the component locally
make setup && make install
source venv/bin/activate
```

Or from PIP:

```bash
pip install -e git+https://github.com/abennion/userctl#egg=userctl
```

## Usage

```bash
userctl --help
userctl --help list-users
userctl list-users -h foo.example.com
userctl --help add-user
userctl add-user -h foo.example.com -u jdoe -p ~/.ssh/jdoe/id_rsa.pub
userctl --help delete-user
userctl delete-user -h foo.example.com -u jdoe
```