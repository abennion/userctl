# pylint: disable=C0103,C0111
from fabric.config import Config
from fabric.main import Fab
from .executor import FabExecutor
from . import __version__ as version


class UserCtl(Fab):
    def load_collection(self):
        # unless set by the user, update the search root to within our
        # package module
        if self.args['search-root'].value is None:
            self.args['search-root'].value = "userctl"
        super(UserCtl, self).load_collection()


program = UserCtl(
    name="userctl",
    version=version,
    executor_class=FabExecutor,
    config_class=Config
)
