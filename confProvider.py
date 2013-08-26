import ConfigParser
from base64 import *

class ConfigProvider:
    def __init__(self):
        self.config = ConfigParser.SafeConfigParser()
        self.config.read('UncPathConf.cfg')
    def write(self, uncPathStruct):
        if self.config.has_section(uncPathStruct[0]):
            return False
        else:
            self.config.add_section(uncPathStruct[0])
            self.config.set(uncPathStruct[0], 'unc path', uncPathStruct[1])
            if len(uncPathStruct) > 2:
                self.config.set(uncPathStruct[0], 'username', uncPathStruct[2])
                self.config.set(uncPathStruct[0], 'password', encodestring(uncPathStruct[3]))
            with open('UncPathConf.cfg', 'wb') as configfile:
                self.config.write(configfile)
            return True

    def getAllUncPathShowString(self):
        return self.config.sections()

    def hasUncPathShowName(self, section):
        return self.config.has_section(section)
    def getSingleUncPath(self, section):
        print section
        if self.config.has_option(section, 'username'):
            return (section,
                self.config.get(section, 'unc path'),
                self.config.get(section, 'username'),
                decodestring(self.config.get(section, 'password')))
        return (section,
                self.config.get(section, 'unc path'))
    
    def getUncPath(self):
        uncPathStructGroup = []

        for section in self.config.sections():
            uncPathStructGroup.append((section,
                                       self.config.get(section, 'unc path'),
                                       self.config.get(section, 'username'),
                                       decodestring(self.config.get(section, 'password'))))
        return uncPathStructGroup

    def update(self, uncPathStruct, previousSection):
        if previousSection != uncPathStruct[0]:
            self.config.remove_section(previousSection)
            self.write(uncPathStruct)
        else:
            self.config.set(uncPathStruct[0], "unc path", uncPathStruct[1])
            self.config.set(uncPathStruct[0], "usename", uncPathStruct[2])
            self.config.set(uncPathStruct[0], "password", encodestring(uncPathStruct[3]))
            with open('UncPathConf.cfg', 'wb') as configfile:
                self.config.write(configfile)
                
    def delete(self, section):
        self.config.remove_section(section)
        with open('UncPathConf.cfg', 'wb') as configfile:
            self.config.write(configfile)
        
