#***************************************************************************
#*                                                                         *
#*   Project CICLONE                                                      *
#*   Copyright (c) 2015                                                    *
#*   Riccardo Soldini <riccardo.soldini@gmail.com>                         *
#*                                                                         *
#*                                                                         *
#* PARAMETERS:                                                             *
#*                                                                         *
#*                                                                         *
#***************************************************************************




__author__ = 'Riccardo'

import makEasy
import types
import math
from dxfwrite import DXFEngine as dxf
import cStringIO
import json



projectName='Ciclone'
projectPath='pCyclon'
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
    item.Class="assembly"
    item.ClassProperty={"Material":"Fe"}
    item.Project=makEasy.projectLibrary[projectName]
    item.ProjectParameters=parameters
    item.WorkFlow=work_flow
    return item



def ExportDXF(self,param):
    output = cStringIO.StringIO()
    drawing = dxf.drawing('cyclon.dxf')

    cx=0
    cy=0
    cutid=1
    
    nf=[]
    nt=[]
    nl=[]


    #misure utili
    htot=param['mantello']['altezza']+param['sezione_interna']['parte_esterna']+param['cono_inferiore']['altezza_totale']

    d=param['mantello']['dia']
    dint=param['sezione_interna']['dia']
    hcono=param['cono_inferiore']['altezza_totale']-param['cono_inferiore']['tronco_diritto']

    xz=0
    yz=0

    #Vista in Pianta
    xz=0-d
    yz=xz

    drawing.add(dxf.circle(d/2,(xz,yz)))
    drawing.add(dxf.circle(dint/2,(xz,yz)))

    
    # Vista di Fronte
    yz=d*0.5+param['cono_inferiore']['altezza_totale']
    h=param['mantello']['altezza']
    nf.append([xz-d/2,yz])
    nf.append([xz+d/2,yz])
    drawing.add(dxf.rectangle((nf[0][0],nf[0][1]),d,h))
    nf.append([xz-param['cono_inferiore']['diametro_finale']/2,yz-hcono])
    nf.append([xz+param['cono_inferiore']['diametro_finale']/2,yz-hcono])
    nf.append([nf[2][0],nf[2][1]-param['cono_inferiore']['tronco_diritto']])
    nf.append([nf[3][0],nf[3][1]-param['cono_inferiore']['tronco_diritto']])
    drawing.add(dxf.line((nf[0][0],nf[0][1]),(nf[2][0],nf[2][1])))
    drawing.add(dxf.line((nf[2][0],nf[2][1]),(nf[3][0],nf[3][1])))
    drawing.add(dxf.line((nf[3][0],nf[3][1]),(nf[1][0],nf[1][1])))
    drawing.add(dxf.line((nf[2][0],nf[2][1]),(nf[4][0],nf[4][1])))
    drawing.add(dxf.line((nf[4][0],nf[4][1]),(nf[5][0],nf[5][1])))
    drawing.add(dxf.line((nf[5][0],nf[5][1]),(nf[3][0],nf[3][1])))



    # Vista Laterale

    for i in nf:
       nl.append([i[0]+d*2,i[1]])

    drawing.add(dxf.rectangle((nl[0][0],nl[0][1]),d,h))
    drawing.add(dxf.line((nl[0][0],nl[0][1]),(nl[2][0],nl[2][1])))
    drawing.add(dxf.line((nl[2][0],nl[2][1]),(nl[3][0],nl[3][1])))
    drawing.add(dxf.line((nl[3][0],nl[3][1]),(nl[1][0],nl[1][1])))
    drawing.add(dxf.line((nl[2][0],nl[2][1]),(nl[4][0],nl[4][1])))
    drawing.add(dxf.line((nl[4][0],nl[4][1]),(nl[5][0],nl[5][1])))
    drawing.add(dxf.line((nl[5][0],nl[5][1]),(nl[3][0],nl[3][1])))

    drawing.save_to_fileobj(output)
    dxf_result=[output.getvalue()]
    return dxf_result


project.ValidateParameters = types.MethodType( ValidateParameters, project )
project.Execute = types.MethodType( Execute, project )
project.ExportDXF = types.MethodType( ExportDXF, project )
makEasy.projectLibrary[project.Name]= project
