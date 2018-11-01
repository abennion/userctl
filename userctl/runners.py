# pylint: disable=W0613,C0111
"""
Runners for executing shell commands.
"""
from socket import gethostbyname
from ipaddress import IPv4Address


def create_instance(name, *args, **kwargs):
    """
    Runner factory method.
    """
    classes = {
        'fabric': FabricRunner
    }
    runner_class = classes.get(name.lower(), FabricRunner)
    if runner_class:
        return runner_class(*args, **kwargs)
    raise NotImplementedError()


class RunnerBase(object):
    def __init__(self, *args, **kwargs):
        self.post_initialize(*args, **kwargs)

    def post_initialize(self, *args, **kwargs):
        pass

    def run_command(self, cmd, *args, **kwargs):
        raise NotImplementedError()


class FabricRunner(RunnerBase):
    """
    Command runner implemented using Fabric.
    """
    connection = None

    def post_initialize(self, *args, **kwargs):
        self.connection = kwargs.get('connection', None)

    # TODO we could check loopback, but probably better to pass a flag

    # from socket import gethostbyname
    # ipaddr = gethostbyname("localhost")
    # addr = ipaddress.IPv4Address(ipaddr)
    # addr.is_loopback

    def run_command(self, cmd, *args, **kwargs):
        fabric_kwargs = kwargs.get('fabric_kwargs', {})
        return self.connection.sudo(cmd, **fabric_kwargs).stdout
