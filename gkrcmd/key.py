from gkrcmd import gkrlib
import fnmatch

import logging
def log(): return logging.getLogger(__name__)

class Key(dict):
    
    # expected: id, keyring
    def __init__(self, **kwargs):
        dict.__init__(self)
        self.update(**kwargs)
        self.sep = "-----------------------------------------------------------\n"
    
    def __repr__(self):
        return self.fmt()
    
    def __eq__(self, other):
        return (self.url() == other.url())
    
    def update(self, **kwargs):
        for key,value in kwargs.items():
            self[key] = value
    
    def id(self):
        return self["id"]
    
    def keyring(self):
        return self["keyring"]
    
    def name(self):
        return gkrlib.get_key_info(self.keyring().id(), self.id())["name"]
    
    def secret(self):
        return gkrlib.get_key_info(self.keyring().id(), self.id())["secret"]
    
    def attributes(self):
        return gkrlib.get_key_info(self.keyring().id(), self.id())["attributes"]

    def fmt_id(self):
        return "[%03d]"%(self.id())

    def fmt_simple(self):
        return "%s %s"%(self.fmt_id(), self.name())
    
    def fmt(self):
        return "%s%s\nSecret: %s\n%s" % (self.sep, self.fmt_simple(), self.secret(), self.fmt_attributes())
    
    def fmt_attributes(self):
        attributes = self.attributes()
        return self.sep + "\n".join([ "%s: %s"%(key, attributes[key]) for key in attributes ]) + "\n" + self.sep
    
    def match(self, pattern):
        return fnmatch.fnmatch(self.name(), pattern)
    
    def startswith(self, pattern):
        return self.name().startswith(pattern)
    
class DB(list):
    
    def clear(self):
        while len(self) > 0 : self.pop()
    
    def update(self, **kwargs):
        for item in self:
            item.update(**kwargs)
    
    def filter(self, function):
        return DB(item for item in self if function(item))
    
