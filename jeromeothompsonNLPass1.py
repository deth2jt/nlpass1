import re
from math import log 

def getLetters(corpus):
	textfile = open(corpus, 'r')
	sentences = re.split(r'([.?!]\s*|[.]{0,50}\r)', textfile.read())
	
	characters = []
	#for index in range(len(sentences)-2):
	for index in range(2):
		sentence = sentences[index]
		pattern = re.compile('[.!,?"/\r]')
		newSentence = pattern.sub('', sentence)
		characters += ['<s>'] + list(newSentence) + ['</s>']

	textfile.close()
	return characters

def getWords(corpus):
	textfile = open(corpus, 'r')
	sentences = re.split(r'([.?!]\s*|[.]{0,50}\r)', textfile.read())
	
	sentenceCleaned = []
	#for index in range(len(sentences)-2):
	for index in range(len(sentences)-2):
		sentence = sentences[index]
		sentence = re.sub('[.;!,?"\r]', '',sentence)
		patternStr2='(\r||. |.\r)+'
		completePat='^'+patternStr2+'$'
		#print("pattern ", completePat)
		match = re.findall(completePat, sentence)
		#if(len(match) > 0):
			#print("bb: ", re.findall(completePat, sentence) )
			#print("dsfhs", sentence)
		#if(not(len(match) > 0) ):
		if((len(sentence) > 0) and sentence != " " ):
			#print(sentence)
			sentenceCleaned += ['<s> ' + sentence + ' </s>']
		#sentence = sentences[index]
		#if(sentence)
	#textfile.close()
	#print("sentenceCleaned", sentenceCleaned[0])
	return sentenceCleaned


def getBigramLetter(characters):
	count = 0
	unigram = dict()
	bigram = dict()
	total_prob = 0

	prev = characters[0]
	unigram.update( {prev:1} )
	for index in range(1,len(characters)):
		curr = characters[index]

		if(unigram.has_key(curr)):
			count = unigram.get(curr)
			unigram.update( {curr: count+1}  )
		else:
			unigram.update( {curr: 1}  )


		comb = (prev, curr) 

		if(bigram.has_key(comb)):
			count = bigram.get(comb)
			bigram.update( {comb: count+1}  )
		else:
			bigram.update( {comb: 1}  )
		prev = curr
	return (bigram, unigram)

def getBigramWord(sentences):
	count = 0
	#unigram = dict()
	unigram = dict()
	bigram = dict()
	total_count = 0

	
	
	for index in range(0,len(sentences)):
		words = sentences[index].split()
		#words = sentences[index]
		firstWord = words[0]
		

		for index in range(1,len(words)):
			firstWorduni = words[index]
			if(unigram.has_key(firstWorduni)):
				count = unigram.get(firstWorduni)
				unigram.update( {firstWorduni: count+1}  )
			else:
				unigram.update( {firstWorduni: 1}  )
				


		#total_count = 1
		for index in range(1,len(words)):
			total_count += 1
			currWord = words[index]




			

			comb = (firstWord, currWord) 

			if(bigram.has_key(comb)):
				count = bigram.get(comb)
				bigram.update( {comb: count+1}  )
			else:
				bigram.update( {comb: 1}  )
			firstWord = currWord
		total_count += 1		
	gtDict = dict()

	for key, value in bigram.items():
		#total_count += value
		if(gtDict.has_key(value)):
			count = gtDict.get(value)
			gtDict.update( {value: count+1}  )
		else:
			gtDict.update( {value: 1}  )

	#print("111", gtDict.get(1))
	return (bigram, gtDict, total_count, unigram)



