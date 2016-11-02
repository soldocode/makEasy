#***************************************************************************
#*                                                                         *
#*   Project PIASTRA                                                       *
#*   Copyright (c) 2015                                                    *
#*   Riccardo Soldini <riccardo.soldini@gmail.com>                         *
#*                                                                         *
#*                                                                         *
#* PARAMETERS:                                                             *
#*                                                                         *
#*  - shape     -> sagoma (rettangolare, circolare)                        *
#*  - width     -> larghezza                                               *
#*  - height    -> altezza                                                 *
#*  - thickness -> spessore                                                *
#*  - holes     -> foratura                                                *
#*    - holes_work  -> lavorazione                                         *
#*    - holes_dia   -> diametro                                            *
#*    - holes_num   -> numero fori                                         *
#*    - holes_dist  -> interasse foratura                                  *
#*    - holes_start -> angolo primo foro                                   *
#*  - material  -> materiale                                               *
#*                                                                         *
#***************************************************************************




__author__ = 'Riccardo'

import makEasy
import types
import math
from dxfwrite import DXFEngine as dxf
import cStringIO
import json



projectName='Piastra'
projectPath='pPlate'
project=makEasy.Project(name=projectName,path=projectPath)


def ValidateParameters(self,parameters):

    return True


def Execute(self,parameters):
    self.ProjectExecuted=True
    ValidateParameters(self,parameters)
    #print json.dumps(parameters, sort_keys=False, indent=4)


    wsPlasma={}
    wsDrill={}

    #### calcola la sequenza di lavorazione Plasma###
    ##workClass='Taglio Plasma'
    wNodes=[{'X':0,'Y':0}]
    countNodes=0


    # sagoma piastra #
    if parameters['shape']==1:
        xcorn=float(parameters['misure2'])/2
        ycorn=float(parameters['misure3'])/2


        wNodes.append({'X':-xcorn,'Y':ycorn})
        wNodes.append({'X':-xcorn,'Y':-ycorn})
        wNodes.append({'X':xcorn,'Y':-ycorn})
        wNodes.append({'X':xcorn,'Y':ycorn})
        countNodes=4

        chain_list=[[["Line",1,2],["Line",2,3],["Line",3,4],["Line",4,1]]]

        bound_box={"Xmin":-xcorn,
                   "Ymin":-ycorn,
                   "Xmax":xcorn,
                   "Ymax":ycorn}



    if parameters['shape']==2:
        radius=float(parameters['misure4'])/2

        wNodes.append({'X':radius,'Y':0})
        countNodes=1

        chain_list=[[["Circle",0,1]]]

        bound_box={"Xmin":-radius,
                   "Ymin":-radius,
                   "Xmax":radius,
                   "Ymax":radius}

    # holes #
    centerx=0.0
    centery=0.0
    cutid=1
    if 'holes' in parameters.keys():
        for holes in parameters['holes']:
            if holes['work']==1:#taglio plasma
                if holes['intfo']<>'':
                    modulo=float(holes['intfo'])/2
                else:
                    modulo=0

                if holes['num']<>'':
                    numfori=int(holes['num'])
                else:
                    numfori=1

                if holes['par']<>'':
                    angpar=float(holes['par'])
                else:
                    angpar=0.0

                angpasso=360.0/numfori
                for i in range(0,numfori):
                    cutid=cutid+1
                    cx=centerx+modulo*math.cos(math.radians(angpar+angpasso*i))
                    cy=centery+modulo*math.sin(math.radians(angpar+angpasso*i))
                    wNodes.append({'X':cx,'Y':cy})
                    wNodes.append({'X':cx+float(holes['dia'])/2,'Y':cy})
                    chain_list.append([["Circle",countNodes+1,countNodes+2]])
                    countNodes=countNodes+2
            elif holes['work']==2:#foratura
                wsDrill={"WorkClass":"Foratura",
                         "Id":'',
                         "Nodes":wNodes,
                         "Chain":chain_list,
                         "BoundBox":bound_box,
                         "Time":1,
                         "Weight":1}


    wsPlasma={"WorkClass":"Taglio Plasma",
              "Id":'',
              "Nodes":wNodes,
              "Chain":chain_list,
              "BoundBox":bound_box,
              "Time":1,
              "Weight":1
             }

    work_flow=[wsPlasma]


    item=makEasy.Item()
    item.Class="sheet"
    item.ClassProperty={"Material":"Fe","Thickness":parameters['misure1']}
    item.Project=makEasy.projectLibrary[projectName]
    item.ProjectParameters=parameters
    item.WorkFlow=work_flow
    return item






project.ValidateParameters = types.MethodType( ValidateParameters, project )
project.Execute = types.MethodType( Execute, project )
#project.ExportDXF = types.MethodType( ExportDXF, project )
makEasy.projectLibrary[project.Name]= project
