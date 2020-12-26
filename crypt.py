from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from binascii import hexlify

def generateNewKeys():

#Generating private key (RsaKey object) of key length of 1024 bits

    private_key= RSA.generate(1024)
    public_key=private_key.publickey()

    private_pem = private_key.export_key().decode()
    public_pem = public_key.export_key().decode()

    with open('private_pem.pem', 'w') as pr:
        pr.write(private_pem)
    with open('public_pem.pem', 'w') as pu:
        pu.write(public_pem)

    return(public_pem)

#sets the key for encryption-exchanged public key.
def setEncryptionKey(newKey):
    with open('encryption_key.pem','w') as encKey:
        encKey.write("-----BEGIN PUBLIC KEY-----\n"+newKey+"\n-----END PUBLIC KEY-----")

def encrypt(message):
    try:
        pu_key = RSA.import_key(open('encryption_key.pem', 'r').read())
        cipher = PKCS1_OAEP.new(key=pu_key)
        cipher_text = cipher.encrypt(message.encode())
        return(cipher_text.hex())

    except:
        print("Something went wrong. Check if encryption key file \'encryption_key.pem\' exists. If not, select option [3] and set it up.")

def getPublicKey():
    file=open('public_pem.pem','r')
    lines = file.readlines()
    #a really shitty way to get a key from file:
    key=""
    for i in range(1,len(lines)-1):
        key+=lines[i].replace('\n','')
    return(key)

def decrypt(message):
    try:
        pr_key = RSA.import_key(open('private_pem.pem', 'r').read())
        decrypt = PKCS1_OAEP.new(key=pr_key)
        decrypted_message = decrypt.decrypt(bytes.fromhex(message))
        return(decrypted_message.decode())
    except:
        print("Something went wrong. Check if the file \'private_pem.pem\' exists. If not, select option [4] to set it up.")
while True:
    print("\n[1]ENCRYPT\n[2]DECRYPT\n[3]SET NEW ENCRYPTION KEY\n[4]GENERATE KEYS\n[5]MY PUBLIC KEY?\n[6]HELP\n[0]EXIT")
    inp=int(input())

    if inp==1:
        print("Message: ",end='')
        inp=input()
        print("encrypting...")
        print("Encrypted message:",encrypt(inp))

    elif inp==2:
        print("Message to decrypt: ",end='')
        inp=input()
        print("Processing...")
        print("Decrypted message:",decrypt(inp))

    elif inp==3:
        print("Paste new encryption key to be used: ",end='')
        inp=input()
        setEncryptionKey(inp)
        print("Encryption key has been updated.")

    elif inp==4:
        print("Generating your new pair of keys...")
        new_public_key=generateNewKeys()
        print("Send your peer the following key:")
        #print(new_public_key)
        print(getPublicKey())

    elif inp==5:
        print("YOUR PUBLIC KEY:",getPublicKey())

    elif inp==6:
        print("Steps to useability: \n\t1)Generate a key - option [4]\n\t2)All participants shall include the generated key under option [3]\n\t3)Enjoy your critography")

    elif inp==0:
        print("Exiting")
        break

    else:
        print("fck u")
