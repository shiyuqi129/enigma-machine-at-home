class Mapping:
    def __init__(self,wiring: list[int]):
        '''Wiring should be numbers from 0-n exactly once each in any order where n is the length of wiring'''
        if not isinstance(wiring,list):
            raise TypeError("wiring must be a list")
        if any(not isinstance(x,int) for x in wiring):
            raise TypeError("wiring must be a list of integer")
        if sorted(wiring)!=list(range(len(wiring))):
            raise ValueError("Wiring should be numbers from 0-n exactly once each where n is the length of wiring")
        self.wiring=wiring[:]
        self.size=len(wiring)
    def _encode(self,letter_index: int) -> int:
        '''Given a number, return the result of the encoding according to the wiring.'''
        if not isinstance(letter_index,int):
            raise TypeError("Mapping input must be an integer")
        if letter_index>self.size or letter_index<0:
            raise ValueError("Input out of range")
        return self.wiring[letter_index]
    def _decode(self,letter_index: int) -> int | None:
        '''Given a number, return the result of the decoding according to the wiring.'''
        if not isinstance(letter_index,int):
            raise TypeError("Mapping input must be an integer")
        if letter_index>self.size or letter_index<0:
            raise ValueError("Input out of range")
        return self.wiring.index(letter_index)

class Rotor (Mapping):
    def __init__(self,wiring: list[int],notches: list[int] =[],initial_position: int =0):
        '''Initialize a rotor is the given wiring with a list of notch position and set it at an initial position.'''
        if not isinstance(initial_position,int):
            raise TypeError("initial_position should be an integer")
        if not isinstance(wiring,list):
            raise TypeError("wiring must be a list")
        if initial_position<0 or initial_position>=len(wiring):
            raise ValueError("initial_position out of range")
        if not isinstance(notches,list):
            raise TypeError("notches must be a list")
        if any(not isinstance(x,int) for x in notches):
            raise TypeError("notches must be a list of integer")
        if any(x<0 or x>=len(wiring) for x in notches):
            raise ValueError("Some of the notches are out of range")
        self.position=initial_position
        self.notches=notches
        super().__init__(wiring[initial_position:]+wiring[:initial_position])
    def rotate(self) -> None:
        '''Rotate left by 1 space'''
        self.wiring=self.wiring[1:]+self.wiring[:1]
    def forward(self,letter_index: int) -> int | None:
        '''Given a input from the direction of the entry wheel, return the output of the rotor'''
        return super()._encode(letter_index)
    def backward(self,letter_index: int) -> int | None:
        '''Given a input from the direction of the reflector, return the output of the rotor'''
        return super()._decode(letter_index)
    
class Reflector (Mapping):
    def __init__(self,wiring: list[int]):
        if any(wiring[x]!=wiring.index(x) for x in wiring):
            raise ValueError("The wiring lead to a reflector that is not reflective")
        super().__init__(wiring)
    def reflect(self,letter_index: int) -> int | None:
        '''Given a input, return the output of the reflector'''
        return super()._encode(letter_index)

class Plugboard (Mapping):
    def __init__(self,connections: list[list[int]]=[],size: int=26):
        '''Initialize the plugboard with a list of connections.'''
        if not isinstance(size,int):
            raise TypeError("size must be an integer")
        if not isinstance(connections,list):
            raise TypeError("connection must be a list")
        if size<=0:
            raise ValueError("size must be positive integer")
        wiring=[i for i in range(size)]
        for connection in connections:
            if not isinstance(connection,list):
                raise TypeError("Each connection must be a list containing exatly two integer")
            if len(connection)!=2:
                raise ValueError("Each connection must be a list containing exatly two integer")
            i,j=connection
            if not (isinstance(i,int) and isinstance(j,int)):
                raise TypeError("Each connection must be a list containing exatly two integer")
            if i<0 or i>=size or j<0 or j>=size:
                raise ValueError("Connection contain index out of range")
            if wiring[i]!=i or wiring[j]!=j or i==j:
                raise ValueError("Repeated or conflicted plugboard configuration")
            wiring[i]=j
            wiring[j]=i
        super().__init__(wiring)
    def swap(self,letter_index: int) -> int | None:
        '''Given a input, return the output of the plugboard'''
        return super()._encode(letter_index)
    def add_connection(self,i,j=None) -> None:
        '''Add connection between i and j. Input could also be two integers, a list, or a tuple'''
        if j==None:
            if not isinstance(i,(list,tuple)):
                raise TypeError("Input must also be two integers in a list, a tuple, or seperated")
            if len(i)!=2:
                raise ValueError("Input must also be exactly two integers")
            i,j=i
        if not (isinstance(i,int) and isinstance(j,int)):
            raise TypeError("Input must be integers")
        if self.wiring[i]!=i or self.wiring[j]!=j:
            raise ValueError("Conflict with existing connection")
        self.wiring[i]=j
        self.wiring[j]=i
    def remove_connection(self,i,j=None) -> None:
        '''Remove connection between i and j. Input could also be a list or a tuple'''
        if j==None:
            if not isinstance(i,(list,tuple)):
                raise TypeError("Input must also be two integers in a list, a tuple, or seperated")
            if len(i)!=2:
                raise ValueError("Input must also be exactly two integers")
            i,j=i
        if not (isinstance(i,int) and isinstance(j,int)):
            raise TypeError("Input must be integers")
        if self.wiring[i]!=j or self.wiring[j]!=i:
            raise ValueError("Non-existing connection")
        self.wiring[i]=i
        self.wiring[j]=j
    def remove_all_connection(self) -> None:
        '''Remove every connections on the plugboard'''
        for i in range(len(self.wiring)):
            self.wiring[i]=i
