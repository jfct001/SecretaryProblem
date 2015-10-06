#!/usr/bin/python3

import collections
import math
import sys
import numpy as np
from datetime import datetime
from multiprocessing import Process, Queue

def configValue(fileName, key, returnType='str'):
	configFile = open(fileName, 'r')
	
	cache = configFile.read()
	
	index = cache.find(key, 0, len(cache))
	if index!=(-1):
		end=cache.find(">", index+1, len(cache))
		configFile.close()
		if returnType=='int':
			return int(cache[index+len(key)+1:end])
		else:
			return cache[index+len(key)+1:end]
	
	configFile.close()


def initApplicants(size, topRange):
	array=[]
	for x in range(size):
		array.append(np.random.random_integers(0, topRange))
	return array

def groupSize(length, alg):
	if alg=='a':
		result = math.sqrt(length)
		return int(math.ceil(result))
	if alg=='b':
		result = math.sqrt(length)
		result += math.sqrt(result)*(length/10)
		return int(math.ceil(result))
	if alg=='b2':
		result = math.sqrt(length)
		result += math.sqrt(result)*(length/(length/10))
		return int(math.ceil(result))
	if alg=='e':
		result = length/math.e
		
		return int(math.ceil(result))
	
def testGroupSize(array, alg):
	return groupSize(len(array), alg)

def chooseApplicants(array, testGroup):
	highest = max(array[0:testGroup])
	#print("Testing first " + str(len(array[0:testGroup])))
	for x in array[testGroup-1:len(array)+1]:
		if x >= highest:
			return x

def progressBar(progress, completion, resolution=20):
    index=math.ceil(((progress/completion)*resolution))
    sys.stdout.write("\r|")
    for x in range(index):
        sys.stdout.write("#")
    for x in range(resolution-index):
        sys.stdout.write("-")
    sys.stdout.write("| %f %% complete" % int((float(progress)/completion)*100))
    sys.stdout.flush()
    
def calculate(testCount, configFile, applicantCount, q, progress='no', customSize='no', sizeValue=0):
	topRange = configValue(configFile, "topRange", 'int')
	alg = configValue(configFile, "alg")
	localCorrect=0
	for x in range(1, int(testCount+1)):
		
		applicants = initApplicants(applicantCount, topRange)

		if customSize=='yes':
			solution=chooseApplicants(applicants, sizeValue)
		else:
			size=testGroupSize(applicants, alg)
			solution=chooseApplicants(applicants, size)

		divisor=testCount/20
		if progress=='yes':
                        if x % divisor == 0:
                                
                                progressBar((x), testCount)
		if solution == max(applicants):
			localCorrect += 1
	q.put(localCorrect)




###BEGIN MAIN PROGRAM
def testAccuracy(configFile, testGroupSize, applicantCount):
	testCount = configValue(configFile, "testCount", 'int')
	quadMode = configValue(configFile, "quadMode")
	print(configValue(configFile, "topRange"))
	

	correct=0.00
	startTime = datetime.now()
	q = Queue()

	if __name__ == '__main__':    
		results = []
		if quadMode=='yes':
		        print("Quad process mode...")
		        threads=4
		        p1 = Process(target=calculate, args=(testCount/threads, configFile, applicantCount, q, 'yes', 'yes', testGroupSize))
		        p1.start()
		        p2 = Process(target=calculate, args=(testCount/threads, configFile, applicantCount, q, 'no', 'yes', testGroupSize))
		        p2.start()
		        p3 = Process(target=calculate, args=(testCount/threads, configFile, applicantCount, q, 'no', 'yes', testGroupSize))
		        p3.start()
		        p4 = Process(target=calculate, args=(testCount/threads, configFile, applicantCount, q, 'no', 'yes', testGroupSize))
		        p4.start()  
		        

		        for i in range(threads):
		                #set block=True to block until we get a result
		                results.append(q.get(True))
		                     
		        
		        
		else:
		        print("Single process mode...")
		        threads=1
		        p1 = Process(target=calculate, args=(testCount/threads, configFile, applicantCount, q, 'yes', 'yes', testGroupSize))
		        p1.start() 

		        for i in range(threads):
		                #set block=True to block until we get a result
		                results.append(q.get(True))
		                     
	
		correct=float(sum(results))

		sys.stdout.write("\n")
		#print(correct)
		print(str((correct/testCount)*100) + "% accuracy") 
		print("Operation took "+ str(datetime.now() - startTime))

testAccuracy("Secretary.cfg", 375, 1000)







