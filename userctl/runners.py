# pylint: disable=W0613,C0111
"""
Runners for executing local and remote commands.
"""

from fabric import Connection


def create_instance(name, *args, **kwargs):
    """
    Returns a runner instance by the specified name.
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

    def run_command(self, cmd):
        raise NotImplementedError()


class FabricRunner(RunnerBase):
    """
    Command runner implemented using Fabric.
    """

    host = None
    config = None

    def post_initialize(self, *args, **kwargs):
        self.host = kwargs.get('host', None)
        self.config = kwargs.get('config', None)

    def run_command(self, cmd):
        with Connection(host=self.host, config=self.config) as conn:
            result = conn.sudo(cmd, hide=True)
            return result.stdout.strip()
