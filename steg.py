from source import *
import random
import string

def main():
	print("Options: ")
	print("[1]: STEG ENCODE DATA IN RGB IMAGES")
	print("[2]: STEG ENCODE DATA IN GRAYSCALE IMAGES")
	print("[3]: STEG ENCODE IMAGE IN RGB IMAGES")
	print("[4]: STEG DECODE DATA IN RGB IMAGES")
	print("[5]: STEG DECODE DATA IN GRAYSCALE IMAGES")
	print("[6]: STEG DECODE IMAGE IN RGB IMAGES")
	print("Enter Your Choice: ")
	option = int(input())
	if option == 1 or option == 2:
		print("Enter Secret Message: ")
		msg = str(input())
		print("Encrypt Message with RSA before Encoding?? [Y/N]")
		var = str(input())
		print("Enter Cover Image Path: ")
		inp = str(input())
		if option == 1:
			print("Steg Encode RGB Started...")
			img = steg_encode_RGB(msg,inp,var)
		if option == 2:
			print("Steg Encode GrayScale Started...")
			img = steg_encode_GrayScale(msg,inp,var)
		name = str(random.randint(1000,10000))
		ext = inp.strip().split('.')
		cv2.imwrite(name + '.' + ext[-1],img)
		print("Your New Image is: " + name + '.' + ext[-1])

	elif option == 3:
		print("Enter Cover Image Path")
		inp1 = str(input())
		print("Enter Secret Image Path")
		inp2 = str(input())
		img = steg_hide_Image(inp1,inp2)
		ext = inp1.strip().split('.')
		cv2.imwrite("secret."+ext[-1],img)
		print("Your New Image is: " + 'secret.' + ext[-1])

	elif option == 4 or option == 5:
		print("Enter Cover Image Path")
		inp = str(input())
		print("Is Message Encrypted? [Y/N]")
		var = str(input())
		if var == 'Y':
			print("Enter RSA keys as: [n,e,d]")
			print("n: ")
			n = int(input())
			print("e: ")
			e = int(input())
			print("d: ")
			d = int(input())
		else: 
			n,e,d = 0,0,0
		if option == 3:
			print("Steg Decode RGB Started...")
			steg_decode_RGB(inp,var,e,n,d,string.printable)
		if option == 4:
			print("Steg Decode GrayScale Started...")
			steg_decode_GrayScale(inp,var,e,n,d,string.printable)
	
	elif option == 6:
		print("Enter Cover Image Path")		
		inp = str(input())
		img1, img2 = steg_extract_Image(inp)
		ext = inp.strip().split('.')
		cv2.imwrite("img1.png",img1)
		cv2.imwrite("img2.png",img2)

	else:
		print("[+] Error: No Such Option Available")
		
main()



#LSB ENCODING OF DATA WORKS FOR PNG AND BMP IMAGES
#LSB ENCODING OF IMAGES WORKS WHEN BOTH IMAGE DIMENSIONS ARE SAME, AS WELL AS FILE EXTENSIONS ARE SAME

