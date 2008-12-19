
__doc__="vmware Virtual Machines Zen Pack"

import Globals
import os.path

# If the ZenPack contains a skins directory it needs to be registered when
# the ZenPack module is loaded.
from Products.CMFCore.DirectoryView import registerDirectory


registerDirectory('skins', globals())

# When a user creates a ZenPack through the Zenoss Create New ZenPack
# command in the UI the ZenPack that's created is an instance of
# Products.ZenModel.ZenPack.Zenpack.  If this file contains a class
# named ZenPack (which should inherit from Products.ZenModel.ZenPack.ZenPack)
# then when it is installed it will create an instance of this class instead.
# This is useful if the ZenPack needs to perform actions like creating
# zProperties, adding users, etc when it is installed (and removing those
# things when it is removed.)  Many ZenPacks will not need to define 
# a ZenPack class here and will be fine with the base ZenPack class.
from Products.ZenModel.ZenPack import ZenPackBase


# If you wish to provide new Zope model object classes with your ZenPack
# then those classes need to be registered with Zope.  HelloWorld is a new
# class that can be managed via the Zope management interface (zmi.)
import ZenPacks.vmware.VirtualMachines
def initialize(registrar):
	registrar.registerClass(
		VirtualMachine.VirtualMachine,
		permission='Add DMD Objects',
	)

# If you want to distribute python modules with your zenpack they are best
# put in a lib subdirectory.  Make sure your subdirectory has an __init__.py
# file so it will be treated as a module.  You also need to include lines
# such as those below to add the subdir to the python path:

# import sys
# zenhome = os.environ['ZENHOME']
# sys.path.append(os.path.join(zenhome, 'Products', 'HelloWorldZenPack', 'lib'))
