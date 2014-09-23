import os
import ConfigParser


# To be case insensitive (files vs env), store all as lowercase
class Config(object):

    def __init__(self):
        self.data = {}


    def __getitem__(self, key):
        return self.get(key)


    def __setitem__(self, key, value):
        self.set(key, value)


    def get(self, key, fallback=None):
        safeKey = key.lower()
        return self.data.get(safeKey, fallback)


    def set(self, key, value):
        safeKey = key.lower()
        self.data[safeKey] = value


    def update(self, src):
        for key, value in src.iteritems():
            self.set(key, value)


    def __str__(self):
        return str(self.data)


    def __repr__(self):
        lines = ["%s = %s" % (k,v) for (k,v) in self.data.iteritems()]
        return "\n".join(lines)


    def setIfSomething(self, key, value):
        if value != None:
            self.set(key, value)


    # --- loading

    def loadFileSection(self, filename, section):
        if os.path.isfile(filename):
            try:
                cfg = ConfigParser.RawConfigParser()
                cfg.read('config.cfg')
                for key in cfg.options(section):
                    self.setIfSomething(key, cfg.get(section, key))
            except:
                pass


    def loadEnv(self, mapping):
        if isinstance(mapping, dict):
            for envKey, cfgKey in mapping.iteritems():
                self.setIfSomething(cfgKey, os.environ.get(envKey, None))
        elif isinstance(mapping, list):
            for key in mapping:
                self.setIfSomething(key, os.environ.get(key, None))
        else:
            raise NameError('loadEnv needs dict or list for mapping')
