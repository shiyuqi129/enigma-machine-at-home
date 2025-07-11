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
class PlugBoard (Mapping):
    pass