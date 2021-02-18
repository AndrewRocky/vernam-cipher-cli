import argparse

# returns True if char is in English alphabet
def isEnglish(char):
    if 'a' <= char <= 'z':
        return True
    else:
        return False

#chr(97) = a
def vernam_gamma_crypt(text, key, decrypt_mode=False):
    text = text.lower()
    key = key.lower()

    alph_strength = 26 #set alphabet strength
    offset = 97 # offset (e.g since ord('a')=97 -> offset=96)
    result = ""

    #check for wrong symbols in input
    if not(all(isEnglish(x) or x.isspace() for x in text)):
        raise ValueError("Wrong symbols in original text!")
    if not(all(isEnglish(x) for x in key)):
        raise ValueError("Wrong symbols or spaces in private key!")
    
    i=0
    for char in text:
        gamma = ord(key[i%len(key)]) - offset
        if char == " " or char == "\n":
            result += char
            continue
        char = ord(char) - offset
        if decrypt_mode:
            intermed_result = (alph_strength + char - gamma)%alph_strength
        else: # encrypt mode
            intermed_result = (char + gamma) % alph_strength
        result += chr(intermed_result + offset)
        i += 1

    return result

parser = argparse.ArgumentParser(description="Powerless tool for encryption/decryption in Vernam's cypher")
parser.add_argument('-i', "--input", required=True, help="Input file")
parser.add_argument('-k', "--key", required=True, help="Private key input file")
parser.add_argument('-o', "--output", required=True, help="Output file")
mode_group = parser.add_mutually_exclusive_group(required=True)
mode_group.add_argument("-e", "--encrypt", action="store_true", help="encryption mode")
mode_group.add_argument("-d", "--decrypt", action="store_true", help="decryption mode")

args = parser.parse_args()

print("Reading text from", args.input)
input_file = open(args.input, 'r').read()
print("Reading key from", args.key)
key_file = open(args.key, 'r').read()
print("Writing to", args.output)
with open(args.output, "w+") as output_file:
    if args.encrypt:
        print("Encryption mode...")
        result = vernam_gamma_crypt(input_file, key_file, False)
    elif args.decrypt:
        print("Decryption mode...")
        result = vernam_gamma_crypt(input_file, key_file, True)
    else:
        raise ValueError("Error in CLI arguments.")
    print("result:", result)
    print(result, file=output_file)



