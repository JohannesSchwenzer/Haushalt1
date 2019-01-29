# Haushalt1

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






