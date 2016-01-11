import sys, wave

def rc4_wav(data, key, outdata):
    #generate key as KSA
    x = 0
    box = range(256)
    for i in range(256):
        x = (x + box[i] + ord(key[i % len(key)])) % 256
        box[i], box[x] = box[x], box[i]
    x = y = 0
    out = []

    #open wav file and get title from it
    data = wave.open(data, "rb")
    title = data.getparams()
    frame_number = data.getnframes()
    #get the data from the wav file
    d = data.readframes(frame_number)
    #open the output wav file
    new_data = wave.open(outdata, "wb")
    new_data.setparams(title)
    #write encrypted or decrypted data in it
    for char in d:
        x = (x + 1) % 256
        y = (y + box[x]) % 256
        box[x], box[y] = box[y], box[x]
        new_data.writeframes(chr(ord(char) ^ box[(box[x] + box[y]) % 256]))
    
    data.close()
    new_data.close()

def rc4_file(data, key, outdata):
    x = 0
    box = range(256)
    for i in range(256):
        x = (x + box[i] + ord(key[i % len(key)])) % 256
        box[i], box[x] = box[x], box[i]
    x = y = 0
    f = open(data, "r")
    d = f.read()
    outdata = open(outdata, "w")
    for char in d:
        x = (x + 1) % 256
        y = (y + box[x]) % 256
        box[x], box[y] = box[y], box[x]
        outdata.write(chr(ord(char) ^ box[(box[x] + box[y]) % 256]))

    f.close()
    outdata.close()

def encrypt(key, plainfile, cipherfile):
    """RC4 encryption with random salt and final encoding"""
    s = plainfile.split('.')
    if s[1] == 'wav':
        rc4_wav(plainfile, key, cipherfile)
    else:
        rc4_file(plainfile, key, cipherfile)

def decrypt(key, cipherfile, decryptfile):
    """RC4 decryption of encoded data"""
    s = cipherfile.split('.')
    if s[1] == 'wav':
        rc4_wav(cipherfile, key, decryptfile)
    else:
        rc4_file(cipherfile, key, decryptfile)

if __name__ == '__main__':
    k = sys.argv[1]
    f = sys.argv[2]
    enc = sys.argv[3]
    dec = sys.argv[4] 
    encrypt(k, f, enc)
    decrypt(k, enc, dec)