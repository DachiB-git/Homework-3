class A:
    def __init__(self,param):
        self.__param = param
    @property
    def param(self):
        return self.__param
    @param.deleter
    def param(self):
        del self.__param

obj1 = A('hello')
del obj1.param
print(obj1.param)