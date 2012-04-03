import gnomekeyring as gkr
import getpass

from gkrcmd.errors import KeyringPasswordError, KeyringLockedError, UnknownError

# import glib
# glib.set_application_name("gkrcmd")

import logging
def log(): return logging.getLogger(__name__)

def keyring_unlock_login(keyring_id):
    # try unlocking by using the login keyring
    try:
        password = ""
        for key_id in gkr.list_item_ids_sync("login"):
            attributes = gkr.item_get_attributes_sync("login", key_id)
            try:
                if attributes["keyring"] == "LOCAL:/keyrings/%s.keyring"%(keyring_id):
                    password = gkr.item_get_info_sync("login", key_id).get_secret()
                    break
            except KeyError: pass
        
        gkr.unlock_sync(keyring_id, password)
    except gkr.IOError: pass

def keyring_unlock_password(keyring_id):
    try: gkr.unlock_sync(keyring_id, getpass.getpass())
    except gkr.IOError: raise KeyringPasswordError("invalid password")

def keyring_lock(keyring_id):
    try: gkr.lock_sync(keyring_id)
    except gkr.IOError: raise UnknownError("something weird happend")
    
def get_default_keyring():
    return gkr.get_default_keyring_sync()

def get_keyring_info(keyring_id):
    locked = gkr.get_info_sync(keyring_id).get_is_locked()
    return {"locked": locked}

def get_keyrings():
    l = []
    
    for name in gkr.list_keyring_names_sync():
        locked = gkr.get_info_sync(name).get_is_locked()
        
        keyring = { "id": name, "locked": locked }
        l.append(keyring)
    
    return l

def get_key_info(keyring_id, key_id):
    # log().debug("key info -- ring:%s, key:%d" %(keyring_id, key_id))
    
    try:
        name = gkr.item_get_info_sync(keyring_id, key_id).get_display_name()
        secret = gkr.item_get_info_sync(keyring_id, key_id).get_secret()
        attributes = gkr.item_get_attributes_sync(keyring_id, key_id)
    except gkr.IOError: raise KeyringLockedError("this operation requires the keyring to be unlocked")
    
    return {"name": name, "secret": secret, "attributes": attributes}
    
def get_keys(keyring_id):
    l = []
    
    for key_id in gkr.list_item_ids_sync(keyring_id):
        key = { "id": key_id }
        l.append(key)
        
    return l

