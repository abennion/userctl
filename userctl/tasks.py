# pylint: disable=C0103,W0613
"""
Tasks for managing users implemented with Invoke.
"""
from __future__ import print_function
from invoke import task
from .runners import create_instance as create_runner
from .users import create_instance as create_user

# TODO: improve passing of core arguments
# TODO: refactor methods for easier testing
# TODO: detect the remote distribution
# TODO: create factory for distribution specific methods
# TODO: create tests with mocks
# TODO: improve output and logging
# TODO: task for creating a sample config file
# TODO: complete documentation and readmes


@task
def add_user(ctx, host, admin_user, admin_key_filename, user, public_key_filename):
    """
    Creates and configures a new user.
    """
    kwargs = {
        'host': host,
        'admin_user': admin_user,
        'admin_key_filename': admin_key_filename,
    }
    runner = create_runner('fabric', **kwargs)
    kwargs = {
        'platform': 'Linux',
        'distribution': 'Ubuntu',
        'runner': runner,
    }
    user = create_user(**kwargs)
    user.create_user(user)


@task
def list_users(ctx, host, admin_user, admin_key_filename):
    """
    Prints a list of users.
    """
    kwargs = {
        'host': host,
        'admin_user': admin_user,
        'admin_key_filename': admin_key_filename,
    }
    runner = create_runner('fabric', **kwargs)
    kwargs = {
        'platform': 'Linux',
        'distribution': 'Ubuntu',
        'runner': runner,
    }
    user = create_user(**kwargs)
    print(user.list_users())


@task
def delete_user(ctx, host, admin_user, admin_key_filename, user):
    """
    Deletes a user and the user's home directory.
    """
    # kwargs = {
    #     'platform': 'Linux',
    #     'distribution': 'Ubuntu',
    #     'host': host,
    #     'admin_user': admin_user,
    #     'admin_key_filename': admin_key_filename
    # }
    # user = create_user(**kwargs)
    # user.delete_user(user)
