# from invoke import Argument, Collection, Program
from invoke import Collection, Program
from . import tasks
from . import __version__ as version


class UserCtl(Program):
    def core_args(self):
        core_args = super(UserCtl, self).core_args()
        return core_args


program = UserCtl(
    name="userctl",
    version=version,
    namespace=Collection.from_module(tasks)
)
