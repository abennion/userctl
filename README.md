# userctl

User management solutions implemented as a CLI in Python and with Ansible.

The [Fabric](https://github.com/fabric/fabric) and
[Ansible](https://www.ansible.com/) both provide CLIs that can be used to
manage users. Fabric and Ansible both utilize the
[Paramiko](https://github.com/paramiko/paramiko) SSH library.

## Limitations

The scope of the solution is limited to the minimum necessary to fulfill the
assignment.

## Installation

```bash
pip install -e git+https://github.com/abennion/userctl#egg=userctl
userctl --help
```

## Development Environment

```bash
# create python virtual environment and install the component locally
make setup && make install
# clean up
make clean
```

## Usage

TODO: ssh configuration

```bash

```

## Design Notes

* Ansible [user](https://github.com/ansible/ansible-modules-core/blob/devel/system/user.py) module

## User Configuration Using Ansible

