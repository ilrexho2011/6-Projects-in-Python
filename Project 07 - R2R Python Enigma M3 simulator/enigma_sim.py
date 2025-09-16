# enigma_sim.py
# Simple Enigma M3 simulator (rotors I, II, III + Reflector B)
# Usage: edit the SETTINGS and MESSAGE below and run.

ALPH = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Rotor wirings (from right to left mapping: entry->exit at rotor in A..Z order)
ROTORS = {
    "I":   {"w":"EKMFLGDQVZNTOWYHXUSPAIBRCJ", "notch":"Q"},
    "II":  {"w":"AJDKSIRUXBLHWTMCQGZNPYFVOE", "notch":"E"},
    "III": {"w":"BDFHJLCPRTXVZNYEIWGAKMUSQO", "notch":"V"},
}
REFLECTORS = {
    "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT"
}

def wiring_to_map(w):
    return [ALPH.index(c) for c in w]

# Convert rotor wiring strings to numeric maps
for r in ROTORS:
    ROTORS[r]["map"] = wiring_to_map(ROTORS[r]["w"])
    # inverse map for reverse traversal
    inv = [0]*26
    for i, v in enumerate(ROTORS[r]["map"]):
        inv[v] = i
    ROTORS[r]["inv"] = inv

REFLECTOR_MAP = wiring_to_map(REFLECTORS["B"])

class Rotor:
    def __init__(self, name, position='A', ring=1):
        spec = ROTORS[name]
        self.map = spec["map"]
        self.inv = spec["inv"]
        self.notch = spec["notch"]
        self.pos = ALPH.index(position.upper())  # rotor window letter (0-25)
        self.ring = ring - 1  # ring setting (0-25)
    def at_notch(self):
        return ALPH[self.pos] in self.notch
    def step(self):
        self.pos = (self.pos + 1) % 26
    # forward mapping through rotor (entry from right -> left)
    def forward(self, c):
        # c: 0-25 entering at right side
        shifted = (c + self.pos - self.ring) % 26
        mapped = self.map[shifted]
        out = (mapped - self.pos + self.ring) % 26
        return out
    # reverse mapping through rotor (left -> right)
    def backward(self, c):
        shifted = (c + self.pos - self.ring) % 26
        mapped = self.inv[shifted]
        out = (mapped - self.pos + self.ring) % 26
        return out

class Enigma:
    def __init__(self, rotors, positions, rings, plugboard_pairs=""):
        # rotors: list like ["I","II","III"] left->middle->right
        self.left = Rotor(rotors[0], positions[0], rings[0])
        self.mid  = Rotor(rotors[1], positions[1], rings[1])
        self.right= Rotor(rotors[2], positions[2], rings[2])
        # build plugboard mapping
        self.plug = {c:c for c in ALPH}
        pairs = plugboard_pairs.upper().split()
        for p in pairs:
            if len(p)==2:
                a,b = p[0], p[1]
                self.plug[a] = b
                self.plug[b] = a

    def step_rotors(self):
        # double-step mechanism:
        if self.mid.at_notch():
            # middle at notch -> middle and left advance (double-step phenomenon)
            self.mid.step()
            self.left.step()
        elif self.right.at_notch():
            # right at notch -> middle advances
            self.mid.step()
        # right rotor always steps
        self.right.step()

    def enc_letter(self, ch):
        if ch not in ALPH: return ch
        # step before enciphering
        self.step_rotors()
        # plugboard in
        c = ALPH.index(self.plug[ch])
        # through rotors right->left
        c = self.right.forward(c)
        c = self.mid.forward(c)
        c = self.left.forward(c)
        # reflector
        c = REFLECTOR_MAP[c]
        # back through rotors left->right (inverse)
        c = self.left.backward(c)
        c = self.mid.backward(c)
        c = self.right.backward(c)
        # plugboard out
        out = self.plug[ALPH[c]]
        return out

    def process(self, text):
        text = text.upper()
        out = []
        for ch in text:
            if ch.isalpha():
                out.append(self.enc_letter(ch))
            else:
                out.append(ch)
        return "".join(out)

if __name__ == "__main__":
    # SETTINGS (change these)
    ROTOR_ORDER = ["I","II","III"]         # left, middle, right
    POSITIONS   = ["A","A","A"]            # initial window letters left->mid->right
    RINGS       = [1,1,1]                  # ring settings (1-26)
    PLUGBOARD   = "AV BS CG DL FU HZ IN KM OW"  # space-separated pairings (example)

    M = "HELLO WORLD"
    enigma = Enigma(ROTOR_ORDER, POSITIONS, RINGS, PLUGBOARD)
    cipher = enigma.process(M)
    print("Plain: ", M)
    print("Cipher:", cipher)

    # To decrypt, reinitialize Enigma with the SAME settings and feed the cipher text:
    enigma2 = Enigma(ROTOR_ORDER, POSITIONS, RINGS, PLUGBOARD)
    print("Decrypt:", enigma2.process(cipher))

