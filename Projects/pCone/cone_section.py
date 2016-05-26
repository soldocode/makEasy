#################################################################
# Riccardo Soldini - 2015                                       #
#                                                               #
# Programma per determinare la sezione di un cono dati i        #
# seguenti parametri:                                           #
# - d   -> differenza tra i due diametri                        #
# - h   -> altezza totale tronco                                #
# - t   -> spessore                                             #
#                                                               #
#################################################################


import math

d=100.0
h=100.0
t=1

alfa=math.atan(d/h)
print 'alfa:',math.degrees(alfa)

h2=t*math.sin(alfa)
print 'h2:',h2
h1=h-h2
beta=math.atan(d/h1)
print beta
h2=t*math.sin(beta)
delta=h1+h2-h

while delta>0:
    h1=h-h2
    beta=math.atan(d/h1)
    h2=t*math.sin(beta)
    delta=h1+h2-h
    print delta

print 'h2:',h2
print 'h1:',h1
print 'h1+h2:',h1+h2
print 'beta:',math.degrees(beta)
print 'delta:',delta
