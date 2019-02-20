# Haushalt1
Update 20.02:
Die numerische Simulation läuft jetzt parallel über einen einstellbaren Bereich von PV Anlagengrößen. Ergebnisse werden als Matrix ausgegeben.
Kleine Anpassungen am System, wie Batteriewirkungsgrad & Systemwirkungsggrad wurden hinzugefügt. 



Update:
Wetter und Lastdaten sind aktualisiert. Die Berechnung erfolgt 10minütig. Die Modellierung kann zwischen einem Einfamilienhaus mit 2 Erwachsenen + 1 Kind oder den kumulierten Lastprofilen aller Haushalte des Quartiers unterschieden werden.
Oemof1 nutzt die oemof.solph Struktur während Algorhytmus1 das Energiesystem auf numerischer Basis simuliert. Beide Scripte erstellen diesselben Ergebnisse, wobei die numerische Variante schnellere Rechenzeiten hervorbringt und freier angepasst werden kann.



Hallo!

Ein erster Oemof Draft zur Darstellung eines Haushalts mit einer PV Anlage und einem Batteriespeicher.
Die Grafiken sind nur testweise mittels copy/paste entstanden und können vorerst vernachlässigt werden.
Die einzelnen Parameter sind im Code etwas genauer erklärt.
Auflösung der Daten ist vorerst stündlich.
Wetterdaten sind in Globalstrahlung in kWh/m² angegeben und entstammen der Messstation St. Peter Ording vom DWD.
Lastdaten sind in kWh angegeben und wurden mit dem LoadProfileGenerator auf Basis eines jährlichen Gesamtstromverbrauchs von 5300kWh für 
ein Einfamilienhaus generiert.

Durch ändern der Anlagengröße und Batteriekapazität mittels den jeweiligen nominal_values können die numerischen Auswirkungen 
(siehe  ***Main results***) auf Netzeinspeisung und Strombezug des Stromanbieters simuliert werden.


Wie gesagt erstmal nur ein sehr rudimentärer Draft zum vertraut Machen mit der oemof.solph library.  =)

Sollte der Code nicht laufen muss eventuell der filepath auf den jeweiligen Speicherort angepasst werden.






