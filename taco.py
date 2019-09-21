#-*-coding: utf-8-*-
from itertools import product
from sys import argv
from optparse import OptionParser as opt
from codecs import open as copen
from time import strftime as time
from lib import *
getDate = lambda: time("%d-%m-%y-%H-%M-%S")

class PasswordGenerator:
	def __init__(self, upper=False, lower=False, title=False, alpha=False, mn=-1, mx=-1):
		self.passwordsList = []
		self.upper = upper
		self.lower = lower
		self.title = title
		self.alpha = alpha
		self.min = mn
		self.max = mx

	def __addPassword(self, password):
		if password in self.passwordsList:
			return -1
		else:
			self.passwordsList.append(password)
			return 0

	def generatePWords(self, words, lng):
		combinations = product(words, repeat=lng)
		for password in combinations: 
			password = "".join(password)
			lpass = len(password)
			if self.min != -1:
				if lpass < self.min:
					continue
			if self.max != -1:
				if lpass > self.max:
					continue
			self.__addPassword(password)
			if self.upper:
				self.__addPassword(password.upper())
			if self.lower:
				self.__addPassword(password.lower())
			if self.title:
				self.__addPassword(password.title())
			if self.alpha:
				self.__addPassword(alph4(password))

	def calpass(self, klen, n, m):
		total = 0
		for num in range(n,m+1):
			total += klen**num
		ftotal = total
		if self.upper:
			total += ftotal
		if self.lower:
			total += ftotal
		if self.title:
			total += ftotal
		if self.alpha:
			total += ftotal
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
	op.add_option("-u", "--upper", dest="upper", default=False, action="store_true", help="Create extra passwords in upper case. [PASSWORD]")
	op.add_option("-l", "--lower", dest="lower", default=False, action="store_true", help="Create extra passwords in lower case. [password]")
	op.add_option("-T", "--Title", dest="title", default=False, action="store_true", help="Create extra passwords starting with a capital letter. [Password]")
	op.add_option("-a", "--alphanumeric", dest="alpha", default=False, action="store_true", help="Create extra passwords in alpha numeric. [p455w0rd]")
	op.add_option("-M", "--maxLen", dest="maxlen", default=-1, type="int", help="Set the maximum length of the passwords. [-1 for not defined max len]")
	op.add_option("-N", "--minLen", dest="minlen", default=-1, type="int", help="Set the minumum length of the passwords. [-1 for not defined min len]")
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
	taco = PasswordGenerator(o.upper, o.lower, o.title, o.alpha, o.minlen, o.maxlen)
	print("Calculating ammount of passwords...")
	total_passwords = taco.calpass(len(keywords), o.min, o.max)
	print("Approximate ammount of passwords to generate: {}".format(total_passwords))
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
		taco.generatePWords(keywords, iterations)
	if iterations+1 == total_passwords:
			print("\n100% DONE!!!!!!!!!\n")
	print("Finishing at {}...".format(time("%H:%M:%S")))
	print("Total ammout of passwords: {}".format(len(taco.passwordsList)))
	permuted_words = "\n".join(taco.passwordsList)
	with copen(o.filename, "w", o.codec) as writeOutput:
		writeOutput.write(permuted_words)



if __name__ == '__main__':
	banner()
	main(argv)