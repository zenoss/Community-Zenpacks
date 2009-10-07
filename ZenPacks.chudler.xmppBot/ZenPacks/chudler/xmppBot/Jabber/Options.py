from optparse import OptionParser, OptionError

class Options(OptionParser):

    def __init__(self, **kwargs):
        OptionParser.__init__(self, **kwargs)

    def error(self, message):
        result = message
        if not message:
            result = 'An Error Occured.  Something wrong with your arguments\n'
        result = result + '\n' + self.get_usage()
        raise OptionError, result

    def exit(self, status = 0, message = None):
        return message

    def print_usage(self, file = None):
        raise OptionError, self.get_usage()
        return None

    def print_help(self, file = None):
        raise OptionError(self.format_help(), '-h')
        return None

    def help(self):
        return self.format_help()
