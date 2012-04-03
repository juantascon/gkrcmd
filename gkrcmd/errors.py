"""Exceptions raised by gkrcmd"""

class GKRCMDError(Exception):
    """Base class for all gkrcmd exceptions"""

class UnknownError(GKRCMDError):
    """The keyring is locked"""

class KeyringLockedError(GKRCMDError):
    """The keyring is locked"""

class KeyringNotFoundError(GKRCMDError):
    """The keyring has not been found"""

class KeyNotFoundError(GKRCMDError):
    """The key has not been found"""

class NoWorkingKeyringError(GKRCMDError):
    """The current keyring has not been set"""

class KeyringPasswordError(GKRCMDError):
    """The keyring password is invalid"""
