#-*-coding: utf-8-*-
from itertools import product
from sys import argv
from optparse import OptionParser as opt
from codecs import open as copen
from time import strftime as time
from lib import *
getDate = lambda: time("%d-%m-%y-%H-%M-%S")
def readKWF(file,encding="utf-8"):
	try:
		with copen(file, "r",  encding) as f:
			content = f.read().split()
	except:
		return -1
	else:
		return content

def generatePWords(words, lng):
	combinations = product(words, repeat=lng)
	passwords = []
	for password in combinations: 
		password = "".join(password)
		passwords.append(password)
	return passwords

def calpass(klen, n, m):
	total = 0
	for num in range(n,m+1):
		total += klen**num
	return total
		

def main(args=[]):
	op = opt("Usage: %prog [flags] [values]")
	op.add_option("-k", "--keywords", dest="keywords", default=" ", type="string",help="Introduce a list of keywords separeted by commas. exp: -k hello,world,1985 == ['hello', 'world', '1985']")
	op.add_option("-d", "--keywordsfile",dest="keywordsfile", default=0, type="string",help="Select a file with a list of keywords.")
	op.add_option("-c", "--kwfile_codec", dest="codec", default="utf-8", help="Select a codec for your keyword file. (default is utf-8)")
	op.add_option("-o", "--dictionaryName",dest="filename", default="{}.txt".format(getDate()), help="Select a name for the output file.")
	op.add_option("-n", "--min", dest="min", default=1, type="int", help="Define the minimum number of combinations for each iteration. (predefined as 1)")
	op.add_option("-m", "--max", dest="max", default=5, type="int", help="Define the maximum number of combinations for each iteration. (predefined as 5)")
	op.add_option("-t", "--total", dest="total", default=-1, type="int", help="Break the password generator after X iterations.")
	(o, args) = op.parse_args()
	keywords = []

	if o.keywordsfile != 0:
		result = readKWF(o.keywordsfile, o.codec)
		if result == -1: 
			print("There was a problem opening the file.")
			return -1
		keywords += result
	if o.keywords != " ":
		o.keywords = o.keywords.split(",")
		keywords += o.keywords
	if len(keywords) == 0:
		print("You must define some keywords...")
		return -2
	permuted_words = []
	print("Calculating ammount of passwords...")
	total_passwords = calpass(len(keywords), o.min, o.max)
	print("Total ammount of passwords to generate: {}".format(total_passwords))
	print("Starting to generate passwords at {}...".format(time("%H:%M:%S")))
	for iterations in range(o.min, o.max+1):
		if iterations == int(total_passwords * 0.25):
			print("\n25% DONE!\n")
		elif iterations == int(total_passwords * 0.50):
			print("\n50% DONE!\n")
		elif iterations == int(total_passwords * 0.75):
			print("\n75% DONE!\n")
		elif iterations == o.total:
			break
		permuted_words += generatePWords(keywords, iterations)
	if iterations+1 == total_passwords:
			print("\n100% DONE!!!!!!!!!\n")
	print("Finishing at {}...".format(time("%H:%M:%S")))
	permuted_words = "\n".join(permuted_words)
	with copen(o.filename, "w", o.codec) as writeOutput:
		writeOutput.write(permuted_words)



if __name__ == '__main__':
	banner()
	main(argv)