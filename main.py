import wirings

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
    def __init__(self,wiring: list[int],notches: list[int] =[],initial_position: int =0, ring_setting:int =0) -> None:
        '''Initialize a rotor is the given wiring with a list of notch position and set it at an initial position and ring settingh. initial_position and notches is according to the alphabet ring'''
        if not isinstance(initial_position,int):
            raise TypeError("initial_position should be an integer")
        if not isinstance(initial_position,int):
            raise TypeError("ring_setting should be an integer")
        if not isinstance(wiring,list):
            raise TypeError("wiring must be a list")
        if initial_position<0 or initial_position>=len(wiring):
            raise ValueError("initial_position out of range")
        if ring_setting<0 or ring_setting>=len(wiring):
            raise ValueError("ring_setting out of range")
        if not isinstance(notches,list):
            raise TypeError("notches must be a list")
        if any(not isinstance(x,int) for x in notches):
            raise TypeError("notches must be a list of integer")
        if any(x<0 or x>=len(wiring) for x in notches):
            raise ValueError("Some of the notches are out of range")
        self.position=(initial_position-ring_setting)%len(wiring)
        self.ring_setting=ring_setting
        self.notches=notches[:]
        super().__init__(wiring)

    @classmethod
    def from_name(cls,name : str,initial_position: int =0, ring_setting:int =0):
        '''Create a rotor with the preset wiring associated with the name'''
        try:
            return cls(wirings.ROTOR_WIRINGS[name],wirings.ROTOR_NOTCHES[name],initial_position,ring_setting)
        except KeyError:
            raise ValueError(f"Rotor '{name}' not found")

    def rotate(self) -> None:
        '''Rotate left by 1 space'''
        self.position+=1
        self.position%=self.size

    def forward(self,letter_index: int) -> int:
        '''Given a input from the direction of the entry wheel, return the output of the rotor'''
        return (super()._encode((letter_index+self.position)%self.size)-self.position)%self.size
    
    def backward(self,letter_index: int) -> int:
        '''Given a input from the direction of the reflector, return the output of the rotor'''
        return (super()._decode((letter_index+self.position)%self.size)-self.position)%self.size
    
    def is_at_notch(self) -> bool:
        return (self.position+self.ring_setting)%self.size in self.notches
    
    def set_position(self,new_position: int) -> None:
        '''Use the new_position according to the alphabet ring'''
        if not isinstance(new_position,int):
            raise TypeError("new_position should be an integer")
        if new_position<0 or new_position>=self.size:
            raise ValueError("new_position out of range")
        new_position=(new_position+self.ring_setting)%self.size
        self.position=new_position

    def set_ring_setting(self,new_ring_setting: int) -> None:
        '''Set the alphabet ring to a new position without turing the rotor'''
        if not isinstance(new_ring_setting,int):
            raise TypeError("new_ring_setting should be an integer")
        if new_ring_setting<0 or new_ring_setting>=self.size:
            raise ValueError("new_ring_setting out of range")
        self.ring_setting=new_ring_setting


