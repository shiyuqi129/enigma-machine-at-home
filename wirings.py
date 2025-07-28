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

def read_wiring_string(wiring:str) -> list[int]:
    '''Given a wiring written in string of A-Z, convert it to  a list of 0-25'''
    return [ord(c)-ord('A') for c in wiring]

ROTOR_WIRINGS={name:read_wiring_string(wiring_string) for name,wiring_string in ROTOR_WIRING_STRINGS.items()}
ROTOR_NOTCHES={name:read_wiring_string(notches_string) for name,notches_string in ROTOR_NOTCH_STRINGS.items()}
REFLECTOR_WIRINGS={name:read_wiring_string(wiring_string) for name,wiring_string in REFLECTOR_WIRING_STRINGS.items()}
