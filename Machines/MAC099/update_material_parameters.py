# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 19:14:32 2019

@author: Produzione
"""

import pyodbc
import json

#FARE UNA COPIA DELLA VERSIONE VECCHIA!!!!

MatPar={}
Gas={0:'Oxy',1:'Nit',2:'Air'}

drv='{Microsoft Access Driver (*.mdb, *.accdb)}'
dbq='V:\\MaterialDb.mdb'
#dbq='\MaterialDb.mdb'
#srv='http:\\10.0.0.199\Archivio\LAVORAZIONI\TAGLIO LASER'
#srv='\\CP-422004\Material'

conn = pyodbc.connect(r'Driver='+drv+';DBQ='+dbq+';')
cursor = conn.cursor()
for row in cursor.tables():
    print (row.table_name)

#cursor.execute('select * from MaterialTypes')
#rows=cursor.fetchall()
#print(rows)

cursor.execute('select * from Material')
rows=cursor.fetchall()
for row in rows:
    #print (row[0])
    if row[1] in MatPar:
        if row[2] in MatPar[row[1]]:
            MatPar[row[1]][row[2]][Gas[row[3]]]={}
        else:
            MatPar[row[1]][row[2]]={Gas[row[3]]:{}}
    else:
        MatPar[row[1]]={row[2]:{Gas[row[3]]:{}}}

    cursor.execute('select * from Cut2 where Material_ID='+str(row[0]))
    columns = [column[0] for column in cursor.description]
    #print (columns)
    speed_data=cursor.fetchall()
    MatPar[row[1]][row[2]][Gas[row[3]]]['Speed']=speed_data[0][4]
    MatPar[row[1]][row[2]][Gas[row[3]]]['GasPressure']=speed_data[0][6]
    MatPar[row[1]][row[2]][Gas[row[3]]]['NozzleType']=speed_data[0][11]
    MatPar[row[1]][row[2]][Gas[row[3]]]['PiercingTime']=600.00

    print (row[1],'-',row[2],'-',Gas[row[3]],':',speed_data[0][4])

    cursor.execute('select * from Pierce1 where Material_ID='+str(row[0]))
    columns = [column[0] for column in cursor.description]
    #print (columns)
    pierce_data=cursor.fetchall()
    ptp=pierce_data[0]
    #print(columns[3],pierce_data[0][3])
    #print(columns[7],pierce_data[0][7])
    #print(columns[23],pierce_data[0][23])
    #print(columns[28],pierce_data[0][28])
    #print(columns[42],pierce_data[0][42])
    #print(columns[47],pierce_data[0][47])
    #print(columns[50],pierce_data[0][50])
    #print(columns[54],pierce_data[0][54])
    #print(columns[61],pierce_data[0][61])
    #print(columns[68],pierce_data[0][68])
    #for d in range(48,len(columns)):
    #    print(d,'-',columns[d],pierce_data[0][d])
    pierce_time=ptp[3]*(ptp[7]+ptp[23]+ptp[28]+ptp[42])+ptp[47]*(ptp[50]+ptp[54]+ptp[61]+ptp[68])
    MatPar[row[1]][row[2]][Gas[row[3]]]['PiercingTime']=pierce_time


#print (MatPar)


#cursor.execute('select * from Cut2 where Material_ID='+row[0])
#columns = [column[0] for column in cursor.description]
#print (columns)
#rows=cursor.fetchall()

#for row in rows:
#    print (row)


f = open("MaterialParameters.json", "w")
f.write(json.dumps(MatPar))
f.close()
