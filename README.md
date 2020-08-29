# direncrypt
Python wrapper around pyAesCrypt to encrypt files inside directory recursively.

# Usage:
## Encryption
`$ direncrypt.py encrypt directory password` 

## Decryption
`$ direncrypt.py decrypt directory password` 

pyAesCrypt assume that a good password is at least 8 chars long and includes at least:
- 1 lowercase char
- 1 uppercase char
- 1 digit
- 1 symbol

It is recomended to not use clear text password in console. You can use a txt file this way:
`$ ./direncrypt.py encrypt directory $(cat /path/to(key.txt)`
`$ ./direncrypt.py decrypt directory $(cat /path/to(key.txt)`

Remember to save the key file in a safe place.

# Requirements
pyAesCrypt
fire
progress.bar
