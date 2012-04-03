import fnmatch
from gkrcmd import gkrlib

import logging
def log(): return logging.getLogger(__name__)

class Keyring(dict):
    
    # expected: id
    def __init__(self, **kwargs):
        dict.__init__(self)
        self.update(**kwargs)
    
    def __repr__(self):
        return self.fmt()
    
    def __eq__(self, other):
        return (self.id() == other.id())
    
    def update(self, **kwargs):
        for key,value in kwargs.items():
            self[key] = value
    
    def locked(self):
        return gkrlib.get_keyring_info(self.id())["locked"]
    
    def unlock(self):
        if self.locked():
            gkrlib.keyring_unlock_login(self.id())
            
        if self.locked():
            gkrlib.keyring_unlock_password(self.id())
        
    def lock(self):
        if not self.locked(): gkrlib.keyring_lock(self.id())
    
    def id(self):
        return self["id"]
    
    def name(self):
        return self.id()
    
    def fmt(self):
        return "KEYRING: %s [ %s ]" % ( self.name(), "locked" if self.locked() else "unlocked" )
    
    def match(self, pattern):
        return fnmatch.fnmatch(self.name(), pattern)
    
    def startswith(self, pattern):
        return self.name().startswith(pattern)
    
class DB(list):
    
    def clear(self):
        while len(self) > 0 : self.pop()
    
    def list(self):
        return "\n".join([ item.fmt() for item in self ])
    
    def update(self, **kwargs):
        for item in self:
            item.update(**kwargs)
    
    def filter(self, function):
        return DB(item for item in self if function(item))
