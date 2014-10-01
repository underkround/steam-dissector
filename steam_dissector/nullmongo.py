
#
# NullObject-style replacement for pymongo
#

class NullCollection(object):

    def remove(self, *args, **kwargs):
        pass

    def insert(self, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        pass

    def find_one(self, *args, **kwargs):
        return None
