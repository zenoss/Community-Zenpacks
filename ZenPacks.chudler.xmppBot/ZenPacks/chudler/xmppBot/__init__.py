import Globals
import os.path

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
from Products.CMFCore.DirectoryView import registerDirectory
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())

import sys
import transaction
from Products.ZenEvents import ActionRule
from Products.ZenModel import UserSettings
from Products.ZenModel.ZenPack import ZenPackBase
from Products.ZenUtils.Utils import zenPath

# give zenactions ActionType a new property so xmpp appears in the
# UI when selecting the Alert Rule type.
target = getattr(sys.modules['Products.ZenEvents'], 'ActionRule')
oldActionTypes = list(getattr(target, 'actionTypes', ('email', 'pager')))
oldActionTypes.append('xmpp')
newActionTypes = tuple(oldActionTypes)
setattr(target, 'actionTypes', newActionTypes)

# give ZenUsers the JabberID property.
target = getattr(sys.modules['Products.ZenModel'], 'UserSettings')
setattr(target, 'JabberId', '')

target = getattr(sys.modules['Products.ZenModel'], 'UserSettings').UserSettings
oldProperties = list(target.__dict__['_properties'])
oldProperties.append({'id':'JabberId', 'type':'string', 'mode':'w'})
newProperties = tuple(oldProperties)
setattr(target, '_properties', newProperties)

"""
# This simply will not work!
from Products.ZenUtils.ZCmdBase import ZCmdBase
dmd = ZCmdBase(noopts = True).dmd
#from Products.ZenUtils.ZenScriptBase import ZenScriptBase
#dmd = ZenScriptBase(connect=True).dmd
for user in cmd.dmd.ZenUsers.getAllUserSettings():
    if not user.hasProperty('JabberId'):
        #user.manage_addProperty('JabberId', '', 'string')
        user._setProperty('JabberId', '', 'string')

transaction.commit()
"""

class ZenPack(ZenPackBase):

    def install(self, app):
        ZenPackBase.install(self, app)
        configFileName = zenPath('etc', 'xmppBot.conf')
        if not os.path.exists(configFileName):
            configFile = open(configFileName, 'w')
            configFile.write('# populate this file by running $ZENHOME/bin/xmppBot genconf > $ZENHOME/etc/xmppBot.conf\n')
            configFile.close()

        # add the JabberId property to existing users
        for user in app.dmd.ZenUsers.getAllUserSettings():
            if not user.hasProperty('JabberId'):
                user.manage_addProperty('JabberId', '', 'string')
                user._setProperty('JabberId', '', 'string')
            try:
                user.getProperty('JabberId')
            except AttributeError:
                user.manage_addProperty('JabberId', '', 'string')
        transaction.commit()

    def remove(self, app, leaveObjects=False):

        # Remove the symlink to the bot daemon
        cdSymLink = zenPath('bin', 'xmppBot')
        if os.path.exists(cdSymLink):
            os.remove(cdSymLink)

        # call parent zenpack uninstall function
        ZenPackBase.remove(self, app, leaveObjects)

        # remove JabberID user propery
        for user in self.dmd.ZenUsers.getAllUserSettings():
            if user.hasProperty('JabberId'):
                user.manage_delProperty('JabberId')
        transaction.commit()
