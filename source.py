import cv2
from Crypto.Util.number import *
import random
import string
import numpy as np

def encrypt(msg):
	p = getPrime(512)
	q = getPrime(512)
	n = p*q
	phi = (p-1)*(q-1)
	e = 65537
	d = inverse(e,phi)
	print("RSA Keys: " + str([n,e,d]))
	return pow(bytes_to_long(msg),e,n)

def decrypt(ct,e,n,d):
	return pow(ct,d,n)

def rand_():
	return bin(random.randint(8,15))[2:]

def steg_encode_RGB(msg,inp,var):
	if var == 'Y':
		msg = bin(encrypt(msg.encode()))[2:]
	else:
		msg = bin(bytes_to_long(msg.encode()))[2:]
	img = cv2.imread(inp)
	if img.shape[0]*img.shape[1]*img.shape[2] < len(msg):
		return "[+] Error: Size of Message Exceeds Image Size!!!"
	k = 0
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			r,g,b = img[i,j]
			if k < len(msg):
				img[i,j,0] = int(bin(r)[:-1] + msg[k],2)
				k = k + 1
			if k < len(msg):
				img[i,j,1] = int(bin(g)[:-1] + msg[k],2)
				k = k + 1
			if k < len(msg):
				img[i,j,2] = int(bin(b)[:-1] + msg[k],2)
				k = k + 1
			else:
				break
	return img

def steg_encode_GrayScale(msg,inp,var):
	if var == 'Y':
		msg = bin(encrypt(msg.encode()))[2:]
	else:
		msg = bin(bytes_to_long(msg.encode()))[2:]
	img = cv2.imread(inp,0)
	if img.shape[0]*img.shape[1] < len(msg):
		return "[+] Error: Size of Message Exceeds Image Size!!!"
	k = 0
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			if k < len(msg):
				pix = bin(img[i,j])
				img[i,j] = int(pix[:-1] + msg[k],2)
				k = k + 1
			else:
				break
	return img

def steg_decode_RGB(inp,var,e=0,n=0,d=0,charset = string.printable):
	img = cv2.imread(inp,cv2.IMREAD_UNCHANGED)
	s = ''
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			for k in range(3):
				s = s + bin(img[i,j,k])[-1]
				if var == 'Y':
					string1 = long_to_bytes(decrypt(int('0b'+s,2),e,n,d)).decode('utf-8',errors = 'ignore')
					if all(c in charset for c in string1):
						print(string1)
				else:
					string1 = long_to_bytes(int('0b'+s,2)).decode('utf-8',errors = 'ignore')
					if all(c in charset for c in string1):
						print(string1)				

def steg_decode_GrayScale(inp,var,e=0,n=0,d=0,charset = string.printable): 
	img = cv2.imread(inp,0)
	k = ''
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			pix = bin(img[i,j])
			k = k + pix[-1]
			if var == 'Y':
				string1 = long_to_bytes(decrypt(int('0b'+k,2),e,n,d)).decode('utf-8',errors = 'ignore')
			else:
				string1 = long_to_bytes(int('0b'+k,2)).decode('utf-8',errors = 'ignore')
			if   all(c in charset for c in string1):
				print(string1)

def steg_hide_Image(inp1,inp2):
	img1 = cv2.imread(inp1)
	img2 = cv2.imread(inp2)
	if img1.shape != img2.shape:
		print("[+] Error: Size of Images Not Same")
		return 0
	for i in range(img1.shape[0]):
		for j in range(img1.shape[1]):
			for l in range(3):
				pix1 = format(img1[i][j][l], '08b')
				pix2 = format(img2[i][j][l], '08b')
				pix = pix1[:4] + pix2[:4]
				img1[i,j,l] = int(pix,2)
	return img1

def steg_extract_Image(inp):
	img = cv2.imread(inp)
	img1 = np.zeros((img.shape[0], img.shape[1],3),np.uint8)
	img2 = np.zeros((img.shape[0], img.shape[1],3),np.uint8)

	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			for l in range(3):
				pix = format(img[i][j][l], '08b')
				img1[i,j,l] = int(pix[:4] + rand_(),2)
				img2[i,j,l] = int(pix[4:] + rand_(),2)
	return img1,img2
			