def getTrigramWord(sentences):
	count = 0
	lamdaNumerator = dict()
	trigram = dict()
	PContNumerator = dict()

	#total_count = 0

	
	for index in range(0,len(sentences)):
		words = sentences[index].split()
		#words = sentences[index]
		firstWord = words[0]
		secWord = words[1]

		#bigramfirst = 
		total_count = 2
		for index in range(2,len(words)):
			
			currWord = words[index]

			

			comb = (firstWord, secWord, currWord) 

			if(trigram.has_key(comb)):
				count = trigram.get(comb)
				trigram.update( {comb: count+1}  )
			else:
				trigram.update( {comb: 1}  )
			firstWord = secWord
			secWord = currWord

			#total_count = total_count + 1
		
	for key, value in trigram.items():
		#total_count += value
		value= (key[0],key[1])

		if(lamdaNumerator.has_key(value)):
			count = lamdaNumerator.get(value)
			lamdaNumerator.update( {value: count+1}  )
		else:
			lamdaNumerator.update( {value: 1}  )

		#total_count += value
		value= (key[2])

		if(PContNumerator.has_key(value)):
			count = PContNumerator.get(value)
			PContNumerator.update( {value: count+1}  )
		else:
			PContNumerator.update( {value: 1}  )
	#print("111", gtDict.get(1))
	return (trigram, lamdaNumerator, PContNumerator)



def getProb(string, Unibigram):
	unigram = Unibigram[1]
	bigram = Unibigram[0]

	#print("UnibigramUnibigramUnibigramUnibigramUnibigram", Unibigram)
	characters = list(string)
	prev = characters[0]
	total_prob = 0
	#print("characterscharacterscharacters", characters)

	for index in range(1,len(characters)):
		curr = characters[index]
		pair= (prev,curr)

		countPrevCurr = bigram.get(pair) 
		if not countPrevCurr is None:
			numerator = countPrevCurr 
			prob = numerator/float(len(unigram))
			total_prob += log(float(prob), 2)
		#denominator = unigram.get(pair[0])
		'''
		if denominator is None:
			#denominator =  0
			prob = 0
		else:
			
			'''

		#total_prob = total_prob  * prob
		#total_prob += log(float(prob), 2)

		prev = curr
	return total_prob 



#TODO
def getAddOneProb(string, bigram, unigram):

	#print("UnibigramUnibigram", unigram)
	string = re.sub('[.;!,?"]', '',string)
	words = string.split()
	#words = re.sub('[.;!,?"]', '',words)
	words[0] = "<s>"
	words += ["</s>"]
	total_prob = 0
	prev = words[0]
	for index in range(1,len(words)):
		curr = words[index]
		pair= (prev,curr)

		countPrevCurr = bigram.get(pair) 		
		if countPrevCurr is None:
			numerator =  1
		else:
			numerator = countPrevCurr + 1
		
		countPrev = unigram.get(prev)
		if countPrev is None:
			denominator =  len(unigram)
		else:
			denominator = float(unigram.get(prev)) + len(unigram)

		
		probAddOne = numerator/float(denominator)
		total_prob += log(probAddOne, 2)

		prev = curr
	return total_prob 

#getKneserNey(line, engTrigram, engbigram, lamdbaVar,pContVar)
def getKneserNeyProb(string, trigram, bigram, lamdbaVar, pContVar, d):
	string = re.sub('[.;!,?"]', '',string)
	words = string.split()
	#words = re.sub('[.;!,?"]', '',words)
	words[0] = "<s>"
	words += ["</s>"]
	#print("wordswordswords", words)
	#prevWord = re.sub('[.;!,?"]', '',prevWord)
	#print("trigramtrigramtrigram",trigram)
	#print("bigrambigrambigram",bigram)

	prev = words[0]
	sec = words[1]
	#print("secsecsecsec",sec)
	#prev = re.sub('[.;!,?"]', '',prev)
	#d = 0.75 

	total_prob = 0

	for index in range(2,len(words)):
		curr = words[index]
		pairTrig= (prev,sec,curr)
		pairBi= (prev,sec)

		countTrig = trigram.get(pairTrig) 
		countBi =bigram.get(pairBi)

		countBiIsh =lamdbaVar.get(pairBi)
		last =pContVar.get(sec)
		'''
		print("pairTrig", pairTrig)
		print("countTrig", countTrig)
		print("countBi", countBi)
		print("countBiIsh", countBiIsh)
		print("last", last)
		'''
		if(countTrig is None):
			countTrig = 0
		if(countBiIsh is None):
			countBiIsh = 0
		if(last is None):
			last = 0

		if(countBi is None):
			firstPart = 0
			secondPart = 0
		else:
			firstPart = max(countTrig - d, 0) / float(countBi)
			secondPart = float(d)/countBi*countBiIsh
		

		

		
		thirdPart = float(last)/len(trigram)

		

		
		probKN = float(firstPart) + float(secondPart * thirdPart)

		if(probKN != 0):
			total_prob += log(probKN, 2)
			#print("log(probKN, 2)log(probKN, 2)", log(probKN, 2))

		prev = sec
		sec = curr
		#print("total_probKNNKNKNKN", total_prob)
	return total_prob 

