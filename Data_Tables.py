import sqlite3
from datetime import datetime
import numpy as np

MatchColumnNames = ['id', 'country_id', 'league_id', 'season', 'stage','date',
                        'match_api_id','home_team_api_id', 'away_team_api_id','home_team_goal',
                        'away_team_goal','home_player_X1', 'home_player_X2','home_player_X3',
                        'home_player_X4', 'home_player_X5', 'home_player_X6','home_player_X7',
                        'home_player_X8','home_player_X9', 'home_player_X10','home_player_X11',
                        'away_player_X1', 'away_player_X2', 'away_player_X3', 'away_player_X4',
                        'away_player_X5', 'away_player_X6', 'away_player_X7', 'away_player_X8',
                        'away_player_X9', 'away_player_X10', 'away_player_X11', 'home_player_Y1',
                        'home_player_Y2','home_player_Y3', 'home_player_Y4', 'home_player_Y5',
                        'home_player_Y6', 'home_player_Y7', 'home_player_Y8', 'home_player_Y9',
                        'home_player_Y10','home_player_Y11', 'away_player_Y1', 'away_player_Y2',
                        'away_player_Y3','away_player_Y4', 'away_player_Y5', 'away_player_Y6',
                        'away_player_Y7', 'away_player_Y8', 'away_player_Y9', 'away_player_Y10',
                        'away_player_Y11', 'home_player_1', 'home_player_2', 'home_player_3',
                        'home_player_4','home_player_5','home_player_6', 'home_player_7',
                        'home_player_8','home_player_9', 'home_player_10', 'home_player_11',
                        'away_player_1','away_player_2', 'away_player_3', 'away_player_4',
                        'away_player_5','away_player_6', 'away_player_7', 'away_player_8',
                        'away_player_9','away_player_10', 'away_player_11', 'goal', 'shoton',
                        'shotoff','foulcommit', 'card','cross', 'corner', 'possession', 'B365H',
                        'B365D','B365A', 'BWH', 'BWD', 'BWA', 'IWH', 'IWD','IWA', 'LBH', 'LBD',
                        'LBA','PSH', 'PSD', 'PSA']
CountryColumnNames = ['id','name']
LeagueColumnNames = ['id','country_id','name']
PlayerColumnNames = ['id','player_api_id','player_name','player_fifa_api_id',
                     'birthday','height','weight']
PlayerColumnNames = ['id','player_api_id','player_name','player_fifa_api_id',
                     'birthday','height','weight']
TeamColumnNames = ['id','team_api_id','team_fifa_api_id','team_long_name',
                   'team_short_name']
TeamAttributesColumnNames = ['id','team_fifa_api_id','team_api_id',
'date','buildUpPlaySpeed','buildUpPlaySpeedClass','buildUpPlayDribbling',
'buildUpPlayDribblingClass','buildUpPlayPassing','buildUpPlayPassingClass',
'buildUpPlayPositioningClass','chanceCreationPassing','chanceCreationPassingClass',
'chanceCreationCrossing','chanceCreationCrossingClass','chanceCreationShooting',
'chanceCreationShootingClass','chanceCreationPositioningClass','defencePressure',
'defencePressureClass','defenceAggression','defenceAggressionClass',
'defenceTeamWidth','defenceTeamWidthClass','defenceDefenderLineClass']

def retrieve_data(ColumnNames,Table):#exagoume ta dedomena apo ta tables
    list_col=[]
    conn = sqlite3.connect('database.sqlite')
    
    sqlquery="SELECT "
    for x in ColumnNames:
        if(x==ColumnNames[len(ColumnNames)-1]):
            sqlquery=sqlquery+x
        else:
            sqlquery=sqlquery+x+","  
 
    cursor = conn.execute(sqlquery+" FROM "+Table)
    rows = cursor.fetchall()
    
    for row in rows:
        list_col.append(row)
    
    return list_col

r=['match_api_id','home_team_api_id', 'away_team_api_id','home_team_goal','away_team_goal','date']

k=['match_api_id','B365H','B365D','B365A', 'BWH', 'BWD', 'BWA', 'IWH', 'IWD','IWA', 'LBH', 'LBD','LBA']

f=['team_api_id','buildUpPlaySpeed','buildUpPlayPassing','chanceCreationPassing','chanceCreationCrossing','chanceCreationShooting','defencePressure','defenceAggression','defenceTeamWidth','date']

K=retrieve_data(k,"Match")#pinakas me tis apodoseis
K=K[:5000]
A=[]
for i in K:
    for j in i:
        if(j is None):#na aporipsoume tis none apodoseis
            A.append(i)
            break

for i in A:
    K.remove(i) 
del A

#print(K)

G=retrieve_data(r,"Match")#pinakas me th diafora twn goal gia na doume poios nikhse
G=G[:5000]
resluts=[]
for g in G:
    DG=g[3]-g[4]
    if(DG>0):
        resluts.append([g[0],g[1],g[2],1,g[5]])
    elif(DG==0):
        resluts.append([g[0],g[1],g[2],0,g[5]])
    else:
        resluts.append([g[0],g[1],g[2],2,g[5]])
#print(resluts)

Y=[]#gia na antistoixhsoume ta dedomena twn duo parapanw pinakwn kai gia na sigoureutoume
#oti exoun ton idio arithmo dedomenwn
for i in K:
    for j in resluts:
        if(i[0]==j[0]):
            Y.append([i[0],j[3],j[1],j[2],j[4]])
            break
#print(Y)
def MNN_data():#kaleite otan theloume to thema 3 gia na kanoume concarate ta dedomena toy pinaka F kai K
    F=retrieve_data(f,"Team_Attributes")
    teams_att=np.array(F)
    training_data=K
    target_data=np.array(Y)
    min_dt=datetime.strptime(teams_att[np.argmin(teams_att[:,9])][9], '%Y-%m-%d %H:%M:%S')
        
    print('fixing some data first...')
    new_trd=[]
    new_td=[]
    mphka=0
    for i in range(0,len(target_data)):
        dt2 = datetime.strptime(target_data[i][4], '%Y-%m-%d %H:%M:%S')
        mphka=0
        for j in range(0,len(teams_att)):
            if(min_dt.year>dt2.year or mphka>1):
                break
            dt = datetime.strptime(teams_att[j][9], '%Y-%m-%d %H:%M:%S')
            if((teams_att[j][0]==target_data[i][2] or teams_att[j][0]==target_data[i][3]) 
            and dt2.year==dt.year):
                mphka+=1
                training_data[i]=np.concatenate(([training_data[i], teams_att[j][1:9]]), axis=None)
        if(len(training_data[i])>21):#analogws thn nikh kai thn htta ftiaxnoyme ena neo pinaka wste na kanoume 
            #classify ta dedomena gia tis 3 classes [0,1,2]=[1,0,0],[0,1,0],[0,0,1] 
            new_trd.append(training_data[i][1:])
            if(target_data[i][1]=='1'):
                new_td.append([1.,0.,0.])
            elif(target_data[i][1]=='0'):
                new_td.append([0.,1.,0.])
            else:
                new_td.append([0.,0.,1.])
    
    return new_trd,new_td
    