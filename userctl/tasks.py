# pylint: disable=C0103,W0613,C0111
"""
Tasks for managing users implemented with Invoke.
"""
from __future__ import print_function
from invoke import task
from .runners import create_instance as create_runner
from .users import create_instance as create_users

# TODO: refactor methods for easier testing
# TODO: improve output and logging
# TODO: task for creating a sample config file
# TODO: complete documentation and readmes


def get_fabric_runner(ctx, host):
    # TODO: this could be better since we're using fabric.config already
    kwargs = {
        'host': host,
        'user': ctx.user,
        'port': ctx.port,
        'config': ctx.config,
        'gateway': ctx.gateway,
        'forward_agent': ctx.forward_agent,
        'connect_timeout': ctx.timeouts,
        'connect_kwargs': ctx.connect_kwargs,
    }
    return create_runner('fabric', **kwargs)


def get_users(ctx, host, runner):
    # TODO determine the host's platform and distribution
    kwargs = {
        'platform': 'Linux',
        'distribution': 'Ubuntu',
        'runner': runner,
    }
    return create_users(**kwargs)


@task
def add_user(ctx, host, user, public_key_filename):
    """
    Creates a new user on the specified host.
    """
    public_key = None
    with open(public_key_filename, 'r') as f:
        public_key = f.read().strip()
    runner = get_fabric_runner(ctx, host)
    users = get_users(ctx, host, runner)
    print(users.create_user(user, public_key))


@task
def list_users(ctx, host):
    """
    Lists users on the specified host.
    """
    runner = get_fabric_runner(ctx, host)
    users = get_users(ctx, host, runner)
    print(users.list_users())


@task
def delete_user(ctx, host, user):
    """
    Deletes a user on the specified host.
    """
    runner = get_fabric_runner(ctx, host)
    users = get_users(ctx, host, runner)
    print(users.delete_user(user))
