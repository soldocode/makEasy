#***************************************************************************
#*                                                                         *
#*   Project CircularFlange                                                *
#*   Copyright (c) 2017                                                    *
#*   Riccardo Soldini <riccardo.soldini@gmail.com>                         *
#*                                                                         *
#*                                                                         *
#* PARAMETERS:                                                             *
#*                                                                         *
#*  - material  -> materiale                                               *
#*  - thickness -> spessore                                                *
#*  - dia_est   -> diametro esterno                                        *
#*  - dia_int   -> diametro interno                                        *
#*  - holes     -> foratura                                                *
#*      - type    -> lavorazione                                           *
#*      - dia     -> diametro                                              *
#*      - num     -> numero fori                                           *
#*      - intfo   -> interasse foratura                                    *
#*      - par     -> angolo primo foro                                     *
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


projectName='CircularFlange'
projectPath='pCircularFlange'
project=makEasy.Project(name=projectName,path=projectPath)
project.Title='Flangia Circolare'


def ValidateParameters(self,parameters):

    return True


def Execute(self,parameters):


    self.ProjectExecuted=True
    ValidateParameters(self,parameters)
    #print json.dumps(parameters, sort_keys=False, indent=4)

    wsPlasma={}
    ws=makEasy.WORKSET['taglio_plasma']

    #### calcola la sequenza di lavorazione Plasma###
    ##workClass='Taglio Plasma'
    wNodes=[{'X':0,'Y':0}]
    countNodes=0


    # sagoma piastra #

    radius_est=float(parameters['dia_est'])/2
    radius_int=float(parameters['dia_int'])/2

    area=math.pow(radius_est,2)*math.pi
    area-=math.pow(radius_int,2)*math.pi

    wNodes.append({'X':radius_est,'Y':0})
    wNodes.append({'X':radius_int,'Y':0})
    countNodes=2

    chain_list=[[["Circle",0,1]],[["Circle",0,2]]]

    bound_box={"Xmin":-radius_est,
               "Ymin":-radius_est,
               "Xmax":radius_est,
               "Ymax":radius_est}

    # holes #
    centerx=0.0
    centery=0.0
    cutid=1
    if 'holes' in parameters.keys():
        for holes in parameters['holes']:

            radius=float(holes['dia'])/2
            hole_area=math.pow(radius,2)*math.pi

            if holes['type']==1:#taglio plasma

                if holes['intfo']<>'':
                    modulo=float(holes['intfo'])/2
                else:
                    modulo=0

                if holes['num']<>'':
                    numfori=int(holes['num'])
                else:
                    numfori=1

                angpasso=360.0/numfori

                if holes['par']<>'':
                    angpar=float(holes['par'])
                else:
                    angpar=0.0

                for i in range(0,numfori):
                    cutid=cutid+1
                    cx=centerx+modulo*math.cos(math.radians(angpar+angpasso*i))
                    cy=centery+modulo*math.sin(math.radians(angpar+angpasso*i))
                    area-=hole_area
                    wNodes.append({'X':cx,'Y':cy})
                    wNodes.append({'X':cx+radius,'Y':cy})
                    chain_list.append([["Circle",countNodes+1,countNodes+2]])
                    countNodes=countNodes+2
            elif holes['type']==2:#foratura
                wsDrill={"WorkClass":"Foratura",
                         "Id":'',
                         "Nodes":wNodes,
                         "Chain":chain_list,
                         "BoundBox":bound_box,
                         "Time":1,
                         "Weight":1}




    Data={
             "Nodes":wNodes,
             "Chain":chain_list,
             "BoundBox":bound_box
            }


    work_flow=[[ws,Data]]


    item=makEasy.Item()
    item.Class="sheet"
    item.Weight=area*parameters['thickness']*7.9/1000000
    item.ClassProperty={"Material":parameters['material'],"Thickness":parameters['thickness']}
    item.Project=makEasy.projectLibrary[projectName]
    item.ProjectParameters=parameters
    item.WorkFlow=work_flow
    return item






project.ValidateParameters = types.MethodType( ValidateParameters, project )
project.Execute = types.MethodType( Execute, project )
makEasy.projectLibrary[project.Name]= project