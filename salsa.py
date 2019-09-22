#-*-coding: utf-8*-
from sys import argv
from optparse import OptionParser as opt
from pyperclip import copy

def banner():
	print('''
		 _____________
		|             |
		|    Taco     |
		|	&     |
		|     Salsa   |
		|_____________|

		[+]Github: https://github.com/binarioGH

		''')

def loadContent(file, hashf="unknown", cont=False):
	try:
		with open(file, "r") as f:
			content = f.read().split("\n")
	except:
		return -1
	else:
		if content[0][:27] != "# -*- Hash dictionary file:":
			return -2 
		if hashf != "unknown":
			hf = content[0].split(" ")[-1]
			if hashf.lower() != hf.lower():
				if not cont:
					return -3
				else:
					print("The hash function do not coincide.\nThe program will continue anyway.")
		new_content = {}
		for data in content[1:]:
			data = data.split("|")	
			data[0] = data[0].split()[0]
			data[1] = data[1].split()[0]
			new_content[data[1]] = data[0]
		del content
		return new_content


def main(args):
	op = opt("Usage: %prog [options] [values]")
	op.add_option("-H", "--hash", dest="hash", default="", type="string", help="Set the hash that you want to break.")
	op.add_option("-d", "--dictionary", dest="dfile", default="", type="string", help="Set the file that contains all the hashes.")
	op.add_option("-f", "--hashfunction", dest="function", default="unknown", type="string", help="Set the hash function name that you are attacking. [exp: md5]")
	op.add_option("-k", "--continueanyway", dest="cont", default=False, action="store_true", help="Continue attacking the hash even tho if it is not the same hash function.")
	op.add_option("-c", "--copyValue", dest="copy", default=False, action="store_true", help="If the hash value is found, copy it.")
	(o, args) = op.parse_args()
	if o.hash == "":
		print("You must define a hash...")
		return -1
	if o.dfile == "":
		print("You must define a dictionary file.")
		return -2
	else:
		content = loadContent(o.dfile, o.function, o.cont)
		if content == -1:
			print("The file do not exist.")
			return -3
		elif content == -2:
			print("The file is not a hash dictionary.")
			return -4
		elif content == -3:
			print("The hash function do not coincide.")
			if not o.cont:
				return -5
	print("Starting to search hash...")
	if o.hash in content:
		print("Hash value founded!!!!")
		print("Hash: {}".format(o.hash))
		print("Value: {}".format(content[o.hash]))
		if o.copy:
			copy(content[o.hash])
	else:
		print("The hash was not found in the file :(")
			



if __name__ == '__main__':
	banner()
	main(argv)