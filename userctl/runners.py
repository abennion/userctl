# pylint: disable=W0613
"""
Command runners.
"""
from fabric import Connection


def create_instance(name, *args, **kwargs):
    """
    Factory method that returns an instance derived from RunnerBase.
    """

    classes = {
        'fabric': FabricRunner
    }

    runner_class = classes.get(name.lower(), None)
    if runner_class:
        return runner_class(*args, **kwargs)
    raise NotImplementedError()


class RunnerBase(object):
    """
    Base class for command runners.
    """

    def __init__(self, *args, **kwargs):
        """
        Constructs the class.
        """
        self.post_initialize(*args, **kwargs)

    def post_initialize(self, *args, **kwargs):
        """
        Initialize the class.
        """
        pass

    def run_command(self, cmd):
        """
        Returns the result of the specified command.
        """
        raise NotImplementedError()


class FabricRunner(RunnerBase):
    """
    Fabric command runner.
    """

    # TODO: provide more authentication options

    host = None
    admin_user = None
    admin_key_filename = None

    def post_initialize(self, *args, **kwargs):
        """
        Initializes the class.
        """
        self.host = kwargs['host']
        self.admin_user = kwargs['admin_user']
        self.admin_key_filename = kwargs['admin_key_filename']

    def run_command(self, cmd):
        """
        Runs a shell command using Fabric.
        """
        with Connection(
            host=self.host,
            user=self.admin_user,
            connect_kwargs={'key_filename': self.admin_key_filename}
        ) as conn:
            result = conn.sudo(cmd, hide=True)
            return result.stdout.strip()
