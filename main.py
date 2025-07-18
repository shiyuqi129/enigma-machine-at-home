class Mapping:
    def __init__(self,wiring: list[int]) -> None:
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
    
    def _decode(self,letter_index: int) -> int:
        '''Given a number, return the result of the decoding according to the wiring.'''
        if not isinstance(letter_index,int):
            raise TypeError("Mapping input must be an integer")
        if letter_index>self.size or letter_index<0:
            raise ValueError("Input out of range")
        return self.wiring.index(letter_index)


class Rotor (Mapping):
    def __init__(self,wiring: list[int],notches: list[int] =[],initial_position: int =0, ring_position:int =0) -> None:
        '''Initialize a rotor is the given wiring with a list of notch position and set it at an initial position and ring position. initial_position and notches is according to the alphabet ring'''
        if not isinstance(initial_position,int):
            raise TypeError("initial_position should be an integer")
        if not isinstance(initial_position,int):
            raise TypeError("ring_position should be an integer")
        if not isinstance(wiring,list):
            raise TypeError("wiring must be a list")
        if initial_position<0 or initial_position>=len(wiring):
            raise ValueError("initial_position out of range")
        if ring_position<0 or ring_position>=len(wiring):
            raise ValueError("ring_position out of range")
        if not isinstance(notches,list):
            raise TypeError("notches must be a list")
        if any(not isinstance(x,int) for x in notches):
            raise TypeError("notches must be a list of integer")
        if any(x<0 or x>=len(wiring) for x in notches):
            raise ValueError("Some of the notches are out of range")
        self.position=(initial_position+ring_position)%len(wiring)
        self.ring_position=ring_position
        self.notches=notches
        super().__init__(wiring[self.position:]+wiring[:self.position])

    def rotate(self) -> None:
        '''Rotate left by 1 space'''
        self.wiring=self.wiring[1:]+self.wiring[:1]
        self.position+=1
        self.position%=self.size

    def forward(self,letter_index: int) -> int:
        '''Given a input from the direction of the entry wheel, return the output of the rotor'''
        return super()._encode(letter_index)
    
    def backward(self,letter_index: int) -> int:
        '''Given a input from the direction of the reflector, return the output of the rotor'''
        return super()._decode(letter_index)
    
    def is_at_notch(self) -> bool:
        return (self.position-self.ring_position)%self.size in self.notches
    
    def set_position(self,new_position: int) -> None:
        '''Use the new_position according to the alphabet ring'''
        if not isinstance(new_position,int):
            raise TypeError("new_position should be an integer")
        if new_position<0 or new_position>=self.size:
            raise ValueError("new_position out of range")
        new_position=(new_position+self.ring_position)%self.size
        offset=(new_position-self.position)%self.size
        self.wiring=self.wiring[offset:]+self.wiring[:offset]
        self.position=new_position

    def set_ring_position(self,new_ring_position: int) -> None:
        '''Set the alphabet ring to a new position'''
        if not isinstance(new_ring_position,int):
            raise TypeError("new_ring_position should be an integer")
        if new_ring_position<0 or new_ring_position>=self.size:
            raise ValueError("new_ring_position out of range")
        self.ring_position=new_ring_position


class Reflector (Mapping):
    def __init__(self,wiring: list[int]) -> None:
        if any(wiring[x]!=wiring.index(x) for x in wiring):
            raise ValueError("The wiring lead to a reflector that is not reflective")
        super().__init__(wiring)

    def reflect(self,letter_index: int) -> int:
        '''Given a input, return the output of the reflector'''
        return super()._encode(letter_index)


class Plugboard (Mapping):
    def __init__(self,size: int=26,connections: list[list[int]]=[]) -> None:
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

    def swap(self,letter_index: int) -> int:
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
        if i<0 or i>=self.size or j<0 or j>=self.size:
            raise ValueError("Connection contain index out of range")
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
        if i<0 or i>=self.size or j<0 or j>=self.size:
            raise ValueError("Connection contain index out of range")
        if self.wiring[i]!=j or self.wiring[j]!=i:
            raise ValueError("Non-existing connection")
        self.wiring[i]=i
        self.wiring[j]=j

    def remove_all_connection(self) -> None:
        '''Remove every connections on the plugboard'''
        for i in range(len(self.wiring)):
            self.wiring[i]=i


class Enigma:
    def __init__(self,rotors:list[Rotor]|None=None,reflector:Reflector|None=None,plugboard:Plugboard|None=None) -> None:
        if rotors==None and reflector==None and plugboard==None:
            raise ValueError("You are not allowed to making a machine with nothing in it")
        if rotors==None:
            rotors=[]
        if not isinstance(rotors,list):
            raise TypeError("rotors must be a list")
        if not isinstance(reflector,(type(None),Reflector)):
            raise TypeError("reflector must be of class Reflector")
        if not isinstance(plugboard,(type(None),Plugboard)):
            raise TypeError("plugboard must be of class Plugboard")
        if any(not isinstance(rotor,Rotor) for rotor in rotors):
            raise TypeError("rotors must be a list rotor of class Rotor")
        if any(rotor.size!=rotors[0].size for rotor in rotors):
            raise ValueError("All rotors must have the same size")
        self.size=None
        if len(rotors)!=0:
            self.size=rotors[0].size
        if self.size==None:
            if reflector!=None:
                self.size=reflector.size
            else:
                self.size=plugboard.size # type: ignore
        if reflector==None:
            reflector=Reflector([i for i in range(self.size)])
        else:
            if reflector.size!=self.size:
                raise ValueError("The components must have the same size")
        if plugboard==None:
            plugboard=Plugboard(self.size)
        else:
            if plugboard.size!=self.size:
                raise ValueError("The components must have the same size")
        self.rotors=rotors[:]
        self.reflector=reflector
        self.plugboard=plugboard