def getGoodTuringProb(string, bigram, ncDict, total_count):
	#Katz (1987) suggests setting k at 5. Thus we define
	k =7
	words = string.split()
	words[0] = "<s>"
	words += ["</s>"]
	
	prevWord = words[0]
	total_prob = 0
	cStar = 0

	
	prevWord = re.sub('[.;!,?"]', '',prevWord)
	

	#print("nnnnn",   words) 

	for index in range(1,len(words)):
		totalWord = 0


		#for key,value in bigram.items():
			#if(key[0] ==prevWord):
				#totalWord += value
		for key,value in ncDict.items():
			totalWord += value

		currWord = words[index]
		currWord = re.sub('[.;!,?"]', '',currWord)

		pair=(prevWord,currWord)

		#print("currWord", currWord)
		#if(pair == ('of', 'wine')):
			#print("ofwiensdsgdhgsh", bigram.get(('of', 'wine'))    ) 
		c = bigram.get(pair) 
		
		if(c is None):
			c = 0
		ncplus1 = ncDict.get(c+1) 
		if(ncplus1 is None):
			c = 0

		nc= ncDict.get(c) 
		#if(nc is None):
			#c = 0

		
		#print("c", c)
		if(c > k):
			#print("ncDict.get(c+1)",ncDict.get(c+1)) 
			#print("pair", pair)
			#print("cccc",c) 
			
			val = float( ncplus1 ) / float(nc)
			cStar = float(c+1)* val
			probGT = float(cStar)/float(total_count)
			#probGT = float(nc) / float(totalWord)
			#print("sdfsd")
		else:
			if(c == 0):
				#probGT = float(ncDict.get(1))/float(total_count)
				probGT = float(ncDict.get(1))/float(total_count)
				#print("asdasd")

			else:
				#print("k",k)
				#print("sadsdas")
				numuerator1 = float(c+1)* (  float(ncplus1)    /    float(nc)    )
				numuerator2 =        (k+1) * float(ncDict.get(k+1) )    / float(ncDict.get(1)  )  
				numuerator = float(numuerator1) - (float(c) * float(numuerator2))
				denominator = float(1) - (  float(k+1) * float(ncDict.get(k+1) )    / float(ncDict.get(1))   )
				cStar = float(numuerator)/float(denominator)
				probGT = float(cStar)/float(totalWord)

		prevWord = currWord
		#if(probGT == 0):
			#print("probGT",probGT)
			#print("c",c)
			#print("cStar",cStar)
		total_prob += float(log(probGT, 2))

		
	return total_prob 	



