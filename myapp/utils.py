from configparser import ConfigParser

class readConfig():

    def __init__(self, path):
        parser = ConfigParser()
        parser.read(path)
        self.parser = parser

    def GetVariableBySection(self, section, variableName):

        return self.parser.get(section, variableName)
