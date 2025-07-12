class Mapping:
    def __init__(self,wiring: list[int]):
        '''Wiring should be every number from 0-n once in any order. 
        Warning: There is no filter for invalid wiring'''
        self.wiring=wiring[:]
    def encode(self,letter_index: int) -> int:
        '''Given a number, return the result of the mapping according to the wiring. Return None if input is out of range'''
        if letter_index>len(self.wiring) or letter_index<0:
            return None
        return self.wiring[letter_index]
class Rotor (Mapping):
    def rotate(self):
        '''Rotate left by 1 space'''
        self.wiring=self.wiring[1:]+self.wiring[:1]
class Reflector (Mapping):
    pass
class Plugboard (Mapping):
    def __init__(self,connections: list[list[int]]=[],size=26):
        '''Initialize the plugboard with a list of connections.
        Warning: There is no filter for invalid connections'''
        wiring=[i for i in range(size)]
        for i,j in connections:
            wiring[i]=j
            wiring[j]=i
        super().__init__(wiring)
    def add_connection(self,i,j=None):
        '''Add connection between i and j. Input could also be a list or a tuple
        Warning: There is no filter for invalid or overlapping connections'''
        if j==None:
            i,j=i
        self.wiring[i]=j
        self.wiring[j]=i
    def remove_connection(self,i,j=None):
        '''Remove connection between i and j. Input could also be a list or a tuple
        Warning: There is no filter for invalid or non-existing connections'''
        if j==None:
            i,j=i
        self.wiring[i]=i
        self.wiring[j]=j
    def remove_all_connection(self):
        '''Remove every connections on the plugboard'''
        for i in range(len(self.wiring)):
            self.wiring[i]=i