if __name__ == '__main__':
	characters = getLetters('EN.txt')
	#print("characters", characters)
	#print(characters)
	englishUniBigram = getBigramLetter(characters)
	#print(re.split('(\W+)', 'Words, words, words.'))

	characters = getLetters('FR.txt')
	frenchUniBigram = getBigramLetter(characters)

	characters = getLetters('GR.txt')
	germanUniBigram = getBigramLetter(characters)

	testfileName = "LangID.test.txt"
	testfile = open(testfileName, "r")

	
	

	engbigram = getBigramWord(getWords('EN.txt'))[0]
	engncDict = getBigramWord(getWords('EN.txt'))[1]
	engncTotal = getBigramWord(getWords('EN.txt'))[2]
	engUnigram = getBigramWord(getWords('EN.txt'))[3]

	frbigram = getBigramWord(getWords('FR.txt'))[0]
	frncDict = getBigramWord(getWords('FR.txt'))[1]
	frgncTotal = getBigramWord(getWords('FR.txt'))[2]
	frUnigram = getBigramWord(getWords('FR.txt'))[3]

	grbigram = getBigramWord(getWords('GR.txt'))[0]
	grncDict = getBigramWord(getWords('GR.txt'))[1]
	grgncTotal = getBigramWord(getWords('GR.txt'))[2]
	grUnigram = getBigramWord(getWords('GR.txt'))[3]

	#print(grncDict)

	#return (bigram, lamdaNumerator, PContNumerator)
	engTrigram = getTrigramWord(getWords('EN.txt'))[0]
	englamdbaVar = getTrigramWord(getWords('EN.txt'))[1]
	engpContVar = getTrigramWord(getWords('EN.txt'))[2]

	frTrigram = getTrigramWord(getWords('FR.txt'))[0]
	frlamdbaVar = getTrigramWord(getWords('FR.txt'))[1]
	frpContVar = getTrigramWord(getWords('FR.txt'))[2]

	grTrigram = getTrigramWord(getWords('GR.txt'))[0]
	grlamdbaVar = getTrigramWord(getWords('GR.txt'))[1]
	grpContVar = getTrigramWord(getWords('GR.txt'))[2]
	#engKN = getKneserNey(line, engTrigram, engbigram, lamdbaVar,pContVar)
	#print("pContVarpContVar", pContVar)
	

	solutionLetterFile = open("solutionLetter.out", 'w')
	solutionAddOnefile = open("solutionAddOne.out", 'w')
	solutionGTfile = open("solutionGT.out", 'w')
	solutionKN = open("solutionKN.out", 'w')

	testCurrfile = re.split(r'\r', testfile.read())
	
	
	outputKN  = "ID LANG\n"
	output  = "ID LANG\n"
	outputGT = 'ID LANG\n'
	probList = "ID LANG\n"

	

	for index in range(len(testCurrfile)):
	#for index in range(20):
		line = testCurrfile[index]
		
		
		eng = getProb(line, englishUniBigram)
		fren = getProb(line, frenchUniBigram)
		germ = getProb(line, germanUniBigram)

		
		'''
		engAddone = getAddOneProb(line, englishUniBigram)
		frenAddone = getAddOneProb(line, frenchUniBigram)
		germAddone = getAddOneProb(line, germanUniBigram)
		'''
		engAddone = getAddOneProb(line, engbigram, engUnigram)
		frenAddone = getAddOneProb(line, frbigram, frUnigram)
		germAddone = getAddOneProb(line, grbigram, grUnigram)

		engGT = getGoodTuringProb(line, engbigram, engncDict, engncTotal)
		frGT = getGoodTuringProb(line, frbigram, frncDict, frgncTotal)
		grGT = getGoodTuringProb(line, grbigram, grncDict, grgncTotal)

		
		d = 0.75
		engKN = getKneserNeyProb(line, engTrigram, engbigram, englamdbaVar,engpContVar, d)
		frKN = getKneserNeyProb(line, frTrigram, frbigram, frlamdbaVar,frpContVar, d)
		grKN = getKneserNeyProb(line, grTrigram, grbigram, grlamdbaVar,grpContVar, d)

		#print( index + 1,engGT, frGT, grGT)
		
		value = max( eng, fren, germ)

		if( value == eng): 
			probList +=  (str(index+1) + ". EN\n")
		elif (value == fren): 
			probList +=  (str(index+1) + ". FR\n")
		elif (value == germ):
			probList +=  (str(index+1) + ". GR\n")
		else:
			probList +=  (str(index+1) + ". N/A\n")

		

		value = max( engAddone, frenAddone, germAddone)

		if( value == engAddone): 
			output +=  (str(index+1) + ". EN\n")
		elif (value == frenAddone): 
			output +=  (str(index+1) + ". FR\n")
		elif (value == germAddone):
			output +=  (str(index+1) + ". GR\n")
		else:
			output +=  (str(index+1) + ". N/A\n")

		value = min( engGT, frGT, grGT)
		#print(engGT, frGT, grGT)

		if( value == engGT): 
			outputGT +=  (str(index+1) + ". EN\n")
		elif (value == frGT): 
			outputGT +=  (str(index+1) + ". FR\n")
		elif (value == grGT):
			outputGT +=  (str(index+1) + ". GR\n")
		else:
			outputGT +=  (str(index+1) + ". N/A\n")

			
		value = min( engKN, frKN, grKN)
		#print( engKN, frKN, grKN)

		
		if( value == engKN): 
			outputKN +=  (str(index+1) + ". EN\n")
		elif (value == frKN): 
			outputKN +=  (str(index+1) + ". FR\n")
		elif (value == grKN):
			outputKN +=  (str(index+1) + ". GR\n")
		else:
			outputKN +=  (str(index+1) + ". N/A\n")



	solutionLetterFile.write(probList)
	solutionLetterFile.close()

	solutionAddOnefile.write(output)
	solutionAddOnefile.close()

	solutionGTfile.write(outputGT)
	solutionGTfile.close()

	solutionKN.write(outputKN)
	solutionKN.close()




	testfile.close()
	


	answerFileName = "LangID.gold.txt"



	solutionLetterFile = open("solutionLetter.out", 'r')
	solutionAddOnefile = open("solutionAddOne.out", 'r')
	solutionGTfile = open("solutionGT.out", 'r')
	solutionKN = open("solutionKN.out", 'r')
	answerFile = open(answerFileName, "r")

	answerCurrFile = re.split(r'\n', answerFile.read())
	solutionLetterFileC = re.split(r'\n', solutionLetterFile.read())
	solutionAddOnefileC = re.split(r'\n', solutionAddOnefile.read())
	solutionGTfileC = re.split(r'\n', solutionGTfile.read())
	solutionKNC = re.split(r'\n', solutionKN.read())

	answerCurrFile = answerCurrFile[0].split("\r")
	#solutionLetterFileC = solutionLetterFileC[0].split("\r")
	#solutionAddOnefileC = solutionAddOnefileC[0].split("\r")
	#solutionGTfileC = solutionGTfileC[0].split("\r")
	#solutionKNC = solutionKNC[0].split("\r")

	letterBi = 0
	addone = 0 
	gtBi = 0
	knsmoothing = 0

	for index in range(len(answerCurrFile)):
		#print("index", index)
		#print("dadfasd", answerCurrFile[index], solutionLetterFileC[index])
		
		if(answerCurrFile[index] == solutionLetterFileC[index]):
			letterBi = letterBi + 1
		if(answerCurrFile[index] == solutionAddOnefileC[index]):
			addone = addone + 1
		if(answerCurrFile[index] == solutionGTfileC[index]):

			gtBi = gtBi + 1
		if(answerCurrFile[index] == solutionKNC[index]):
			knsmoothing = knsmoothing + 1

	print("accuracy letter Bigram", float(letterBi)/len(answerCurrFile)* 100, '%')
	print("accuracy Addicative One Bi", float(addone)/len(answerCurrFile)* 100, '%')
	print("accuracy GooD Turning Bi", float(gtBi)/len(answerCurrFile)* 100, '%')
	print("accuracy  Kneser-Ney Bi", float(knsmoothing)/len(answerCurrFile)* 100, '%')


	solutionLetterFile.close()

	
	solutionAddOnefile.close()

	
	solutionGTfile.close()

	
	solutionKN.close()
	answerFile.close()

