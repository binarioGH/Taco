#-*-coding: utf-8-*-

def banner():
	print('''
            {}
	   |               |
	   |               |
	    -----     -----
	        |     |
	        |     |
	        |     | A C O
	        |     |
	        |     |
	        -------
	    [+] Github: https://github.com/binarioGH
		'''.format("_______________"))



def readKWF(self, file,encding="utf-8"):
	try:
		with copen(file, "r",  encding) as f:
			content = f.read().split()
	except:
		return -1
	else:
		return content

def alph4(word):
	lword = list(word)
	alphalow = {
	"a": 4,
	"l": 1,
	"b": 6,
	"o": 0,
	"q": 9,
	"g": 9
	}
	alpha = {
	"O": 0,
	"B": 8,
	"S": 5,
	"Z": 7	
	}
	for i in range(len(lword)):
		letter = lword[i]
		if not letter.isalpha():
			continue
		if letter.lower() == letter:
			if letter in alphalow:
				lword[i] = str(alphalow[letter])
		else:
			if letter in alpha:
				lword[i] = str(alpha[letter])
	return "".join(lword)
