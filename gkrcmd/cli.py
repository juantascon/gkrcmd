import readline, cmd, argparse, sys
from gkrcmd import manager, keyring, key
from gkrcmd.errors import GKRCMDError, KeyringNotFoundError

from gkrcmd import msg

import logging
def log(): return logging.getLogger(__name__)

class ArgumentParser(argparse.ArgumentParser):
    
    def _print_message(self, message, file=None):
        if message:
            msg(message)
            
class Cmd(cmd.Cmd, manager.Manager):
    def __init__(self):
        readline.set_completer_delims(" ")
        
        manager.Manager.__init__(self)
        cmd.Cmd.__init__(self)
        
        self.update_prompt()
        
    def update_prompt(self):
        self.prompt = "gkrcmd:> "
    
    def load(self):
        try: manager.Manager.load(self)
        except KeyringNotFoundError as ex:
            msg("Current Keyring: none")
            return
        except GKRCMDError as ex:
            msg("FAIL: %s\n"%(ex))
            return
        
        msg("Current Keyring:\n%s\n"%(self.wkeyring.fmt()))
        
    def do_reload(self, line):
        parser = ArgumentParser(prog="reload", description="Reload keys and keyrings", epilog="example: reload")
        try: args = parser.parse_args(line.split())
        except SystemExit: return
        
        self.load()
    
    #
    # Keyrings Commands
    #
    def do_keyring(self, line):
        parser = ArgumentParser(prog="keyring", description="Set or show (no arguments) the working keyring", epilog="example: keyring default")
        parser.add_argument("keyring", metavar="KEYRING", help="keyring name")
        try: args = parser.parse_args([line])
        except SystemExit: return
        
        if args.keyring:
            try:  self.set_wkeyring(args.keyring)
            except GKRCMDError as ex:
                msg("FAIL: %s\n"%(ex))
                return
        
        msg("Current Keyring:\n%s\n"%(self.wkeyring.fmt()))

    def do_lock(self, line):
        parser = ArgumentParser(prog="lock", description="Unlock the working keyring", epilog="example: unlock")
        try: args = parser.parse_args(line.split())
        except SystemExit: return
        
        try: self.get_wkeyring().lock()
        except GKRCMDError as ex: msg("FAIL: %s\n"%(ex))
        msg("%s\n"%(self.wkeyring.fmt()))
    
    def do_unlock(self, line):
        parser = ArgumentParser(prog="unlock", description="Unlock the working keyring", epilog="example: unlock")
        try: args = parser.parse_args(line.split())
        except SystemExit: return
        
        try: self.get_wkeyring().unlock()
        except GKRCMDError as ex: msg("FAIL: %s\n"%(ex))
        msg("%s\n"%(self.wkeyring.fmt()))
    
    def do_keyring_ls(self, line):
        parser = ArgumentParser(prog="keyring_ls", description="Show keyrings information", epilog="example: keyring_ls *")
        parser.add_argument("filters", metavar="KEYRING", nargs="*", default=["*"], help="keyring name or filter, ex: defau*")
        
        try: args = parser.parse_args(line.split())
        except SystemExit: return
        
        db = self.keyring_db
        
        for pattern in args.filters:
            db.filter(lambda k: k.match(pattern))
            
            for kr in db:
                print(kr.fmt())
    
    #
    # Complete text
    #
    # def _complete(self, text, options, db):
    #     _options = [ opt for opt in options if opt.startswith(text) ]
    #     _episodes = db.complete_text(text)
        
    #     return _options + _episodes
    
    # def complete_tor(self, text, line, start_index, end_index):
    #     return self._complete(text, ["-h", "--help"], self.episode_db.filter(lambda url: not url.future() and url["status"] in [cons.NEW]))
    
    # def complete_ls(self, text, line, start_index, end_index):
    #     return self._complete(text, ["-n", "--new", "-a", "--adquired", "-s", "--seen", "-f", "--future"], self.episode_db)
    
    def do_ls(self,line):
        parser = ArgumentParser(prog="ls", description="Show keys information", epilog="example: ls -a *")
        parser.add_argument("-a", "--all", action="store_true", help="list all the key info (including secret)")
        parser.add_argument("filters", metavar="KEY", nargs="*", default=["*"], help="key name or filter, ex: http://www.google.com")
        
        try: args = parser.parse_args(line.split())
        except SystemExit: return
        
        try:
            db = self.get_wkeys()
            for pattern in args.filters:
                db = db.filter(lambda k: k.match(pattern))
                
                if args.all: print("\n".join([ "%s"%(k.fmt()) for k in db ]))
                else: print("\n".join([ "%s"%(k.fmt_simple()) for k in db ]))
        except GKRCMDError as ex:
            msg("FAIL: %s\n"%(ex))
        
    #
    # Auxiliary commands:
    #
    def do_help(self, line):
        sep = "\n   "
        msg("To get specific help type: COMMAND --help\n\n")
        msg("Auxiliary commands:"+sep+sep.join(["exit", "quit", "help"]) + "\n")
        msg("Keyrings commands:"+sep+sep.join(["reload", "keyring", "keyring_ls", "lock", "unlock"]) + "\n")
        msg("Keys commands:"+sep+sep.join(["ls"]) + "\n")
    
    def ask_yn(self, question):
        answer = ""
        while True:
            answer = input(question + " [y/n]: ").lower()
            if answer in ["y", "yes"]: return True
            elif answer in ["n", "no"]: return False
    
    def exit(self):
        return True
    
    def emptyline(self):
        pass
    
    def do_exit(self, line):
        parser = ArgumentParser(prog="exit/quit", description="Exit the application", epilog="example: exit")
        try: args = parser.parse_args(line.split())
        except SystemExit: return
        
        return self.exit()
    
    do_quit = do_exit
    
    def default(self, line):
        if line == "EOF":
            print()
            return self.exit()
        
        msg("Invalid command: %s"%(line.split(" ")[0]))
        return self.do_help("")
    
    def cmdloop(self):
        try:
            return cmd.Cmd.cmdloop(self)
        except KeyboardInterrupt:
            print("^C")
            return self.cmdloop()
