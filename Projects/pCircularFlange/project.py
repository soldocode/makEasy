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

import makEasy as ME
import types
import math
from dxfwrite import DXFEngine as dxf
import cStringIO
import json
from g2 import *


projectName='CircularFlange'
projectPath='pCircularFlange'
project=ME.Project(name=projectName,path=projectPath)
project.Title='Flangia Circolare'


def ValidateParameters(self,parameters):
    return True


def Execute(self,parameters):


    self.ProjectExecuted=True
    ValidateParameters(self,parameters)
    
    radius_est=float(parameters['dia_est'])/2
    radius_int=float(parameters['dia_int'])/2

    ### create Shape
    nd_ext=[Point(0,0),Point(radius_est,0.0)]
    nd_int=[Point(0,0),Point(radius_int,0.0)]
    path=[0,'Circle',1]
    p_ext=Path(nd_ext,path)
    p_int=Path(nd_int,path)
    shape=Shape(p_ext,[p_int])

    #### crea la sequenza di lavorazione ###
    ws_plasma=ME.WorkStep(ME.WORKSET['taglio_plasma'])
    ws_drill=ME.WorkStep(ME.WORKSET['drill'])


    # holes #
    centerx=0.0
    centery=0.0
    #cutid=1
    
    if 'holes' in parameters.keys():
        for holes in parameters['holes']:
            radius=float(holes['dia'])/2
            if holes['type']==1:#plasma cut
                if holes['intfo']<>'':
                    module=float(holes['intfo'])/2
                else:
                    module=0
                if holes['num']<>'':
                    nh=int(holes['num'])
                else:
                    nh=1
                angle_step=360.0/nh
                if holes['par']<>'':
                    angle_start=float(holes['par'])
                else:
                    angle_start=0.0
                for i in range(0,nh):
                    #cutid=cutid+1
                    cx=centerx+module*math.cos(math.radians(angle_start+angle_step*i))
                    cy=centery+module*math.sin(math.radians(angle_start+angle_step*i))
                    nodes=[Point(cx,cy),Point(cx+radius,cy)]
                    shape.internal.append(Path(nodes,path))

                shape.update()        
                
            elif holes['type']==2:#drill
                ws_drill={"WorkClass":"Foratura",
                          "Id":'',
                          "Nodes":wNodes,
                          "Chain":chain_list,
                          "BoundBox":bound_box,
                          "Time":1,
                          "Weight":1}

    

    work_flow=[ws_plasma,ws_drill]


    item=ME.Item()
    item.Class="sheet"
    item.Weight=shape.area['total']*parameters['thickness']*7.9/1000000
    item.ClassProperty={"Material":parameters['material'],"Thickness":parameters['thickness']}
    item.Project=ME.projectLibrary[projectName]
    item.ProjectParameters=parameters
    item.WorkFlow=work_flow
    return item




project.ValidateParameters = types.MethodType( ValidateParameters, project )
project.Execute = types.MethodType( Execute, project )
ME.projectLibrary[project.Name]= project
