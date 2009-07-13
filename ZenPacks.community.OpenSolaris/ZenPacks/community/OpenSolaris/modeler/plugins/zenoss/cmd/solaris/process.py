from pprint import pformat
from Products.DataCollector.ProcessCommandPlugin import ProcessCommandPlugin

class process(ProcessCommandPlugin):
    """
    Solaris command plugin for parsing ps command output and modeling processes.
    """

    command = 'ps -eo args'
    compname = "os"
    relname = "processes"
    modname = "Products.ZenModel.OSProcess"

    def condition(self, device, log):
        """
        If the device resides under the Server/SSH device class, then always
        run this plugin.  Otherwise only run this plugin if uname has been
        previously modeled as "Linux".
        """
        path = device.deviceClass().getPrimaryUrlPath()

        if path.startswith("/zport/dmd/Devices/Server/SSH"):
            result = True
        else:
            result = device.os.uname == 'Solaris'

        return result


    # Override ProcessCommandPlugin process
    def process(self, device, results, log):

        log.info('Collecting process information for device %s' % device.id)
        relMap = self.relMap()

        # Skip the first line as its a header
        for line in results.splitlines()[1:]:

            words = line.split()
            om = self.objectMap()
            om.procName=words[0]
            om.parameters= " ".join(words[1:])
            relMap.append(om)

       # log.debug("First three modeled processes:\n%s" %
       #         pformat(relMap.maps[:3]))
        log.debug(relMap)
        return relMap
