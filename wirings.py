ROTOR_WIRING_STRINGS={
    "I"     :"EKMFLGDQVZNTOWYHXUSPAIBRCJ",
    "II"    :"AJDKSIRUXBLHWTMCQGZNPYFVOE",
    "III"   :"BDFHJLCPRTXVZNYEIWGAKMUSQO",
    "IV"    :"ESOVPZJAYQUIRHXLNFTGKDCMWB",
    "V"     :"VZBRGITYUPSDNHLXAWMJQOFECK",
    "VI"    :"JPGVOUMFYQBENHZRDKASXLICTW",
    "VII"   :"NZJHGRCXMYSWBOUFAIVLPEKQDT",
    "VIII"  :"FKQHTLXOCBJSPDZRAMEWNIUYGV"
}

ROTOR_NOTCH_STRINGS={
    "I"     :"Q",
    "II"    :"E",
    "III"   :"V",
    "IV"    :"J",
    "V"     :"Z",
    "VI"    :"MZ",
    "VII"   :"MZ",
    "VIII"  :"MZ"
}

REFLECTOR_WIRING_STRINGS={
    "A"     :"EJMZALYXVBWFCRQUONTSPIKHGD",
    "B"     :"YRUHQSLDPXNGOKMIEBFZCWVJAT",
    "C"     :"FVPJIAOYEDRZXWGCTKUQSBNMHL"
}

def read_position_string(positions:str) -> list[int]:
    '''Given positions written in string of A to Z, convert it to a list of integer from 0 to 25'''
    if not isinstance(positions,str):
        raise TypeError("Input must be a string")
    return [ord(c.upper())-ord("A") for c in positions if c.isalpha()]

def write_position_string(positions:list[int]) -> str:
    '''Given a list of integer from 0 to 25, convert it to positions written in string of A to Z'''
    if not isinstance(positions,list):
        raise TypeError("Input must be a list of integers")
    if not all(isinstance(num,int) for num in positions):
        raise TypeError("Input must be a list of integers")
    if not all(26>num>=0 for num in positions):
        raise ValueError("Some of the position are out of range. Input should be in 0~25")
    wiring_letters=[chr(num+ord("A")) for num in positions]
    return "".join(wiring_letters)

ROTOR_WIRINGS={name:read_position_string(wiring_string) for name,wiring_string in ROTOR_WIRING_STRINGS.items()}
ROTOR_NOTCHES={name:read_position_string(notches_string) for name,notches_string in ROTOR_NOTCH_STRINGS.items()}
REFLECTOR_WIRINGS={name:read_position_string(wiring_string) for name,wiring_string in REFLECTOR_WIRING_STRINGS.items()}
