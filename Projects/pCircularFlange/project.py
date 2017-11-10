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
import sys
import json
from g2 import *

if sys.version_info[0]==3:
    import io
else:    
    import cStringIO as io


projectName='CircularFlange'
projectPath='pCircularFlange'
project=ME.Project(name=projectName,path=projectPath)
project.Title='Flangia Circolare'


def ValidateParameters(self,parameters):
    return True


def Execute(self,parameters):
    
    #mat_id=parameters['material']+'|'+str(parameters['thickness'])
    
    #var_plasma=ME.MACHINES['PLA01'].getParameters(mat_id)

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

    #### create working sequence ###
    ws_plasma=ME.WorkStep(ME.WORKSET['PlasmaCut'])
    ws_drill=ME.WorkStep(ME.WORKSET['drill'])


    # holes #
    centerx=0.0
    centery=0.0
    
    if len(parameters['holes'])>0:
        for holes in parameters['holes']:
            radius=float(holes['circular_holes_dia'])/2
            if holes['circular_holes_type']==1:#plasma cut
                if holes['intfo']!='':
                    module=float(holes['intfo'])/2
                else:
                    module=0
                if holes['num']!='':
                    nh=int(holes['num'])
                else:
                    nh=1
                angle_step=360.0/nh
                if holes['par']!='':
                    angle_start=float(holes['par'])
                else:
                    angle_start=0.0
                for i in range(0,nh):
                    cx=centerx+module*math.cos(math.radians(angle_start+angle_step*i))
                    cy=centery+module*math.sin(math.radians(angle_start+angle_step*i))
                    nodes=[Point(cx,cy),Point(cx+radius,cy)]
                    shape.internal.append(Path(nodes,path))

                #shape.update() 
                #ws_plasma.Data={'shape':shape}       
                
            elif holes['circular_holes_type']==2:#drill
                ws_drill={"WorkClass":"Foratura",
                          "Id":'',
                          "Nodes":wNodes,
                          "Chain":chain_list,
                          "BoundBox":bound_box,
                          "Time":1,
                          "Weight":1}

    #### evaluate time production
    shape.update() 
    ws_plasma.Data={'shape':shape}

    work_flow=[ws_plasma,ws_drill]


    item=ME.Item()
    item.Class="sheet"
    item.Weight=shape.area['total']*parameters['sheet_thk']*7.9/1000000
    item.ClassProperties={"Material":parameters['sheet_mat'],"Thickness":parameters['sheet_thk']}
    item.Project=ME.projectLibrary[projectName]
    item.ProjectParameters=parameters
    item.WorkFlow=work_flow
    return item




project.ValidateParameters = types.MethodType( ValidateParameters, project )
project.Execute = types.MethodType( Execute, project )
ME.projectLibrary[project.Name]= project
