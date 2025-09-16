The Enigma encrypts a letter by passing current through a plugboard, a sequence of rotating rotors (each a fixed substitution with a rotational offset), a reflector, then back through the rotors and plugboard. Every key press advances rotors so the substitution changes with each letter. 

Rotor internals are fixed wirings (26-wire mappings) and each rotor has a notch that triggers the next rotor to step — this creates the famous “double-step” behaviour.

Notes about using the script:

Use the same machine settings (rotor order, ring settings, start positions, plugboard) to decrypt — Enigma is symmetric.

The script models rotor stepping including the double-step behavior (middle rotor stepping due to its notch).
