import numpy as np
import math
import matplotlib.pyplot as plt

def hypothesis(x, theta):#Wt*x
    t=np.transpose(np.array(theta)).dot(np.array(x))
    return t
    
def costFunction(theta, x, y):
    factor = 1 / len(x)
    sum = 0
    for i in range(0,len(x)):
        sum += math.pow((hypothesis(x[i], theta) - y[i]), 2)
        
    return factor * sum

def learnThetaSingle(theta, x, y, alpha):#w(n)+2*p*Error*x
    return theta + 2*alpha * (y - hypothesis(x, theta)) * x

def learnTheta(theta, x, y):
    alpha=1/len(x)#learning rate
    f = theta
    bet=[]
    curr=[]
    all_bet_sites=[0 for i in range(0,len(x))]
    for i in range(0,len(x)):#ftiaxnoume enan neo pinaka me ola ta bets mazi me to 1 sto telos gia na mas bohthisei sto kostos
        curr=x[i][1],x[i][2],x[i][3],1
        curr=np.array(curr)
        all_bet_sites[i]=curr
    matrix_weights=[]
    costs=[]
    performance=[]
    minimum=1
    iterrations=10#dinoume ena perithwrio merikwn epanalhpsewn mhpws xana katebei to kostos opws tha doume kai pio katw
    j=0
    while(j<4):#gia kathe betting site
        i=0
        while(i<len(x)):#gia ola ta dedomena
            bet=x[i][j*3+1],x[i][j*3+2],x[i][j*3+3],1#bazoume oles ths apodoshs se mia metablhth kai prosthetoume to 1 sto telos 
            bet=np.array(bet)
            f = learnThetaSingle(f, bet, y[i], alpha)#mathenei ta nea barh
            i+=1
        
        cost=costFunction(f, all_bet_sites, y)#metrame to kostos
        costs.append(cost)#se periptwsh pou to kostos anebainei h epanalhpsh tha stamathsei kai emeis theloume auto to pinaka
        #gia na paroume apo kei th mikroterh timh
        curr=round(cost,6)#tha bohthisei gia pio apodotikous upologismous
        if(curr<minimum):#oso peftei to kostos den allazoume betting site
            minimum=curr
        else:#otan doume oti anebainei allazoume kai apothikeuoume ta dedomena weights,cost ktl..
            iterrations-=1#me th metablhth auth dinoume ena perithwrio mhpws xana katebei to kostos
            if(iterrations==0):
                matrix_weights.append(f)
                f=[1,1,1,1]
                j+=1
                try:
                    for i in range(0,len(x)):
                        all_bet_sites[i]=x[i][j*3+1],x[i][j*3+2],x[i][j*3+3],1
                    performance.append(costs[np.argmin(costs)])
                except:
                    performance.append(costs[np.argmin(costs)])
                iterrations=10
                minimum=1
                performance.append(costs[np.argmin(costs)])
                costs=[]
      
    return matrix_weights,performance#fernoume pisw to pinaka me ola ta weights olws twn sites kai ta kosth toys

def init(theta,x,y):
    #ftiaxnoume tis 3 discriminant functions kai tha doume poia tha krathsoume sto telos
    output=[[1,-1,-1],[-1,1,-1],[-1,-1,1]]#ta y gia kathe sunarthsh
    new_matrix_weights=[]
    new_performance=[]
    new_y=[0 for i in range(0,len(y))]
    for j in output:
        #ta bazoume mesa se enan pinaka pou tha allazei otan allazoume sunarthsh
        for i in range(0,len(y)):
            if(y[i][1]=='1'):
                new_y[i]=j[0]
            elif(y[i][1]=='0'):
                new_y[i]=j[1]
            else:
                new_y[i]=j[2]
        
        matrix_weights,performance=learnTheta(theta, x, new_y)#lms algoritmos tha trexei gia ola ta betting site tautoxrona
        new_matrix_weights.append(matrix_weights)#ta weights meta to treximo gia kathe betting site
        new_performance.append(performance)#to kostos toy

    minimum_performance=[]
    final_weights=[]
    final_performance=[]
    right_output=[]
    for i in range(0,4):
        minimum_performance=new_performance[0][i],new_performance[1][i],new_performance[2][i]
        index=np.argmin(minimum_performance)
        right_output.append(index)
        final_weights.append(new_matrix_weights[index][i])#ta telika weights bash toy mikroterou kostoys kathe betting site
        final_performance.append(new_performance[index][i])#ta telika mikrotera kosth
    final_output=output[right_output[np.argmin(final_performance)]]#to output pou tha xrhimopoihsoume bash kostous gia to testarisma toy algorithmou
    #dld auto poy tha mas ferei ta perisssotera swsta

    return final_weights,final_performance,final_output

def test(theta,x,y,output_matrix):
    new_y=[0 for i in range(0,len(y))]#ftiaxnoume to neo pinaka me bash to kalutero output pou brhkame
    for i in range(0,len(y)):
        if(y[i][1]=='1'):
            new_y[i]=output_matrix[0]
        elif(y[i][1]=='0'):
            new_y[i]=output_matrix[1]
        else:
            new_y[i]=output_matrix[2]
    sum_w=0#metrame ta lathi
    sum_r=0#metrame ta swsta
    for j in range(0,4):
        for i in range(0,len(x)):
            bet=x[i][j*3+1],x[i][j*3+2],x[i][j*3+3],1#prosthetoume to 1 sto telos tou pinaka me ta bets
            if(np.sign(hypothesis(theta,bet))==new_y[i]):#ousiastika an einai panw ap th sunarthsh h katw analogws to outcome pou theloume
                sum_r+=1
            else:
                sum_w+=1
    return sum_w,sum_r
