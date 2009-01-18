from Globals import InitializeClass
from OFS.SimpleItem import SimpleItem
from AccessControl import ClassSecurityInfo
from Products.ZenModel.ZenModelItem import ZenModelItem

def manage_addTopLevel(context, id='TopLevel', REQUEST=None):
    """
    Adds a TopLevel object to the context.
    """
    toplevel = TopLevel(id)
    context._setObject(id, toplevel)
    if REQUEST is not None:
        REQUEST.RESPONSE.redirect(context.absolute_url() + '/manage_main')


class TopLevel(ZenModelItem, SimpleItem):

    portal_type = meta_type = "TopLevel"

    security = ClassSecurityInfo()

    customProperty = "default value"

    _properties = (
        {'id':'customProperty', 'type':'string'},
    )


    def manage_editProperties(self, customProperty=None, REQUEST=None):
        """
        Allows editing of the TopLevel object.
        """
        if customProperty:
            self.customProperty = customProperty

        if REQUEST:
            REQUEST['message'] = "TopLevel Settings Saved"
            return self.callZenScreen(REQUEST)


InitializeClass(TopLevel)
