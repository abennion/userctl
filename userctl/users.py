# pylint: disable=W0613,C0111
"""
User managers implemented for different host environments.
"""


def create_instance(*args, **kwargs):
    """
    Factory method that returns an instance derived from Users.
    """
    platform = kwargs.get('platform', None)
    distribution = kwargs.get('distribution', None)
    name = "{}-{}".format(platform, distribution)
    classes = {
        'linux-generic': Users
    }
    runner_class = classes.get(name.lower(), Users)
    if runner_class:
        return runner_class(*args, **kwargs)
    raise NotImplementedError()


class Users(object):
    """
    User manager for a generic Linux host.

    Ansible user module: https://github.com/ansible/ansible-modules-core/blob/devel/system/user.py.
    """

    runner = None

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
        cmd = "cat /etc/passwd | grep '/home' | cut -d: -f1"
        return self.runner.run_command(cmd)

    def delete_user_deluser(self, name):
        cmd = "deluser --remove-home {}".format(name)
        return self.runner.run_command(cmd)

    def create_user(self, name, public_key):
        # TODO: study the ansible user module
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
        return self.list_users_passwd()

    def delete_user(self, name):
        self.delete_user_deluser(name)
