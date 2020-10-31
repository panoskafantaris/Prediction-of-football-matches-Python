from numpy.linalg import inv, solve, matrix_rank
import numpy as np
import sys, os
from random import shuffle, randint

def train(x,y):
	D = x.shape[1] + 1 
	K = y.shape[1]
	# xi*xi and xi*yi, oysiastika vasizetai stin exisosi piknotitas pithanotitas gia to w
	sum1 = np.zeros((D,D)) # arxikopoihsh
	sum2 = np.zeros((D,K))
	i = 0
	for x_i in x:						 
		x_i = np.append(1, x_i) 		# prosthitki array me 1 sto dianysma  
		y_i = y[i]						
		sum1 += np.outer(x_i, x_i)		# xi*xi_kapelo - aplooiimeni morfi tis synartisis P.P J(w) -> sx3.43 toy biblioy
		sum2 += np.outer(x_i, y_i)		# xi*yi_kapelo
		i += 1
	
	# Dianysma baron -> pollaplasiasmos sum2 me antistrofi toy sum1
	return np.dot(inv(sum1),sum2)#sxesi 3.45


def predict(W, x):
	x = np.append(1, x)		# prosthetei ton array 1 sto x dianysma, oste na kanei tin praxi

	# Lynoyme to W_hat*x
	values = list(np.dot(W.T,x))
	
	# Eyresi megistis timis 
	winners = [i for i, x in enumerate(values) if x == max(values)]	
    # epilegei stin tyxi ean to apotelesma tha einai 0 i 1 dld ypothetei tin timi toy y
	index = randint(0,len(winners)-1)
	winner = winners[index]     #orizei se nea metavliti winner tin timi ton i kai x poy exei epilegei gia problepsi

	y = [0 for x in values] 	# arxikopoihsh pinaka me midenika 
	y[winner] = 1 				# epilogi timis
	return y

def fixLabels(y):
	newY = []
	for i in range(len(y)):
		# Kathe lista einai to megethos tis klasis me ti megalyteri timi
		if(y[i][1]=='1'):
			newY.append([1,0,0])#epeidi nikise i home, 1 stin apodosi tis stoiximatis gia niki
		elif(y[i][1]=='0'):
			newY.append([0,1,0])#an einai isopalia/itta , 1 gia ti stili draw,away kai 0 sti home
		else:
			newY.append([0,0,1])#to idio me to deytero
	return np.matrix(newY)

def test(a,b,c,d):
	# Dimioyrgia dianysmatos baron, telos ekpaideysis
	W = train(a,b)
	# Dimioyrgia synolon gia testing
	x = c
	y = d
	
	total = y.shape[0]
	i = 0
	hits = 0	
    # an i timi apo to prediction einai idia me tin timi toy y (tote anevainei to accuracy)
	for i in range(total):
		prediction = predict(W,x[i])
		actual = list(y[i].A1)
		if prediction == actual:
			hits += 1 # accuracy hits (diairo me to mikos ton y kai brisko synoliko accuracy)
	accuracy = hits/float(total)*100
	print ("Akribeia = " + str(accuracy) + "%", "(" + str(hits) + "/" + str(total) + ")")
	print(" ")
	
def main(x_train,y_train,x_test,y_test):
	print('Enarksi ekpaideysis...')
	data = x_train[:,1:]
	classes = y_train
	
	x = np.matrix(data)#metatropi input se mitres px an exei delimiter
	y = fixLabels(classes)#apla ftiaximo toy y me aparaitith morfh gia tis praxeis  
	c=np.matrix(x_test[:,1:])
	d=fixLabels(y_test)
	# shuffle dedomenon gia kalyteri akribeia
	z = [] #prosorinos pinakas - se ena array vazoyme ta x kai y 
	size = x.shape[0] - 1        
	for i in range(size):#size-1 epeidh to for loop xekinaei apo 0, https://datascience.stackexchange.com/questions/24511/why-should-the-data-be-shuffled-for-machine-learning-tasks 
		z.append((x[i],y[i]))	
	for i in range(size):
		x[i] = z[i][0]
		y[i] = z[i][1]		

    # Emfanisi dedomenon ekpaideysis(training) kai dokimis(testing)
	test(x,y,c,d)
