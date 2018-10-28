# pylint: disable=W0613
"""
User management module.
"""


def create_instance(*args, name='generic', **kwargs):
    """
    Factory method that returns an instance derived from Users.
    """
    # TODO: get class by platform and distribution
    classes = {
        'generic': Users
    }
    runner_class = classes.get(name.lower(), None)
    if runner_class:
        return runner_class(*args, **kwargs)
    raise NotImplementedError()


class Users(object):
    """
    Manage users on a generic Linux host.
    """

    platform = 'Generic'
    distribution = None
    runner = None

    def __init__(self, *args, **kwargs):
        """
        Constructs the instance.
        """
        self.post_initialize(*args, **kwargs)

    def post_initialize(self, *args, **kwargs):
        """
        Initializes a user instance for generic hosts.
        """
        print(kwargs)
        self.runner = kwargs['runner']

    def run_command(self, cmd):
        """
        Executes a shell command.
        """
        return self.runner.run_command(cmd)

    def dir_exists(self, dirname):
        """
        Returns True if the directory exists.
        """
        text = self.runner.run_command(
            '[ ! -d "{}" ] || echo "1"'.format(dirname))
        return text.strip() == "1"

    def create_user_useradd(self, name):
        """
        Create user using useradd.
        """
        cmd = "useradd -m -d /home/{0} -s /bin/bash {0}".format(name)
        self.run_command(cmd)
        # except UnexpectedExit as uex:
        #     # ignore if user exists (exit code 9)
        #     if uex.result.exited != 9:
        #         raise

    def list_users_passwd(self):
        """
        List users using passwd.
        """
        cmd = "cat /etc/passwd | grep '/home' | cut -d: -f1"
        return self.runner.run_command(cmd)

    def delete_user_deluser(self, name):
        """
        Delete user using deluser.
        """
        cmd = "deluser --remove-home {}".format(name)
        self.runner.run_command(cmd)

    def create_user(self, name):
        """
        Create a user.
        """
        self.create_user_useradd(name)
        # conn.sudo("usermod --lock {}".format(user))
        # if not dir_exists(conn, "/home/{}/.ssh".format(user)):
        #     conn.sudo("mkdir /home/{}/.ssh".format(user))
        # conn.sudo("chown -R {0}:{0} /home/{0}/.ssh".format(user))
        # conn.sudo("chmod 700 /home/{0}/.ssh".format(user))
        # if not dir_exists(conn, "/home/{}/.ssh/authorized_keys".format(user)):
        #     conn.sudo("touch /home/{}/.ssh/authorized_keys".format(user))
        # conn.sudo("chown -R {0}:{0} /home/{0}/.ssh".format(user))
        # conn.sudo("chmod 600 /home/{}/.ssh/authorized_keys".format(user))
        # result = conn.sudo("cat /home/{}/.ssh/authorized_keys".format(user))
        # if not public_key in result.stdout.strip():
        #     cmd = "bash -c \"echo '{0}' >> /home/{1}/.ssh/authorized_keys\""
        #     cmd = cmd.format(public_key, user)
        #     conn.sudo(cmd)

    def list_users(self):
        """
        List users.
        """
        return self.list_users_passwd()

    def delete_user(self, name):
        """
        Delete a user.
        """
        self.delete_user_deluser(name)
