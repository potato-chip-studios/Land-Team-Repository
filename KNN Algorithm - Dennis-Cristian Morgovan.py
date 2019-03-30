import math
import operator
from decimal import Decimal
 
#Euclidian distance = distance between two points in Euclidian space
#Formula: For two points a and b: dist = sqrt((a1 - b1)^2 + (a2-b2)&2 + ... + (an - bn)^2)
def euclideanDistance(x, y, length):
	dist  = 0
	
	for i in range(length):
		dist  += pow((x[i] - y[i]), 2)
		
	return math.sqrt(dist)
	
def p_root(value, root): 
      
    root_value = 1 / float(root) 
    return round (Decimal(value) ** Decimal(root_value), 3) 	
	
def minkowskiDistance(p, q, n): 
      
    return sum([abs(x-y)**n for x,y in zip(p,q)])**1/n
	
#Gets the k nearest neighbours 
def getNeighbors(trainingSet, test, k):
	distances = []
	
	minkTest = []
	neighbours  = []
	
	length = len(test)-1
	p = 3
	
	for i in range(len(test) - 1):
	    minkTest.append(test[i])
	    
	
	
	#Calculates the euclidian distance between the test input and every element in the training vector
	for i in range(len(trainingSet)):
		#dist = euclideanDistance(trainingSet[i], test, length)
		minkTraining = []
		for j in range(len(trainingSet[i]) -1):
		    minkTraining.append(trainingSet[i][j])
		
		dist = minkowskiDistance(minkTraining, minkTest, length)
		distances.append((trainingSet[i], dist))
		
	distances.sort(key=operator.itemgetter(1))
	
	
	for i in range(k):
		neighbours.append(distances[i][0])

	return neighbours 
	
#Gets the k nearest neighbours 
def getResponseWeight(trainingSet, test, k):
	distances = []
	
	minkTest = []
	neighbours  = []
	
	redNumber = 0
	redDist = 0
	greenNumber = 0
	greenDist = 0
	response = ''
	
	length = len(test)-1
	p = 3
	
	for i in range(len(test) - 1):
	    minkTest.append(test[i])
	    
	
	
	#Calculates the euclidian distance between the test input and every element in the training vector
	for i in range(len(trainingSet)):
		#dist = euclideanDistance(trainingSet[i], test, length)
		minkTraining = []
		for j in range(len(trainingSet[i]) -1):
		    minkTraining.append(trainingSet[i][j])
		
		dist = minkowskiDistance(minkTraining, minkTest, length)
		distances.append((trainingSet[i], dist))
		
	distances.sort(key=operator.itemgetter(1))
	
	
	for i in range(k):
		neighbours.append(distances[i][0])
		if neighbours[i][-1] == 'r':
		    redNumber +=1
		    redDist += 1 / distances[i][-1]
		else:
		    greenNumber +=1
		    greenDist += 1 / distances[i][-1]
	
	if redDist == 0:
	    redDist = 1
	if greenDist == 0:
	    greenDist = 1
	    
	
	if redNumber / redDist > greenNumber / greenDist:
	    response = 'r'
	else:
	    response = 'g'
	return response 

#Gets the type of label most common in the neighbours array
#A general 2D array of neighbours would look like this: neighbours = [[0, 1, 0, 'g'], [1, 0, 0, 'r'], ...]
#The label of the element is situated at the end 
def getResponse(neighbours):
	responses = {}
	sortedResponses = {}
	
	#Goes through the array of neighbours and checks their labels (last element), 
	#adding the label to the response list, or incrementing the label number if the label is already present.
	for i in range(len(neighbours)):
		response = neighbours[i][-1]
		
		if response in responses:
			responses[response] += 1
		else:
			responses[response] = 1
			
	sortedResponses = sorted(responses.iteritems(), key=operator.itemgetter(1), reverse=True)
	
	return sortedResponses[0][0]

#Tests the accuracy of the classifier algorithm 
def getAccuracy(testSet, predictions):
	correctAnswers  = 0
	
	for i in range(len(testSet)):
		if testSet[i][-1] == predictions[i]:
			correctAnswers  += 1
			
	return (correctAnswers /float(len(testSet))) * 100.0

            
