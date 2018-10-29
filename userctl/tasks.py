# pylint: disable=C0103,W0613,C0111
"""
Tasks for managing users implemented with Invoke.
"""
from __future__ import print_function
from invoke import task
from .utils import get_fabric_runner
from .users import Users

# TODO: refactor methods for easier testing
# TODO: improve output and logging
# TODO: task for creating a sample config file
# TODO: complete documentation and readmes


def get_user_manager(ctx, host):
    runner = get_fabric_runner(ctx, host)
    return Users(**{'runner': runner})


@task
def add_user(ctx, host, user, public_key_filename):
    """
    Creates a new user on the specified host.
    """
    public_key = None
    with open(public_key_filename, 'r') as f:
        public_key = f.read().strip()
    users = get_user_manager(ctx, host)
    users.create_user(user, public_key)
    print("user added")


@task
def list_users(ctx, host):
    """
    Lists users on the specified host.
    """
    users = get_user_manager(ctx, host)
    print(users.list_users())


@task
def delete_user(ctx, host, user):
    """
    Deletes a user on the specified host.
    """
    users = get_user_manager(ctx, host)
    users.delete_user(user)
    print("user deleted")
