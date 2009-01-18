import Globals
from Products.ZenModel.migrate.Migrate import Version
from ZenPacks.example.Techniques.TopLevel import manage_addTopLevel

import logging
log = logging.getLogger("zen.migrate")


class InstallTopLevel:
    version = Version(1, 0, 0)

    def migrate(self, pack):
        if not getattr(pack.dmd, 'TopLevel', None):
            log.info("Installing TopLevel object.")
            manage_addServiceNow(pack.dmd)
        else:
            log.info("TopLevel object already exists.")


InstallServiceNow()
