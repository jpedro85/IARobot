class Utils:
    
    file  = open('output.txt', 'w')

    @classmethod
    def getFile(cls):
        return cls.file
    
    @classmethod
    def print(cls,line:int,file:str,string:str):
        str_r = "L:" + str(line) + " f:"+ file + ": " +string
        print(str_r,end="")
        cls.file.write(str_r)


