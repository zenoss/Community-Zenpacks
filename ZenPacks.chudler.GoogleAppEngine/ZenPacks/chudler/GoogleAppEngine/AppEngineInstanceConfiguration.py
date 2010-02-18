from twisted.spread import pb

class AppEngineInstanceConfiguration(pb.Copyable, pb.RemoteCopy):

    def __init__(self, id, user, password):
        self.id=id
        self.user=user
        self.password=password

    def __eq__(self, target):
        if not target:
            return False
        if not isinstance( target, AppEngineInstanceConfiguration ):
            return False
        return self.id==target.id

    def __ne__(self,target):
        return not self.__eq__( target )

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return '%s (%s/******)' % (self.id, self.user)

pb.setUnjellyableForClass( AppEngineInstanceConfiguration,
                           AppEngineInstanceConfiguration )
