# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 21:26:46 2019

@author: s0536
"""

import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D

timesteps =  52560                  #10 minütige Auflösung
df=pd.read_csv('QuartierHH.csv',nrows=timesteps) 




                    # Welches Element soll simuliert werden?? #
                    
Haushalt_2_11= True                 # Haushalt code 2.11 aus Datenrecherche_FHW.xlsx
HHQuartiergesamt = False            # Gesamtheit aller Haushalte im Quartier

EFHgesamt = False                   # noch nicht implementiert
MFHgesamt = False                   # noch nicht implementiert
GHDgesamt = False                   # noch nicht implementiert
Quartiergesamt = False              # noch nicht implementiert


                      # Grundparameter des Energiesystems #
                    
                    
Startkapazität=0                    # Startkapazität der Batterie in kWh
Kapazität = 5                       # Größe der gesamten Speicherkapazität in kWh
Wirkungsgrad_pv = 0.2
Systemwirkungsgrad_pv = 0.92        
Systemwirkungsgrad_bat = 0.881



                   # Dimensionierung des Anlagengrößenbereichs #


# Der nutzbare PV Flächen Bereich kann entweder über die vorhandene Dachfläche  
# und Dachausnutzung oder über Simulationsschrittweise festgelegt werden.
# Nur eines von Beiden ist möglich.   
                   
                   
Rechnung_über_Dachfläche = False    
Dachfläche = 80
Prozent_genutzteDachfläche_min = 40
Prozent_genutzteDachfläche_max = 45

Ausrichtung_Ost_West = True         # noch nicht implementiert
Ausrichtung_Nord_Süd = False        # noch nicht implementiert


Rechnung_über_Simulationsschritte = True
start = 0                           # Startwert der PV Anlagengröße in m²
Simulationsschritte = 5             # Anzahl der parallel simulierten PV Kapazitäten
Simulationsschrittweite = 4         # 1 entspricht 1m² pv/Simulationsschritt  


                              # Ergebnisse aus der Stoffstromanalyse und LCOA #

co2_Emmission_PV_pro_kWh = 80      # g/kWh   


                            # Strommix der aus dem Netz bereitgestellten Energie # 

Anteil_Windkraft              = 0  # in %. Die kumulierten Werte aller Anteile müssen 1 ergeben!  
Anteil_Braun_und_Steinkohle   = 0
Anteil_Wasserkraft            = 0  
Anteil_Solarstrom             = 0                          
deutscher_Strommix            = 1  
Anteil_Erdgas                 = 0        
Anteil_Atomkraft              = 0

                        ###      Gewichtung   der Optimierungskriterien      ###
                            ### gesamter Bereich noch nicht implementiert ###
                            
flexible_Energiemenge = 1          # Werte haben noch keine Auswirkungen auf die Simulation
An_Abfahrverhalten = 1
Planwertbasiertheit = 1
Lebenszykluskosten = 1
Systemintegrationskosten = 1
Emmissionen = 1
Kritikalität_Rohstoffe = 1
Effizienz = 1
Resilienz = 1


                          ###            3D Plots               ####

# True zeigt die entsprechende 3D Grafik
# False erstellt die Grafik nicht                

Vergleich_Flächepv_co2Einsparung_ROI = True 
Vergleich_Flächepv_co2Einsparung_Stromkostenersparniss = True 
Vergleich_Flächepv_co2Emmission_prokWh_Installationskosten = True 
Vergleich_Flächepv_Netzbezug_Netzeinspeisung = True             




### Simulation des Energiesystems startet ###

if Haushalt_2_11 == True:
  a = df['LAST_EFH']

if HHQuartiergesamt == True:
  a = df['LAST_HH']


b = df['pv']

n_pv = Wirkungsgrad_pv
nsys_pv= Systemwirkungsgrad_pv
nsys_bat = Systemwirkungsgrad_bat 


if Rechnung_über_Simulationsschritte == True: 
    test=Simulationsschritte
    s = Simulationsschrittweite

if Rechnung_über_Dachfläche == True: 
    test_float= (Prozent_genutzteDachfläche_max/100* Dachfläche - Prozent_genutzteDachfläche_min/100 * Dachfläche)
    test = int(test_float)
    s = 1 
    start = Prozent_genutzteDachfläche_min/100 * Dachfläche
q = np.zeros(shape=(timesteps,test))


for i in range(q.shape[0]):
    for j in range(q.shape[1]):
       
           q[i,j] = a[i] 
           
u = np.zeros(shape=(timesteps,test))


for i in range(u.shape[0]):
    for j in range(u.shape[1]):
       
           u[i,j] = b[i]*n_pv*nsys_pv * s *(j+1) + b[i]*n_pv*nsys_pv * start              


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



### Auswertung der Ergebnisse ###
            
co2faktor = 0.45 * deutscher_Strommix  + 1 * Anteil_Braun_und_Steinkohle + 0.08 * Anteil_Solarstrom
+ 0.01 * Anteil_Windkraft  + 0.001 * Anteil_Wasserkraft  + 0.5 *Anteil_Erdgas + 0.024 * Anteil_Atomkraft

            

Ersparniss= np.zeros(shape=(test))

for i in range(Ersparniss.shape[0]):
 
       Ersparniss[i]= (np.sum(q, axis=0)[i] -  (np.sum(Netzbezug, axis=0)[i])) *0.29 + (np.sum(Netzeinspeisung, axis=0)[i]) *0.12

            

Installationskosten = np.zeros(shape=(1,test))
for i in range(1):
   for j in range(test):
       Installationskosten[i,j]= (j+1)*250 * s + start *250 + Kapazität*500              

ROI= Installationskosten/Ersparniss

co2= np.zeros(shape=(test))

for i in range(co2.shape[0]):
 
       co2[i]= (np.around(a.sum()) - (np.sum(Netzbezug, axis=0)[i]))*co2faktor



avco2pkwh = (co2_Emmission_PV_pro_kWh * 0.001 *(np.around(np.sum(u, axis=0), decimals=3)-np.around(np.sum(Netzeinspeisung, axis=0), decimals=3))+ (np.sum(Netzbezug, axis=0))*co2faktor)/np.around(a.sum(),decimals=3)
#print(avco2pkwh)


co2inGeld = np.zeros(shape=(test))
for i in range(co2inGeld.shape[0]):
  
       co2inGeld[i] = co2[i]/1000 * 25  
       
       
fr = np.zeros(shape=(test))
for i in range(fr.shape[0]):
       
           fr[i] = (i+1 )* s  + start


Netzbezug1 = np.zeros(shape=(test))
for i in range(Netzbezug1.shape[0]):
       Netzbezug1[i] = np.around(np.sum(Netzbezug, axis=0), decimals=2)[i]
       
Netzeinspeisung1 = np.zeros(shape=(test))
for i in range(Netzeinspeisung1.shape[0]):
       Netzeinspeisung1[i] = np.around(np.sum(Netzeinspeisung, axis=0), decimals=2)[i]       


### Ausgabe der Ergebnisse ###


print(' ')
print('****                 Energiedaten                  ****        ')
print(' ')
print('Verbrauch [kWh]:          ',np.around(a.sum(),decimals=3))
print('PV Fläche in m²           ',fr )
print('Solarstrom gesamt [kWh] : ',np.around(np.sum(u, axis=0), decimals=3))

#print('batein:               ',np.around(np.sum(batein, axis=0), decimals=3))
#print('bataus:               ',np.around(np.sum(bataus, axis=0), decimals=3))
print('Netzbezug [kWh]:          ',np.around(np.sum(Netzbezug, axis=0), decimals=3))
print('Netzeinspeisung [kWh]:    ',np.around(np.sum(Netzeinspeisung, axis=0), decimals=3))
print(' ')
print('****                 Wirtschaftlichkeit                  ****        ')
print(' ')
print('Ersparniss [€/a]:         ',np.around(Ersparniss, decimals=2))
print('Installationskosten [€]:  ',Installationskosten)
print('Return on Investment [a]: ',np.around(ROI, decimals=2))
print(' ')
print('****                 CO2 Emmissionen                  ****        ')
print(' ')
print('CO2 Einsparung [kg/a]:    ',np.around(co2, decimals=2))
print('Durchschnitt CO2 Emmission pro kWh [kg/kWh]:',np.around(avco2pkwh, decimals=2))
##x[x != 50] = x[x != 50] < 50


### Plots ###

if Vergleich_Flächepv_co2Einsparung_ROI == True :
    plt.figure(1)
    ax = plt.gca(projection="3d")
    x,y,z = [fr],[co2],[ROI]


    ax.scatter(x,y,z, c='grey',s=70)

    ax.set_xlabel('PV Fläche in m²')
    ax.set_ylabel('vermiedene CO² Emmission in kg/a')
    ax.set_zlabel('Return on Investment in Jahren')

    
if Vergleich_Flächepv_co2Einsparung_Stromkostenersparniss == True :    
    plt.figure(2)
    ax = plt.gca(projection="3d")
    x,y,z = [fr],[co2],[Ersparniss]


    ax.scatter(x,y,z, c='grey',s=70)

    ax.set_xlabel('PV Fläche in m²')
    ax.set_ylabel('vermiedene CO² Emmission in kg/a')
    ax.set_zlabel('gesparte Stromkosten in €/a')
    
if Vergleich_Flächepv_co2Emmission_prokWh_Installationskosten == True :    
    plt.figure(3)
    ax = plt.gca(projection="3d")
    x,y,z = [fr],[avco2pkwh],[Installationskosten]


    ax.scatter(x,y,z, c='grey',s=70)

    ax.set_xlabel('PV Fläche in m²')
    ax.set_ylabel('Durchschnittliche CO² Emmission pro genutzter kWh  in kg/kWh')
    ax.set_zlabel('Installationskosten in €')    

if Vergleich_Flächepv_Netzbezug_Netzeinspeisung == True :    
    plt.figure(4)
    ax = plt.gca(projection="3d")
    x,y,z = [fr],[Netzbezug1],[Netzeinspeisung1]


    ax.scatter(x,y,z, c='grey',s=70)

    ax.set_xlabel('PV Fläche in m²')
    ax.set_ylabel('Netzbezug  in kWh/a')
    ax.set_zlabel('Netzeinspeisung  in kWh/a')      
plt.show()
