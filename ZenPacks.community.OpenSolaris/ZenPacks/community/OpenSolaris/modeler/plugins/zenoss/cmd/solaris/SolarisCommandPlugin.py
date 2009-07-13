from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin
class SolarisCommandPlugin(CommandPlugin):
    """
    A command plugin for solaris that is used by devices in Server/Cmd and
    Server/SSH/Solaris
    """


    def condition(self, device, log):
        """
        If the device resides under the Server/Cmd device class, then only run
        this plugin if uname has been previously modeled as "SunOS". Otherwise
        always run this plugin.
        """
        path = device.deviceClass().getPrimaryUrlPath()

        if path.startswith("/zport/dmd/Devices/Server/Cmd"):
            result = device.os.uname == 'SunOS'
        else:
            result = True

        return result
