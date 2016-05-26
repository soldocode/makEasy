#***************************************************************************
#*                                                                         *
#*   Project RectTube                                                      *
#*   2016                                                                  *
#*   Riccardo Soldini <riccardo.soldini@gmail.com>                         *
#*   Last Update: 10/05/16                                                 *
#*                                                                         *
#*                                                                         *
#* PARAMETERS:                                                             *
#*                                                                         *
#*                                                                         *
#***************************************************************************




__author__ = 'Riccardo Soldini'

import makEasy
import types
import math
from dxfwrite import DXFEngine as dxf
import cStringIO
import json


class RectTube(object):
    def __init__(self):
        self.dim=1
        

projectName='Tubo Rettangolare'
projectPath='pRectTube'
project=makEasy.Project(name=projectName,path=projectPath)


def ValidateParameters(self,parameters):

    return True


def Execute(self,parameters):
    self.ProjectExecuted=True
    ValidateParameters(self,parameters)
    print parameters

    #### calcola la sequenza di lavorazione ###
    work_flow=''

    item=makEasy.Item()
    item.Project=makEasy.projectLibrary[projectName]
    item.ProjectParameters=parameters
    item.WorkFlow=work_flow
    return item



def ExportDXF(self,param):
    output = cStringIO.StringIO()
    drawing = dxf.drawing('rectTube.dxf')

    cx=0
    cy=0
    cutid=1
    
    nf=[]
    nt=[]
    nl=[]


    #misure utili
    
    xz=0
    yz=0

    #Vista in Pianta
    

    
    # Vista di Fronte
    



    # Vista Laterale

   

    drawing.save_to_fileobj(output)
    dxf_result=[output.getvalue()]
    return dxf_result


project.ValidateParameters = types.MethodType( ValidateParameters, project )
project.Execute = types.MethodType( Execute, project )
project.ExportDXF = types.MethodType( ExportDXF, project )
makEasy.projectLibrary[project.Name]= project