class Reflector (Mapping):
    def __init__(self,wiring: list[int]) -> None:
        if any(wiring[x]!=wiring.index(x) for x in wiring):
            raise ValueError("The wiring lead to a reflector that is not reflective")
        super().__init__(wiring)

    @classmethod
    def from_name(cls,name : str):
        '''Create a reflector with the preset wiring associated with the name'''
        try:
            return cls(wirings.REFLECTOR_WIRINGS[name])
        except KeyError:
            raise ValueError(f"Reflector '{name}' not found")

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
            if not isinstance(connection,(list,str)):
                raise TypeError("Each connection must be a list containing exatly two integer or string of two letters")
            if len(connection)!=2:
                raise ValueError("Each connection must be a list containing exatly two integer or string of two letters")
            i,j=connection
            if isinstance(i,str):
                if i.isalpha():
                    i=ord(i.upper())-ord("A")
                else:
                    raise ValueError("Input string should only contain letters A-Z")
            if isinstance(j,str):
                if j.isalpha():
                    j=ord(j.upper())-ord("A")
                else:
                    raise ValueError("Input string should only contain letters A-Z")
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
        '''Add connection between i and j. Input could also be two integers, a list, or a tuple. Also take string by converting A-Z to 0-25'''
        if j==None:
            if not isinstance(i,(list,tuple,str)):
                raise TypeError("Input must be two integers in a list, a tuple, seperated, or string of letters")
            if len(i)!=2:
                raise ValueError("Input must be exactly two integers or letters")
            i,j=i
        if isinstance(i,str):
            if len(i)==1 and i.isalpha():
                i=ord(i.upper())-ord("A")
            else:
                raise ValueError("Input string should only contain letters A-Z")
        if isinstance(j,str):
            if len(j)==1 and j.isalpha():
                j=ord(j.upper())-ord("A")
            else:
                raise ValueError("Input string should only contain letters A-Z")
        if not (isinstance(i,int) and isinstance(j,int)):
            raise TypeError("Input must be integers or A-Z")
        if i<0 or i>=self.size or j<0 or j>=self.size:
            raise ValueError("Connection contain index out of range")
        if i==j:
            raise ValueError("Both end of the connection must be different position")
        if self.wiring[i]!=i or self.wiring[j]!=j:
            raise ValueError("Conflict with existing connection")
        self.wiring[i]=j
        self.wiring[j]=i

    def remove_connection(self,i,j=None) -> None:
        '''Remove connection between i and j. Input could also be two integers, a list, or a tuple. Also take string by converting A-Z to 0-25'''
        if j==None:
            if not isinstance(i,(list,tuple,str)):
                raise TypeError("Input must be two integers in a list, a tuple, seperated, or string of letters")
            if len(i)!=2:
                raise ValueError("Input must be exactly two integers or letters")
            i,j=i
        if isinstance(i,str):
            if len(i)==1 and i.isalpha():
                i=ord(i.upper())-ord("A")
            else:
                raise ValueError("Input string should only contain letters A-Z")
        if isinstance(j,str):
            if len(j)==1 and j.isalpha():
                j=ord(j.upper())-ord("A")
            else:
                raise ValueError("Input string should only contain letters A-Z")
        if not (isinstance(i,int) and isinstance(j,int)):
            raise TypeError("Input must be integers or A-Z")
        if i<0 or i>=self.size or j<0 or j>=self.size:
            raise ValueError("Connection contain index out of range")
        if self.wiring[i]!=j or self.wiring[j]!=i or i==j:
            raise ValueError("Non-existing connection")
        self.wiring[i]=i
        self.wiring[j]=j

    def remove_all_connection(self) -> None:
        '''Remove every connections on the plugboard'''
        for i in range(len(self.wiring)):
            self.wiring[i]=i


class Enigma:
    def __init__(self,rotors:list[Rotor]|None=None,reflector:Reflector|None=None,plugboard:Plugboard|None=None) -> None:
        '''Create an Enigma machine with a list of rotors (from left to right), a reflector, and a plugboard'''
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
        self.size:int =-1
        if len(rotors)!=0:
            self.size=rotors[0].size
        if self.size==-1:
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
    
    def _step(self) -> None:
        is_engaged: bool=True
        for rotor in reversed(self.rotors):
            is_at_notch: bool=rotor.is_at_notch()
            if (is_at_notch and rotor!=self.rotors[0]) or is_engaged:
                rotor.rotate()
            is_engaged=is_at_notch

    def _encode(self, input: int) -> int:
        '''Encode a input without stepping'''
        if not isinstance(input, int):
            raise TypeError("input must be an integer")
        if input<0 or input>=self.size:
            raise ValueError("input out of range")
        output=self.plugboard.swap(input)
        for rotor in reversed(self.rotors):
            output=rotor.forward(output)
        output=self.reflector.reflect(output)
        for rotor in self.rotors:
            output=rotor.backward(output)
        return self.plugboard.swap(output)

    def key_press(self,input: int=0) -> int:
        '''Simulate a key press on a Enigma machine'''
        if not isinstance(input, int):
            raise TypeError("input must be an integer")
        if input<0 or input>=self.size:
            raise ValueError("input out of range")
        self._step()
        return self._encode(input)
    
    def encode_message(self,message: str="") -> str:
        '''Encode a message using the Enigma machine. The machine must have a size of 26.
        Will only encode A-Z or a-z, other character will be skipped'''
        if self.size!=26:
            raise ValueError("The Enigma must be of size 26 to support encoding message made out of letters")
        message=message.upper()
        output: list[str]=[]
        for c in message:
            if not c.isalpha():
                continue
            output.append(chr(self.key_press(ord(c)-ord("A"))+ord("A")))
        return "".join(output)