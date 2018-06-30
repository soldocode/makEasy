###############################################################################
# Assembly - work.py - 2018
#
# Riccardo Soldini - riccardo.soldini@gmail.com
###############################################################################


import makEasy
import math,g2
from dxfwrite import DXFEngine as dxf

def Execute ():
    job = makEasy.Job()

    return job

def WorkOut(args):
    tLoad=5
    tTool=10
    tWork=1
    tMove=1
    tLook=2

    res={"time":tLoad+tTool+tWork+tMove+tLook}
    return res

#def getData (machine,blocks,parameters):
#    print (machine.Name)
#    return

def updateWorkData (machine,blocks,parameters):
    print (machine.Name)
    print (blocks)
    print (parameters)
   
    total_area=0
    t_load=parameters['Load']['CTime']
    t_move=0
    t_work=0
    t_dwld=0
    weight_blocks=0


    return
    


def getDXF (data):
    dwg=g2.Drawing()
    dwg.insertGeo('work',data['shape'])
    print(dwg.boundBox)
    dxf_result=dwg.getDXF()
    return dxf_result


work=makEasy.Work('Assembly','Assiemaggio')
work.Folder='wAssembly'
work.Execute=Execute
work.updateWorkData=updateWorkData
#work.getData=getData
work.getDXF=getDXF

makEasy.WORKSET[work.Class]= work