def main():
	#Input
	trainingSet=[
	    [1, 0, 0, 'r'], 
	    [0.5, 0, 0, 'r'], 
	    [0.7, 0.3, 0.1, 'r'], 
	    [0.9, 0.2, 0.1, 'r'],
	    [0.925, 0.1, 0.1, 'r'],
	    [0.654, 0.4, 0.1, 'r'],
	    [0.55, 0.43, 0.2, 'r'],
	    [0.765, 0.267, 0.1, 'r'],
	    [0.5797, 0.23, 0.26, 'r'],
	    [0.7987, 0.132, 0.323, 'r'],
	    [0.8679, 0.2352, 0.0, 'r'],
	    [0.6554, 0.4432, 0.01, 'r'],
	    [0.501584, 0.4974327, 0.0, 'r'],
	    [0.50001321, 0.47805, 0.2, 'r'],
	    [0.5375, 0.48908, 0.03, 'r'],
	    [0.52145, 0.46564, 0.121, 'r'],
	    [0.51231, 0.4908099, 0.12321, 'r'],
	    [0.6213, 0.4845, 0.0, 'r'],
	    [0.77454, 0.2353, 0.0, 'r'],
	    [0.6896, 0.2785, 0.1, 'r'],
	    [0.98748, 0.02, 0.01, 'r'],
	    [0.3221, 0.21313, 0.543, 'r'],
	    [0.49550, 0.286960, 0.25223, 'r'],
	    [0.459, 0.314, 0.25223, 'r'],
	    [0.409, 0.401, 0.25223, 'r'],
	    [0.439, 0.114, 0.45223, 'r'],
	    [0.359, 0.314, 0.25223, 'r'],
	    [0.759, 0.314, 0, 'r'],
	    [0.6159, 0.214, 0.25223, 'r'],
	    [0.589, 0.214, 0.15223, 'r'],
	    [0.4709, 0.332344, 0.20223, 'r'],
	    [0.359, 0.314, 0.35223, 'r'],
	    [0.4959, 0.4714, 0.15223, 'r'],
	    [0.4679, 0.4564, 0.15223, 'r'],
	    [0.4239, 0.406, 0.25223, 'r'],
	    [0.4, 0.6, 0.7, 'g'], 
	    [0, 1, 0, 'g'], 
	    [0, 0.5, 0.5, 'g'], 
	    [0.2, 0.3, 0.5, 'g'],
	    [0.1, 0.7, 0.3, 'g'],
	    [0.4, 0.6, 0.1, 'g'],
	    [0.1, 0.32, 0.1, 'g'],
	    [0.3, 0.45, 0.3, 'g'],
	    [0, 0.8, 0.2, 'g'],
	    [0.345, 0.623, 0.2, 'g'],
	    [0.4867, 0.50948, 0.0, 'g'],
	    [0.49878, 0.50103, 0.1, 'g'],
	    [0.45978, 0.54876, 0.0, 'g'],
	    [0.43434, 0.57665, 0.0, 'g'],
	    [0.465, 0.485, 0.2, 'g'],
	    [0.49965, 0.51, 0.0, 'g'],
	    [0.47564, 0.5331, 0.0, 'g'],
	    [0.4567, 0.53756, 0.2, 'g'],
	    [0.43534, 0.4756, 0.3, 'g'],
	    [0.413, 0.623, 0.0433, 'g'],
	    [0.401, 0.580, 0.0433, 'g'],
	    [0.313, 0.723, 0.0433, 'g'],
	    [0.213, 0.523, 0.3433, 'g'],
	    [0.313, 0.423, 0.3433, 'g'],
	    [0.113, 0.523, 0.4433, 'g'],
	    [0.353, 0.373, 0.233, 'g'],
	    [0.373, 0.393, 0.133, 'g'],
	    [0.325, 0.350, 0.243, 'g'],
	    [0.283, 0.303, 0.3433, 'g'],
	    [0.383, 0.423, 0.2433, 'g'],
	    [0.443, 0.453, 0.133, 'g'],
	    [0.113, 0.523, 0.433, 'g'],
	    [0.2913, 0.313, 0.333, 'g'],
	    [0.5113, 0.59023, 0, 'g'],
	    [0.313, 0.383, 0.3433, 'g'],
	    [0.2513, 0.4523, 0.3433, 'g']]
	testSet=[
	    [0.2, 0.7, 0.2, 'g'],
	    [0.4, 0.64, 0.3, 'g'],
	    [0.45, 0.55, 0.0, 'g'],
	    [0.5, 0.5, 0.0, 'g'], #Case where both colours are the same amount
	    [0.49, 0.51, 0.1, 'g'],
	    [0.4543, 0.4590, 0.1, 'g'],
	    [0.42, 0.4897, 0, 'g'],
	    [0.42131, 0.459787, 0.2, 'g'],
	    [0.288796, 0.3254, 0.2, 'g'],
	    [0.3030676, 0.35078, 0.3, 'g'],
	    [0.28060, 0.35959, 0.3, 'g'],
	    [0.6, 0.3, 0, 'r'],
	    [0.8, 0.2, 0, 'r'],
	    [0.3, 0.2, 0.5, 'r'],
	    [0.6789, 0.342, 0, 'r'],
	    [0.8565, 0.2323, 0.1, 'r'],
	    [0.925, 0.1, 0, 'r'],
	    [0.567, 0.456, 0, 'r'],
	    [0.478, 0.476, 0.3, 'r'],
	    [0.4256, 0.402, 0.2, 'r'],
	    [0.4756, 0.4356, 0, 'r'],
	    [0.4654, 0.48, 0.12, 'r'],
	    [0.4453, 0.3434, 0.22, 'r'],
	    [0.41323, 0.212, 0.211, 'r'],
	    [0.3989, 0.3, 0.2789, 'r']]
	
	#Prediction generation
	predictions=[]
	k = 6
	
	for i in range(len(testSet)):
		neighbours = getNeighbors(trainingSet, testSet[i], k)
		result = getResponse(neighbours)
		#result = getResponseWeight(trainingSet, testSet[i], k)
		predictions.append(result)
		print('Prediction: ' + repr(result) + ', Actual: ' + repr(testSet[i][-1]))
	accuracy = getAccuracy(testSet, predictions)
	print('Accuracy: ' + repr(accuracy) + '%')
	
	
main()