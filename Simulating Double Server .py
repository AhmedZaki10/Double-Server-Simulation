#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt

# Creating the Dataframe
d= ['Customer Number', 'IAT Random Numbers', 'IAT', 'Clock', 'ST Random Numbers', 'Baker Begins', 'Baker ST', 'Baker Ends' ,'Able Begins' ,'Able ST' ,'Able Ends', 'Queuing Time' ,'Time in System' ,'Baker - Idle Time' ,'Able - Idle Time']
df=pd.DataFrame(columns=d)
df[d]=[0][0]


# In[2]:


def simulation(clock,iat_rn,st_rn,iat_st,iat_prob,baker_st,baker_prob,able_st,able_prob):

# Filling RN & Clock
    df['IAT Random Numbers']=iat_rn
    df['ST Random Numbers']=st_rn
    df['Clock']=clock
    for i in range(len(iat_rn)):
        df.loc[df.index[i], 'Customer Number'] = i+1
    df.fillna(0,inplace=True) 
        
# Creating IAT Cprobability list   
    iat_cprob=[]
    iat_cprob.append(iat_prob[0])
    for i in range(len(iat_prob)-1):
        iat_cprob.append(round(iat_cprob[i]+iat_prob[i+1],2))
# Filling "IAT" column based on IAT_RN
    for i in range(len(iat_rn)):
        for j in range(len(iat_cprob)):
            if iat_rn[i]<iat_cprob[j]*100:
                df.loc[df.index[i], 'IAT'] = iat_st[j]
                break
      
    
# Creating Baker Cprobability list    
    baker_cprob=[]
    baker_cprob.append(baker_prob[0])
    for i in range(len(baker_prob)-1):
        baker_cprob.append(round(baker_cprob[i]+baker_prob[i+1],2))
# Creating Able Cprobability list        
    able_cprob=[]
    able_cprob.append(able_prob[0])
    for i in range(len(able_prob)-1):
        able_cprob.append(round(able_cprob[i]+able_prob[i+1],2))

        
# Filling the Dataframe
    for k in range(len(iat_rn)):
        
        # 1) If Baker is available 
        if df.loc[df.index[k], 'Clock']>=max((df['Able Ends'])):
            # Spot RN range
            for j in range(len(baker_cprob)):
                if st_rn[k]<baker_cprob[j]*100:
                    df.loc[df.index[k], 'Able ST'] = baker_st[j]
                    break
            df.loc[df.index[k], 'Able Begins']=df.loc[df.index[k], 'Clock']
            df.loc[df.index[k], 'Able - Idle Time']=df.loc[df.index[k], 'Able Begins']-max(df['Able Ends'])
            df.loc[df.index[k], 'Able Ends']=df.loc[df.index[k], 'Able ST']+df.loc[df.index[k], 'Able Begins']
        
        # 2) If Baker is busy & Able is available
        elif df.loc[df.index[k], 'Clock']>=max((df['Baker Ends'])):
            
            for j in range(len(able_cprob)):
                if st_rn[k]<able_cprob[j]*100:
                    df.loc[df.index[k], 'Baker ST'] = able_st[j]
                    break
            
            df.loc[df.index[k], 'Baker Begins']=df.loc[df.index[k], 'Clock']
            df.loc[df.index[k], 'Baker - Idle Time']=df.loc[df.index[k], 'Baker Begins']-max(df['Baker Ends'])
            df.loc[df.index[k], 'Baker Ends']=df.loc[df.index[k], 'Baker ST']+df.loc[df.index[k], 'Baker Begins']
        
        # 3) If 2 are busy & Able finishes first    
        elif min(max(df['Able Ends']),max(df['Baker Ends']))==max(df['Able Ends']):
            for j in range(len(baker_cprob)):
                if st_rn[k]<baker_cprob[j]*100:
                    df.loc[df.index[k], 'Able ST'] = baker_st[j]
                    break
            df.loc[df.index[k], 'Able Begins']=max(df['Able Ends'])
            df.loc[df.index[k], 'Able - Idle Time']=df.loc[df.index[k], 'Able Begins']-max(df['Able Ends'])
            df.loc[df.index[k], 'Able Ends']=df.loc[df.index[k], 'Able ST']+df.loc[df.index[k], 'Able Begins']
        
        # 4) If 2 are busy & Baker finishes first
        else:
            for j in range(len(able_cprob)):
                if st_rn[k]<able_cprob[j]*100:
                    df.loc[df.index[k], 'Baker ST'] = able_st[j]
                    break
            df.loc[df.index[k], 'Baker Begins']=max(df['Baker Ends'])
            df.loc[df.index[k], 'Baker - Idle Time']=df.loc[df.index[k], 'Baker Begins']-max(df['Baker Ends'])
            df.loc[df.index[k], 'Baker Ends']=df.loc[df.index[k], 'Baker ST']+df.loc[df.index[k], 'Baker Begins']
            
    # Calculating Queuing Time    
    for i in range(len(iat_rn)):
        df.loc[df.index[i], 'Queuing Time']=max(df.loc[df.index[i], 'Able Begins'],df.loc[df.index[i], 'Baker Begins'])-df.loc[df.index[i], 'Clock']
    # Calculating Time in System
    for i in range(len(iat_rn)):
        df.loc[df.index[i], 'Time in System']=max(df.loc[df.index[i], 'Able Ends'],df.loc[df.index[i], 'Baker Ends'])-df.loc[df.index[i], 'Clock']
        
        


    


# In[3]:


# Input sample
iat_rn=[0,26,98,90,26,42,74,80,68,22,48,34,45,24,34,63,38,80,42,56,89,18,51,71,16,92]
st_rn=[95,21,51,92,89,38,13,61,50,49,39,53,88,1,81,53,81,64,1,67,1,47,87,57,87,47]
iat_st=[1,2,3,4]
iat_prob=[0.25,0.40,0.20,0.15]
baker_st=[2,3,4,5]
baker_prob=[0.35,0.25,0.20,0.20]
able_st=[2,3,4,5]
able_prob=[0.30,0.28,0.25,0.17]
clock=[0,2,6,10,12,14,17,20,23,24,26,28,30,31,33,35,37,40,42,44,48,49,51,54,55,59]


# In[4]:


simulation(clock,iat_rn,st_rn,iat_st,iat_prob,baker_st,baker_prob,able_st,able_prob)


# In[5]:


df


# In[6]:


percentage_of_baker_busy=round(sum(df['Baker ST'])/max(max(df['Able Ends']),max(df['Baker Ends'])),3)
percentage_of_able_busy=round(sum(df['Able ST'])/max(max(df['Able Ends']),max(df['Baker Ends'])),3)
print("Percentage of Baker busy =",percentage_of_baker_busy,"\nPercentage of Able busy =",percentage_of_able_busy)


# In[7]:


avg_waiting_time=round(sum(df['Queuing Time'])/len(df[df['Queuing Time']== 1.0] ),3)


# In[8]:


avg_waiting_time


# In[ ]:




