# pylint: disable=W0613,C0111
"""
User managers implemented for different host environments.
"""
from .utils import load_platform_subclass


class Users(object):
    """
    User manager for a generic Linux host.
    """

    PASSWD_USERNAME = 0
    PASSWD_PASSWORD = 1
    PASSWD_UID = 2
    PASSWD_GID = 3
    PASSWD_COMMENT = 4
    PASSWD_HOME = 5
    PASSWD_SHELL = 6

    platform = 'Linux'
    distribution = None
    runner = None

    def __new__(cls, *args, **kwargs):
        return load_platform_subclass(Users, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        self.post_initialize(*args, **kwargs)

    def post_initialize(self, *args, **kwargs):
        self.runner = kwargs.get('runner', None)

    def run_command(self, cmd):
        return self.runner.run_command(cmd)

    def dir_exists(self, dirname):
        text = self.runner.run_command(
            '[ ! -d "{}" ] || echo "1"'.format(dirname))
        return text.strip() == "1"

    def create_user_useradd(self, name):
        # TODO check if the user already exists
        cmd = "useradd -m -d /home/{0} -s /bin/bash {0}".format(name)
        return self.run_command(cmd)

    def list_users_passwd(self):
        cmd = "getent passwd"
        text = self.runner.run_command(cmd)
        users = {}
        for line in text.strip().split('\n'):
            parts = line.split(':')
            if '/home' in parts[self.PASSWD_HOME]:
                # this doesn't really need to be a dict
                users[parts[self.PASSWD_USERNAME]] = {
                    'uid': parts[self.PASSWD_UID],
                    'comment': parts[self.PASSWD_COMMENT],
                    'home': parts[self.PASSWD_HOME]
                }
        return users

    def delete_user_userdel(self, name):
        # cmd = "deluser --remove-home {}".format(name)
        cmd = "userdel -r {}".format(name)
        return self.runner.run_command(cmd)

    def create_user(self, name, public_key):
        """
        Creates a new user and adds an authorized key.

        The following commands are run on the host via Fabric and SSH, unlike
        Ansible, which executes Python on the host.

        https://github.com/ansible/ansible-modules-core/blob/devel/system/user.py
        """
        self.create_user_useradd(name)
        self.run_command("usermod --lock {}".format(name))
        if not self.dir_exists("/home/{}/.ssh".format(name)):
            self.run_command("mkdir /home/{}/.ssh".format(name))
        self.run_command("chown -R {0}:{0} /home/{0}/.ssh".format(name))
        self.run_command("chmod 700 /home/{0}/.ssh".format(name))
        if not self.dir_exists("/home/{}/.ssh/authorized_keys".format(name)):
            self.run_command(
                "touch /home/{}/.ssh/authorized_keys".format(name))
        self.run_command("chown -R {0}:{0} /home/{0}/.ssh".format(name))
        self.run_command(
            "chmod 600 /home/{}/.ssh/authorized_keys".format(name))
        result = self.run_command(
            "cat /home/{}/.ssh/authorized_keys".format(name))
        if not public_key in result.strip():
            cmd = "bash -c \"echo '{0}' >> /home/{1}/.ssh/authorized_keys\""
            cmd = cmd.format(public_key, name)
            self.run_command(cmd)

    def list_users(self):
        users = self.list_users_passwd()
        res = ""
        for username, details in users.items():
            res += "username: {}, uid: {}, comment: {}\n".format(
                username, details['uid'], details['comment'])
        return res.strip()

    def delete_user(self, name):
        self.delete_user_userdel(name)


class CentOsUsers(Users):
    """
    Demonstrates a platform specific subclass.
    """

    platform = 'Linux'
    distribution = "Centos linux"

    def list_users(self):
        users = self.list_users_passwd()
        # res = "{}, {}\n".format(self.platform, self.distribution).lower()
        res = "using the centos users class\n"
        for username, details in users.items():
            res += "username: {}, uid: {}, comment: {}\n".format(
                username, details['uid'], details['comment'])
        return res.strip()
