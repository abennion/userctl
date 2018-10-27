# pylint: disable=C0103,W0613
"""
Tasks for managing users implemented with Invoke.
"""
import os
from invoke import task
from invoke.exceptions import UnexpectedExit
from fabric import Connection

# TODO: improve passing of core arguments
# TODO: refactor methods for easier testing
# TODO: create factory for distribution specific methods
# TODO: create tests with mocks
# TODO: improve output and logging
# TODO: task for creating a sample config file
# TODO: complete documentation and readmes


def user_add(conn, user):
    """
    Creates a user and home directory.
    """
    cmd = "useradd -m -d /home/{0} -s /bin/bash {0}".format(user)
    try:
        conn.sudo(cmd)
    except UnexpectedExit as uex:
        # ignore if user exists (exit code 9)
        if uex.result.exited != 9:
            raise


def dir_exists(conn, dirname):
    """
    Returns True if the directory exists.
    """
    result = conn.sudo('[ ! -d "{}" ] || echo "1"'.format(dirname))
    return result.stdout.strip() == "1"


@task
def add_user(ctx, host, admin_user, admin_key_filename, user, public_key_filename):
    """
    Creates and configures a new user.
    """
    public_key = None
    with open(public_key_filename, 'r') as fp:
        public_key = fp.read().strip()
    with Connection(
        host=host,
        user=admin_user,
        connect_kwargs={'key_filename': admin_key_filename}
    ) as conn:
        user_add(conn, user)
        conn.sudo("usermod --lock {}".format(user))
        if not dir_exists(conn, "/home/{}/.ssh".format(user)):
            conn.sudo("mkdir /home/{}/.ssh".format(user))
        conn.sudo("chown -R {0}:{0} /home/{0}/.ssh".format(user))
        conn.sudo("chmod 700 /home/{0}/.ssh".format(user))
        if not dir_exists(conn, "/home/{}/.ssh/authorized_keys".format(user)):
            conn.sudo("touch /home/{}/.ssh/authorized_keys".format(user))
        conn.sudo("chown -R {0}:{0} /home/{0}/.ssh".format(user))
        conn.sudo("chmod 600 /home/{}/.ssh/authorized_keys".format(user))
        result = conn.sudo("cat /home/{}/.ssh/authorized_keys".format(user))
        if not public_key in result.stdout.strip():
            cmd = "bash -c \"echo '{0}' >> /home/{1}/.ssh/authorized_keys\""
            cmd = cmd.format(public_key, user)
            conn.sudo(cmd)


def get_users(conn):
    """
    Returns a list of users.
    """
    cmd = "cat /etc/passwd | grep '/home' | cut -d: -f1"
    result = conn.sudo(cmd, hide=True)
    return result.stdout.strip().split(os.linesep)


@task
def list_users(ctx, host, admin_user, admin_key_filename):
    """
    Prints a list of users.
    """
    with Connection(
        host=host,
        user=admin_user,
        connect_kwargs={'key_filename': admin_key_filename}
    ) as conn:
        users = get_users(conn)
        print(os.linesep.join(users))


@task
def delete_user(ctx, host, admin_user, admin_key_filename, user):
    """
    Deletes a user and the user's home directory.
    """
    with Connection(
        host=host,
        user=admin_user,
        connect_kwargs={'key_filename': admin_key_filename}
    ) as conn:
        conn.sudo("deluser --remove-home {}".format(user))
