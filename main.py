class Mapping:
    def __init__(self,wiring: list[int]):
        '''Wiring should be every number from 0-n once in any order. 
        Warning: There is no filter for invalid wiring'''
        self.wiring=wiring[:]
    def _encode(self,letter_index: int) -> int:
        '''Given a number, return the result of the encoding according to the wiring. Return None if input is out of range'''
        if letter_index>len(self.wiring) or letter_index<0:
            return None
        return self.wiring[letter_index]
    def _decode(self,letter_index: int) -> int:
        '''Given a number, return the result of the decoding mapping according to the wiring. Return None if input is out of range'''
        if letter_index>len(self.wiring) or letter_index<0:
            return None
        return self.wiring.index(letter_index)
class Rotor (Mapping):
    def __init__(self,wiring: list[int],notches: list[int] =[],initial_position=0):
        '''Initialize a rotor is the given wiring with a list of notch position and set it at an initial position.
        Warning: No check for invalid input'''
        self.position=initial_position
        self.notches=notches
        super().__init__(wiring[initial_position:]+wiring[:initial_position])
    def rotate(self):
        '''Rotate left by 1 space'''
        self.wiring=self.wiring[1:]+self.wiring[:1]
    def forward(self,letter_index: int) -> int:
        '''Given a input from the direction of the entry wheel, return the output of the rotor'''
        return super()._encode(letter_index)
    def backward(self,letter_index: int) -> int:
        '''Given a input from the direction of the reflector, return the output of the rotor'''
        return super()._decode(letter_index)
class Reflector (Mapping):
    def reflect(self,letter_index: int) -> int:
        '''Given a input, return the output of the reflector'''
        return super()._encode(letter_index)
class Plugboard (Mapping):
    def __init__(self,connections: list[list[int]]=[],size=26):
        '''Initialize the plugboard with a list of connections.
        Warning: There is no filter for invalid connections'''
        wiring=[i for i in range(size)]
        for i,j in connections:
            wiring[i]=j
            wiring[j]=i
        super().__init__(wiring)
    def swap(self,letter_index):
        '''Given a input, return the output of the plugboard'''
        return super()._encode(letter_index)
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