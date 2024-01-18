class Utils:
    
    file  = open('output.txt', 'w')

    @classmethod
    def getFile(cls):
        return cls.file

