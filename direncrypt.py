#!/usr/local/bin/python3

import fire
import sys
import os
import pyAesCrypt
from progress.bar import Bar
from multiprocessing import Pool, current_process
from functools import partial

maxPassLen = 1024  # maximum password length (number of chars)

# encryption/decryption buffer size - 64K
bufferSize = 64 * 1024


def getListOfFiles(dirName):

	# create a list of file and sub directories 
	# names in the given directory 
	listOfFile = os.listdir(dirName)
	allFiles = list()
	# Iterate over all the entries
	for entry in listOfFile:
		# Create full path
		fullPath = os.path.join(dirName, entry)
		# If entry is a directory then get the list of files in this directory 
		if os.path.isdir(fullPath):
			allFiles = allFiles + getListOfFiles(fullPath)
		else:
			allFiles.append(fullPath)
		
	return allFiles 


def encrypt_pool(listOfFiles, password):

	bar = Bar(current_process().name, max=len(listOfFiles))
	for elem in listOfFiles:
		ofname = elem + ".aes"
		try:
			pyAesCrypt.encryptFile(elem, ofname, password, bufferSize)
			os.remove(elem)
			bar.next()
		# handle IO errors
		except IOError as ex:
			exit(ex)
		# handle value errors
		except ValueError as ex:
			exit(ex)
	bar.finish()


def decrypt_pool(listOfFiles, password):

	bar = Bar(current_process().name, max=len(listOfFiles))
	for elem in listOfFiles:
		# open aes file
		ofname = ""
		if elem.endswith(".aes"):
			ofname = elem[:-4]

		if len(ofname) != 0:
			# call decryption function
			try:
				pyAesCrypt.decryptFile(elem, ofname, password, bufferSize)
				os.remove(elem)
				bar.next()
			# handle IO errors
			except IOError as ex:
				exit(ex)
			# handle value errors
			except ValueError as ex:
				exit(ex)
	bar.finish()	

	

def encrypt(directory, password):

	if checks(directory, password):
		# Get the list of all files in directory tree at given path
		print(f"Please wait while collecting files in {directory}...")
		listOfFiles = getListOfFiles(directory)

		n_key = len(listOfFiles)
		chunks = [listOfFiles[x:x+128] for x in range(0, n_key, 128)]
		pool = Pool(processes=8)

		print("")
		print('Encrypting files:')

		pool.map(partial(encrypt_pool, password=password), chunks)
		pool.close()


def decrypt(directory, password):

	if checks(directory, password):
		# Get the list of all files in directory tree at given path
		print(f"Please wait while collecting files in {directory}...")
		listOfFiles = getListOfFiles(directory)

		n_key = len(listOfFiles)
		chunks = [listOfFiles[x:x+128] for x in range(0, n_key, 128)]
		pool = Pool(processes=8)

		print("")
		print('Decrypting files:')

		pool.map(partial(decrypt_pool, password=password), chunks)
		pool.close()


def check_password(passw):

# Check password complexity
# here assume that a good password is at least 8 chars long
# and includes at least:
# 1 lowercase char
# 1 uppercase char
# 1 digit
# 1 symbol
	if not((len(passw) > 7) and (len(passw) <= maxPassLen) and any(c.islower() for c in passw) and any(c.isupper() for c in passw) and any(c.isdigit() for c in passw) and any(not(c.isalnum()) for c in passw)):
		print("Warning: your password seems weak.")
		print("A password should be at least 8 chars long and should contain at least one lowercase char, one uppercase char, one digit and one symbol.")
		return False
	else:
		return True

def checks(directory, password):
	
	if check_password(password):
		if os.path.exists(directory):
			return True
	
	return False
        
if __name__ == '__main__':
    fire.Fire({'encrypt': encrypt,'decrypt': decrypt,})
