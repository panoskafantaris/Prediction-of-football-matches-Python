import numpy as np
import Data_Tables as dt
from sklearn.model_selection import KFold

category=1
inp=input('Enter the exercise you want(for example- exercise 1):')
if(inp=='exercise 1'):#o least mean square algorithm
    category=1
    import LeastMeanSquares as lms
    X = np.array(dt.K)#o pinakas me tis apodoseis twn paixnidiwn
    y = np.array(dt.Y)#ta output twn paixnidiwn
elif(inp=='exercise 2'):
    category=2
    import LeastSquares as ls
    X = np.array(dt.K)#o pinakas me tis apodoseis twn paixnidiwn
    y = np.array(dt.Y)#ta output twn paixnidiwn
else:#to multilayer neural network
    category=3
    import MultiLayerNN as mnn
    X,y=dt.MNN_data()
    X = np.array(X)#o pinakas me tis apodoseis twn paixnidiwn
    y = np.array(y)#ta output twn paixnidiwn
kf = KFold(n_splits=10)#xwrizoume th bash se 10 merh
kf.get_n_splits(X)
bet_sites=['B365','BW','IW','LB']
i=1
for train_index, test_index in kf.split(X):
    print('iterration:'+str(i))
    print('wait it starts the training...')
    X_train, X_test = X[train_index], X[test_index]#train kai test tou pinaka twn apodosewn
    y_train, y_test = y[train_index], y[test_index]#train kai test tou pinaka twn output
    
    if(category==1):#an theloume thn askhsh 1 na trexoume
        theta=[1,1,1,1]
        matrix_weights,performance,output=lms.init(theta, X_train, y_train)

        print('Most Accurate Betting Site:')
        for k in bet_sites:
            if (bet_sites.index(k)==np.argmin(performance)):
                print(k)
                break
        print('Weights:')
        print(matrix_weights[np.argmin(performance)])
        print('Cost')
        print(performance[np.argmin(performance)])
        wrongs,rights=lms.test(matrix_weights[np.argmin(performance)],X_test,y_test,output)
        print('Wrongs are: '+str(wrongs))
        print('Rights are: '+str(rights))
        print(" ")
    elif(category==2):
        ls.main(X_train,y_train,X_test,y_test)
    else:
        mnn.init(X_train,y_train,X_test,y_test)

    i+=1