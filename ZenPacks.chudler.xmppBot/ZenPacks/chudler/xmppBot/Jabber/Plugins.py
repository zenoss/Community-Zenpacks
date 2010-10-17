import sys, logging

"""Find and load plugins for the jabber bot"""

class Plugin(object):

    capabilities = []
    threadsafe = False
    private = True

    def __init__(self, jabberClient, **kw):
        self.jabberClient = jabberClient

    def __repr__(self):
        return '<%s %r>' % (
            self.__class__.__name__,
            self.capabilities
        )

def loadPlugins(plugins, jabberClient):
    logger = logging.getLogger('zen.xmppBot')
    for plugin in plugins:
        logger.debug('PLUGINS: Importing Plugin %s' % plugin)
        __import__(plugin, None, None, [''])

    # initialize every plugin now.  Don't wait until it is used
    for plugin in Plugin.__subclasses__():
        if not plugin in _instances:
            logger.debug('PLUGINS: Initializing plugin %s' % plugin)
            pluginInstance = plugin(jabberClient=jabberClient) 
            if not pluginInstance.threadsafe:
                logger.debug('PLUGINS: Plugin %s is not threadsafe.' % plugin)
                _instances[plugin] = pluginInstance

def initPluginSystem(pluginPath, plugins, jabberClient):
    if not pluginPath in sys.path:
        sys.path.insert(0, pluginPath)
    loadPlugins(plugins, jabberClient)

def findPlugins():
    return Plugin.__subclasses__()

_instances = {}

def getPluginsByCapability(capability, jabberClient):
    """Find plugins that have registered the capability.
       _instances will keep their instance for subsiquent calls
    """
    result = []
    for plugin in Plugin.__subclasses__():
        if capability in plugin.capabilities:
            if not plugin in _instances:
                pluginInstance = plugin(jabberClient=jabberClient)
                # threaded plugins should not be singletons
                if not pluginInstance.threadsafe:
                    _instances[plugin] = pluginInstance
            else:
                pluginInstance = _instances[plugin]
            result.append(pluginInstance)
    return result
