import os,time,zlib,base64
from time import sleep
from sys import stdin, stdout, stderr
from argparse import ArgumentParser
from pathlib import Path
from base64 import b64decode
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import unpad
from Crypto.Cipher import AES, Blowfish
from Crypto.Util.Padding import unpad
from base64 import b64decode
from urllib.parse import unquote
import re,sys

DEFAULT_FILE_EXTENSION = '.tmt'

def sshinjector(file:str,key:bytes=b'263386285977449155626236830061505221752'):
    text = b64decode(open(file,'rb').read())
    iv = b'\x00\x01\x02\x03\x04\x05\x06\x07'
    cipher = Blowfish.new(key, Blowfish.MODE_CBC,iv)
    plaintext = cipher.decrypt(text)
    decrypt_text = unpad(plaintext, Blowfish.block_size).decode() # remove pkcs#7
    
    pattern = r'<entry key="(.*)">(.*)</entry>'
    match = re.findall(pattern, decrypt_text)
    for i in match:
        key,value = i
        print(f"[>]  {key} ⦔ {value}")
#ssh injektor

# passwords to derive the key from
PASSWORDS = {
       '.ziv': b'fubvx788b46v',
       '.tnl': b'B1m93p$$9pZcL9yBs0b$jJwtPM5VG@Vg',  #✓
       '.pb': b'Cw1G6s0K8fJVKZmhSLZLw3L1R3ncNJ2e',  #✓
       '.hqp': b'Ed',     #✓
       '.hq': b'Ed', 
       '.bdi': b'@technore 2022',
       '.nti': b'Ed', 
       
}

# some utility functions
def error(error_msg = 'Corrupted/unsupported file.'):
    stderr.write(f'\033[41m\033[30m X \033[0m {error_msg}\n')
    stderr.flush()

    exit(1)

def warn(warn_msg):
    stderr.write(f'\033[43m\033[30m ! \033[0m {warn_msg}\n')
    stderr.flush()

def ask(prompt):
    stderr.write(f'\033[104m\033[30m ? \033[0m {prompt} ')
    stderr.flush()

    return input()

def human_bool_to_bool(human_bool):
    return 'y' in human_bool

def main():
    # parse arguments
    parser = ArgumentParser()
    parser.add_argument('file', help='file to decrypt')

    output_args = parser.add_mutually_exclusive_group()
    output_args.add_argument('--output', '-o', help='file to output to')
    output_args.add_argument('--stdout', '-O', action='store_true', help='output to stdout', default=True)

    args = parser.parse_args()

    # open file
    encrypted_contents = open(args.file, 'r').read()

    # determine the file's extension
    file_ext = Path(args.file).suffix
    
    if file_ext not in PASSWORDS:
        warn(f'Unknown file extension, defaulting to {DEFAULT_FILE_EXTENSION}')
        file_ext = DEFAULT_FILE_EXTENSION

    # split the file
    split_base64_contents = encrypted_contents.split('.')

    #if len(split_base64_contents) != 3:
        #raise ValueError('Unsupported file.')

    split_contents = list(map(b64decode, split_base64_contents))
    #split_contents= encrypted_contents.split('.')
   

    # derive the key
    decryption_key = PBKDF2(PASSWORDS[file_ext], split_contents[0], hmac_hash_module=SHA256)

    # decrypt the file
    cipher = AES.new(decryption_key, AES.MODE_GCM, nonce=split_contents[1])
    decrypted_contents = cipher.decrypt_and_verify(split_contents[2][:-16], split_contents[2][-16:])

    # decide where to write contents
    if args.output:
        output_file_path = Path(args.output)

        # check if the file exists
        if output_file_path.exists() and output_file_path.is_file():
            # check if the user agrees to overwrite it
            if not human_bool_to_bool(ask(f'A file named "{args.output}" already exists. Overwrite it? (y/n)')):
                # if user doesn't, quit
                exit(0)
        
        # write the contents to the file
        output_file = open(output_file_path, 'wb')
        output_file.write(decrypted_contents)
    elif args.stdout:
        # convert the config to UTF-8
        config = decrypted_contents.decode('utf-8','ignore')
        #print(config)
        
        
        sshadd ='';port ='';user='';passw=''
        configdict ={}
        for line in config.split('\n'):
        	if line.startswith('<entry'):
        		line = line.replace('<entry key="','')
        		line = line.replace('</entry','')
        		line = line.split('">')
        		if len(line) >1:
        			configdict[line[0]] = line[1].strip(">")
        			
        		else:
        			configdict[line[0].strip('"/>')]= " ***"
        			#print(f'[>] {line} ==> X')
        for k,v in configdict.items():
        	if k in ["sshServer","sshPass","sshUser","sshPort"]:
        		continue
        	else:
        		print("[*] [" +k+ "] : " +v)

if __name__ == '__main__':
    print('\n\n\nRead Config By KMKZ™ Tools\n* t.me/EstebanZxx\n* t.me/XDecrytorID\n==========================') 
    args = sys.argv    
    file = args[1]
    if file.split('.')[1] == 'ssh':
            sshinjector(file)
            
    try:
        main()
    except Exception as err:
        error(err)