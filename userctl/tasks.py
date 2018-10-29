# pylint: disable=C0103,W0613,C0111
"""
Tasks for managing users implemented with Invoke.
"""
from __future__ import print_function
from invoke import task
from .runners import create_instance as create_runner
from .users import create_instance as create_users
from textwrap import dedent

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


def get_platform(runner):
    """
    Returns the platform of the remote host.
    """
    # TODO move these to a helper module
    cmd = dedent("""\
        python - <<DOC
        from __future__ import print_function
        import platform
        print(platform.system())
        DOC
        """).strip()
    return runner.run_command(cmd).strip()


def get_distribution(runner):
    """
    Returns the distribution of the remote host.
    """
    cmd = dedent("""\
        python - <<DOC
        from __future__ import print_function
        import os
        import platform
        if platform.system() == 'Linux':
            try:
                supported_dists = platform._supported_dists + ('arch', 'alpine', 'devuan')
                distribution = platform.linux_distribution(supported_dists=supported_dists)[0].capitalize()
                if not distribution and os.path.isfile('/etc/system-release'):
                    distribution = platform.linux_distribution(supported_dists=['system'])[0].capitalize()
                    if 'Amazon' in distribution:
                        distribution = 'Amazon'
                    else:
                        distribution = 'OtherLinux'
            except:
                # FIXME: MethodMissing, I assume?
                distribution = platform.dist()[0].capitalize()
        else:
            distribution = None
        print(distribution)
        DOC
        """).strip()
    return runner.run_command(cmd).strip()


def get_distribution_version(runner):
    cmd = dedent("""\
        python - <<DOC
        from __future__ import print_function
        import os
        import platform
        if platform.system() == 'Linux':
            try:
                distribution_version = platform.linux_distribution()[1]
                if not distribution_version and os.path.isfile('/etc/system-release'):
                    distribution_version = platform.linux_distribution(supported_dists=['system'])[1]
            except:
                # FIXME: MethodMissing, I assume?
                distribution_version = platform.dist()[1]
        else:
            distribution_version = None
        print(distribution_version)
        DOC
        """).strip()
    return runner.run_command(cmd).strip()


def get_user_manager(ctx, host):
    runner = get_fabric_runner(ctx, host)
    platform = get_platform(runner)
    distribution = get_distribution(runner)
    print("platform: {}, distribution: {}".format(platform, distribution))
    kwargs = {
        'platform': platform,
        'distribution': distribution,
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
