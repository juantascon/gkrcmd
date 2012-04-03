from gkrcmd import key, keyring, gkrlib
from gkrcmd.errors import KeyringNotFoundError, NoWorkingKeyringError

import logging
def log(): return logging.getLogger(__name__)

class Manager():
    
    def __init__(self):
        self.key_db = key.DB()
        self.keyring_db = keyring.DB()
        self.wkeyring = None
    
    def get_wkeys(self):
        db = self.key_db.filter(lambda k: k.keyring() == self.get_wkeyring())
        return db
    
    def get_wkeyring(self):
        if not self.wkeyring: raise NoWorkingKeyringError("This operation requires a working keyring")
        return self.wkeyring
    
    def set_wkeyring(self, keyring_id):
        db = self.keyring_db.filter(lambda kr: kr.id() == keyring_id)
        if len(db) == 0: raise KeyringNotFoundError("The keyring %s cannot be found" %(keyring_id))
        
        self.wkeyring = db[0]
    
    def load(self):
        self.key_db.clear()
        self.keyring_db.clear()
        
        keyrings = gkrlib.get_keyrings()
        for kr_info in keyrings:
            kr_obj = keyring.Keyring(id=kr_info["id"])
            self.keyring_db.append(kr_obj)
            
            keys = gkrlib.get_keys(kr_obj.id())
            for k_info in keys:
                k_obj = key.Key(id=k_info["id"], keyring=kr_obj)
                self.key_db.append(k_obj)
        
        self.set_wkeyring(gkrlib.get_default_keyring())
