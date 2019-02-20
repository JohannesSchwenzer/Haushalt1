# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 21:26:46 2019

@author: s0536
"""

import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt



timesteps =  52560  #10 minütige Auflösung
df=pd.read_csv('QuartierHH.csv',nrows=timesteps) 


Startkapazität=0         #Startkapazität der Batterie in kWh
Kapazität = 5            #Größe der Batterie in kWh
Wirkungsgrad_pv = 0.2
Systemwirkungsgrad_pv = 0.98
Systemwirkungsgrad_bat = 0.881
Simulationsschritte = 5       # Anzahl der parallel simulierten PV Kapazitäten
Simulationsschrittweite = 2   # 1 entspricht 1m² pv/Simulationsschritt,  




a = df['LAST_EFH']
b = df['pv']

n_pv = Wirkungsgrad_pv
nsys_pv= Systemwirkungsgrad_pv
nsys_bat = Systemwirkungsgrad_bat 
s = Simulationsschrittweite

test=Simulationsschritte


q = np.zeros(shape=(timesteps,test))


for i in range(q.shape[0]):
    for j in range(q.shape[1]):
       
           q[i,j] = a[i] 
           
u = np.zeros(shape=(timesteps,test))


for i in range(u.shape[0]):
    for j in range(u.shape[1]):
       
           u[i,j] = b[i]*n_pv*nsys_pv * s *(j+1)           


bataus = u-q

for i in range(bataus.shape[0]):
    for j in range(bataus.shape[1]):
        if bataus[i,j]>0:
            bataus[i,j]=0
        elif bataus[i,j]<0:
             bataus[i,j]=bataus[i,j]
             


batein = u-q


for i in range(batein.shape[0]):
    for j in range(batein.shape[1]):
        if batein[i,j]<0:
            batein[i,j]=0
        elif batein[i,j]>0:
             batein[i,j]=batein[i,j]
             



batkap=u-q

for i in range(batkap.shape[0]):
    for j in range(batkap.shape[1]):
        if i in (0,1):
            if batein[i,j]+bataus[i,j]+Startkapazität>0 :
           
        
                batkap[i,j]=batein[i,j]+bataus[i,j]+Startkapazität    
            else: batkap[i,j]=0
        
    
        else:    
            if batein[i,j]+bataus[i,j]+batkap[i-1,j]>0 :
                if batein[i,j]+bataus[i,j]+batkap[i-1,j]> Kapazität :
                    batkap[i,j]= Kapazität
                else: batkap[i,j]=(batein[i,j]+bataus[i,j])*(1-(1-nsys_bat)/2)+batkap[i-1,j]
                    
            else:
                batkap[i,j]=0
      

      
diff= u-q
Netzbezug= u-q


for i in range(Netzbezug.shape[0]):
    for j in range(Netzbezug.shape[1]):
        if i < timesteps-1:
            if diff[i+1,j]+batkap[i,j]<0:
                Netzbezug[i,j]= abs(diff[i+1,j]+batkap[i,j]*(1-(1-nsys_bat)/2))
            else: Netzbezug[i,j]= 0    
        else: Netzbezug[i,j]= abs(diff[i,j])
   
   
    
  
    
    
    
    

Netzeinspeisung=u-q

for i in range(Netzeinspeisung.shape[0]):
   for j in range(Netzeinspeisung.shape[1]): 
    if i in (0,1):
        Netzeinspeisung[i,j]=0
           
            
    else:    
        if Netzbezug[i,j] == 0 :
           if batkap[i-1,j] == Kapazität :
            Netzeinspeisung[i,j]= batein[i,j]
           else: Netzeinspeisung[i,j]= 0
                
        else:
            Netzeinspeisung[i,j]= 0
            
Ersparniss= (np.sum(q, axis=0) -  np.sum(Netzbezug, axis=0)) *0.29 + (np.sum(Netzeinspeisung, axis=0) *0.12)            

#Installationskosten= (np.sum(q, axis=0) -  np.sum(Netzbezug, axis=0)) *0.29 + (np.sum(Netzeinspeisung, axis=0) *0.12)
Installationskosten = np.zeros(shape=(1,test))
for i in range(1):
   for j in range(test):
       Installationskosten[i,j]= (j+1)*250 * s + Kapazität*500              

ROI= Installationskosten/Ersparniss


co2= (np.sum(q, axis=0) -  np.sum(Netzbezug, axis=0)) *0.29 + (np.sum(Netzeinspeisung, axis=0) *0.12)
for i in range(1):
   for j in range(test):
       co2[j]= (np.around(a.sum()) - (np.sum(Netzbezug, axis=0)[j]))*0.45


fr = np.zeros(shape=(1,test))


for i in range(fr.shape[0]):
    for j in range(fr.shape[1]):
       
           fr[i,j] = (j+1 )* s           


#print(co2)
print(' ')
print('****                 Energiedaten                  ****        ')
print(' ')
#plt.matshow(u)
print('Verbrauch [kWh]:             ',np.around(a.sum(),decimals=3))
print('PV Fläche in m²              ',fr )
print('Solarstrom gesamt [kWh] :    ',np.around(np.sum(u, axis=0), decimals=3))

#print('batein:               ',np.around(np.sum(batein, axis=0), decimals=3))
#print('bataus:               ',np.around(np.sum(bataus, axis=0), decimals=3))
print('Netzbezug [kWh]:             ',np.around(np.sum(Netzbezug, axis=0), decimals=3))
print('Netzeinspeisung [kWh]:       ',np.around(np.sum(Netzeinspeisung, axis=0), decimals=3))
print(' ')
print('****                 Wirtschaftlichkeit                  ****        ')
print(' ')
print('Ersparniss [€/a]:            ',np.around(Ersparniss, decimals=2))
print('Installationskosten [€]:     ',Installationskosten)
print('Return on Investment [a]:    ',np.around(ROI, decimals=2))
print('CO2 Einsparung [kg]:         ',np.around(co2, decimals=2))
##
##x[x != 50] = x[x != 50] < 50


