import Globals
import os
from Products.CMFCore.DirectoryView import registerDirectory

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

from Products.ZenModel.ZenPack import ZenPack as Base

class ZenPack(Base):
    packZProperties = [
        ("zAMQPPort",        5672,     'int'), # 5672 is the default AMQP port
        ("zAMQPUsername",    '',       'string'),
        ("zAMQPPassword",    '',       'string'),
        ('zAMQPVirtualHost', '/',      'string'),
        ('zAMQPQueue',       'zenoss', 'string'),
        ('zAMQPIgnore',      True,     'boolean'),
    ]

    def install(self, app):
        Base.install(self, app)
        self.migrate()

    def upgrade(self, app):
        Base.upgrade(self, app)
        self.migrate()
