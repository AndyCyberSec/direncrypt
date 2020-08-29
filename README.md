# direncrypt
Direncrypt uses pyAesCrypt to recursively encrypt/decrypt files inside a directory.

# Usage:
## Encryption
`$ python3 direncrypt.py encrypt directory password` 

## Decryption
`$ python3 direncrypt.py decrypt directory password` 

## note
pyAesCrypt assume that a good password is at least 8 chars long and includes at least:
- 1 lowercase char
- 1 uppercase char
- 1 digit
- 1 symbol

It is recomended to not use clear text password in console. You can use a txt file this way:

```
$ python3 direncrypt.py encrypt directory $(cat /path/to(key.txt)
$ python3 direncrypt.py decrypt directory $(cat /path/to(key.txt)
```

Remember to save the key file in a safe place.

Once you installed pyAesCrypt you can also use it this way: https://github.com/marcobellaccini/pyAesCrypt

# Requirements
- pyAesCrypt
- fire
- progress

`pip3 install -r requirements.txt`
