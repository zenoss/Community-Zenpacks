import sys

"""Find and load plugins for the jabber bot"""

class Plugin(object):

    capabilities = []

    def __repr__(self):
        return '<%s %r>' % (
            self.__class__.__name__,
            self.capabilities
        )

def loadPlugins(plugins):
    for plugin in plugins:
        __import__(plugin, None, None, [''])


def initPluginSystem(cfg):
    if not cfg['pluginPath'] in sys.path:
        sys.path.insert(0, cfg['pluginPath'])
    loadPlugins(cfg['plugins'])
    

def findPlugins():
    return Plugin.__subclasses__()


_instances = {}

def getPluginsByCapability(capability):
    """Find plugins that have registered the capability.
       _instances will keep their instance for subsiquent calls
    """
    result = []
    for plugin in Plugin.__subclasses__():
        if capability in plugin.capabilities:
            if not plugin in _instances:
                _instances[plugin] = plugin()
            result.append(_instances[plugin])
    return result

