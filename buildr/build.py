

class Build(object):

    def __call__(self):
        print "What's my name?!", type(self).__name__
