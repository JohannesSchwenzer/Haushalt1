# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 19:17:47 2019

@author: s0536
"""

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt



##############################################

#Hier können die veränderlichen Parameter des PV Systems eingetragen werden# 


Startkapazität=0        #Startkapazität der Batterie in kWh     
Kapazität = 3           #Größe der Batterie in kWh
Solaranlage = 5         #Größe der Solaranlage in m² mit einem Wirkungssgrad von 20% 


##############################################

timesteps = 52560

u=Solaranlage/5
df=pd.read_csv('QuartierHH.csv',nrows=timesteps) 

a = df["pv"]
b = df["LAST_EFH"]


c= u*a-b
d= u*a-b
e= u*a-b
f= u*a-b
g= u*a-b
h= u*a-b


bataus=pd.to_numeric(c)


for i in range(bataus.shape[0]):
   
        if bataus[i]>0:
           bataus[i]=0
        elif bataus[i]<0:
            bataus[i]=bataus[i]
            
batein=pd.to_numeric(d)


for i in range(batein.shape[0]):
   
        if batein[i]<0:
           batein[i]=0
        elif batein[i]>0:
           batein[i]=batein[i]            


batkap=pd.to_numeric(e)

for i in range(batkap.shape[0]):
    if i in (0,1):
        if batein[i]+bataus[i]+Startkapazität>0 :
           
        
            batkap[i]=batein[i]+bataus[i]+Startkapazität    
        else: batkap[i]=0
        
    
    else:    
        if batein[i]+bataus[i]+batkap[i-1]>0 :
           if batein[i]+bataus[i]+batkap[i-1]> Kapazität :
            batkap[i]= Kapazität
           else: batkap[i]=batein[i]+bataus[i]+batkap[i-1]
                
        else:
            batkap[i]=0
   
Netzbezug=pd.to_numeric(f)
diff=pd.to_numeric(g)

for i in range(Netzbezug.shape[0]):
   if i < timesteps-1:
    if diff[i+1]+batkap[i]<0:
        Netzbezug[i]= abs(diff[i+1]+batkap[i])
    else: Netzbezug[i]= 0    
   else: Netzbezug[i]= abs(diff[i])
   
Netzeinspeisung=pd.to_numeric(h)  

for i in range(Netzeinspeisung.shape[0]):
    if i in (0,1):
        Netzeinspeisung[i]=0
           
            
    else:    
        if Netzbezug[i] == 0 :
           if batkap[i-1] == Kapazität :
            Netzeinspeisung[i]= batein[i]
           else: Netzeinspeisung[i]= 0
                
        else:
            Netzeinspeisung[i]= 0

Ersparniss= (b.sum() -  Netzbezug.sum()) *0.29 + (Netzeinspeisung.sum() *0.12)
Installationskosten=u*5000+ Kapazität*1000  
ROI= Installationskosten/Ersparniss
print('Solarstrom gesamt:       ',a.sum())
#print('Batterieaufladung:       ',batein.sum())
print('Verbrauch:               ',b.sum())
#print('Batterieeinspeisung;     ', abs(bataus.sum()))
#print(batkap.sum())
print('Netzbezug:               ', Netzbezug.sum())
print('Netzeinspeisung:         ', Netzeinspeisung.sum())
print('Ersparniss:              ', Ersparniss)
print('Installationskosten:     ', Installationskosten)
print('Return on Investment:    ', ROI)

#batein.plot(title='batein')