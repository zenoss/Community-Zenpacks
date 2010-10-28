################################################################################
#
# This program is part of the DellEqualLogicMon Zenpack for Zenoss.
# Copyright (C) 2010 Eric Enns.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

class DellEqualLogicComponent:

    def statusString(self, status=None):
        """
        Return the status string
        """
        return self.state or 'Unknown'

