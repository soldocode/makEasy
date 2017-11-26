#***************************************************************************
#*                                                                         *
#*   Project TRONCO DI CONO                                                *
#*   2015-2016                                                             *
#*   Riccardo Soldini <riccardo.soldini@gmail.com>                         *
#*                                                                         *
#* PARAMETERS:                                                             *
#*  - dia_max   -> diametro maggiore                                       *
#*  - dia_min   -> diametro minore                                         *
#*  - height    -> altezza                                                 *
#*  - thickness -> spessore                                                *
#*  - parts     -> nr parti divisione                                      *
#***************************************************************************

__author__ = 'Riccardo'


import makEasy
import types
import math
import json
from g2 import *


projectName='Tronco di Cono'
projectPath='pCone'
project=makEasy.Project(name=projectName,path=projectPath)
project.Title="Tronco di Cono"


def ValidateParameters(self,parameters):
    if not('dia_max' in parameters):parameters['dia_max']=0.0
    if not('dia_min' in parameters):parameters['dia_min']=0.0
    if not('height' in parameters):parameters['height']=0.0
    if not('sheet_thk' in parameters):parameters['sheet_thk']=0.0
    return True


def Execute(self,parameters):
    ValidateParameters(self,parameters)

    ### get section ###
    mat=parameters['sheet_mat']
    d=float((parameters['dia_max']-parameters['dia_min']))/2
    h=float(parameters['height'])
    t=float(parameters['sheet_thk'])
    alfa=math.atan(d/h)
    h2=t*math.sin(alfa)
    h1=h-h2
    beta=math.atan(d/h1)
    h2=t*math.sin(beta)
    delta=h1+h2-h
    while delta>0:
        h1=h-h2
        beta=math.atan(d/h1)
        h2=t*math.sin(beta)
        delta=h1+h2-h
    tdiff=math.sqrt(math.pow(t,2)-math.pow(h2,2))

    ### develop cone ###
    diam_max=float(parameters['dia_max']-tdiff)
    diam_min=float(parameters['dia_min']-tdiff)
    oblique_side=math.sqrt(math.pow(d,2)+math.pow(h1,2))
    greater_circ=diam_max*math.pi
    greater_radius_dev=oblique_side/d*(diam_max/2)
    smaller_radius_dev=greater_radius_dev-oblique_side
    greater_circ_dev=greater_radius_dev*2*math.pi
    dev_degree=360/greater_circ_dev*greater_circ
    dev_degree=dev_degree/parameters['parts']

    ### create Shape
    nd=[Point(0,0)]
    sin_alfa=math.sin(math.radians(90-dev_degree/2))
    cos_alfa=math.cos(math.radians(90-dev_degree/2))
    sin_beta=math.sin(math.radians(90+dev_degree/2))
    cos_beta=math.cos(math.radians(90+dev_degree/2))
    nd.append(Point(smaller_radius_dev*cos_alfa,smaller_radius_dev*sin_alfa))
    nd.append(Point(0,smaller_radius_dev))
    nd.append(Point(smaller_radius_dev*cos_beta,smaller_radius_dev*sin_beta))
    nd.append(Point(greater_radius_dev*cos_beta,greater_radius_dev*sin_beta))
    nd.append(Point(0,greater_radius_dev))
    nd.append(Point(greater_radius_dev*cos_alfa,greater_radius_dev*sin_alfa))
    ch=[3,'Arc',2,1,'Line',6,'Arc',5,4,'Line',3]
    p_ext=Path(nd,ch)
    shape=Shape(p_ext)


    #### create working sequence ###
    ws_plasma=makEasy.WorkStep(makEasy.WORKSET['PlasmaCut'])

    #### evaluate time production
    shape.update()
    ws_plasma.Data={'shape':shape}

    work_flow=[ws_plasma]

    ### create item
    item=makEasy.Item()
    item.Class="sheet"
    item.ClassProperties={"Material":mat,"Thickness":t}
    item.Weight=shape.area['total']*t*makEasy.MATERIALS[mat]['weight']
    item.Project=makEasy.projectLibrary[projectName]
    item.ProjectParameters=parameters
    item.WorkFlow=work_flow
    return item




def Execute_old(self,parameters):
    self.ProjectExecuted=True
    ValidateParameters(self,parameters)

    ### calcola la sezione di sviluppo ###
    d=float((parameters['dia_max']-parameters['dia_min']))/2
    h=float(parameters['height'])
    t=float(parameters['sheet_thk'])

    alfa=math.atan(d/h)
    #print 'alfa:',math.degrees(alfa)

    h2=t*math.sin(alfa)
    #print 'h2:',h2
    h1=h-h2
    beta=math.atan(d/h1)
    #print beta
    h2=t*math.sin(beta)
    delta=h1+h2-h

    while delta>0:
        h1=h-h2
        beta=math.atan(d/h1)
        h2=t*math.sin(beta)
        delta=h1+h2-h
        #print delta

    #print 'h2:',h2
    #print 'h1:',h1
    #print 'h1+h2:',h1+h2
    #print 'beta:',math.degrees(beta)
    #print 'delta:',delta

    tdiff=math.sqrt(math.pow(t,2)-math.pow(h2,2))
    #print 'tdiff:',tdiff



    ### calcola lo sviluppo del cono ###
    diam_max=float(parameters['dia_max']-tdiff)
    #print diam_max
    diam_min=float(parameters['dia_min']-tdiff)
    oblique_side=math.sqrt(math.pow(d,2)+math.pow(h1,2))
    greater_circ=diam_max*math.pi
    greater_radius_dev=oblique_side/d*(diam_max/2)
    smaller_radius_dev=greater_radius_dev-oblique_side
    greater_circ_dev=greater_radius_dev*2*math.pi
    dev_degree=360/greater_circ_dev*greater_circ

    #print 'grater_radius_dev:',greater_radius_dev
    #print 'smaller_radius_dev',smaller_radius_dev
    #print 'dev_degree',dev_degree

    dev_degree=dev_degree/parameters['parts']


    #### calcola il peso ####
    area=(math.pow(greater_radius_dev,2)-math.pow(smaller_radius_dev,2))*math.pi
    w=((area/1000000)*7.9*t)/360*dev_degree


    #### calcola la sequenza di lavorazione ###
    work_flow=[]

    ## Taglio Plasma ##
    work=makEasy.WORKSET['PlasmaCut']
    wNodes=[{'X':0,'Y':0}]
    sin_alfa=math.sin(math.radians(90-dev_degree/2))
    cos_alfa=math.cos(math.radians(90-dev_degree/2))
    sin_beta=math.sin(math.radians(90+dev_degree/2))
    cos_beta=math.cos(math.radians(90+dev_degree/2))
    wNodes.append({'X':smaller_radius_dev*cos_alfa,'Y':smaller_radius_dev*sin_alfa})
    wNodes.append({'X':0,'Y':smaller_radius_dev})
    wNodes.append({'X':smaller_radius_dev*cos_beta,'Y':smaller_radius_dev*sin_beta})
    wNodes.append({'X':greater_radius_dev*cos_beta,'Y':greater_radius_dev*sin_beta})
    wNodes.append({'X':0,'Y':greater_radius_dev})
    wNodes.append({'X':greater_radius_dev*cos_alfa,'Y':greater_radius_dev*sin_alfa})
    #print 'Nodes:'
    #for i in wNodes: print i

    chain_list=[[["Arc",3,1,2],["Line",1,6],["Arc",6,4,5],["Line",4,3]]]

    if dev_degree>180:
        bound_box={"Xmin":-greater_radius_dev,
                   "Ymin":wNodes[4]['Y'],
                   "Xmax":greater_radius_dev,
                   "Ymax":greater_radius_dev}
    else:
        bound_box={"Xmin":wNodes[4]['X'],
                   "Ymin":wNodes[3]['Y'],
                   "Xmax":wNodes[6]['X'],
                   "Ymax":greater_radius_dev}


    shift_y=bound_box['Ymin']+(bound_box['Ymax']-bound_box['Ymin'])/2

    for count in range(0,len(wNodes)):
        wNodes[count]['Y']=wNodes[count]['Y']-shift_y
    bound_box['Ymin']=bound_box['Ymin']-shift_y
    bound_box['Ymax']=bound_box['Ymax']-shift_y


    Data={  "Nodes":wNodes,
             "Chain":chain_list,
             "BoundBox":bound_box
            }


    work_flow.append([work,Data])


    ## calandratura/piegatura ##
    if diam_min<500: #questo valore va sostituito con il d minimo della calandra
        work=makEasy.WORKSET['piegatura']
    else:
        work=makEasy.WORKSET['calandratura']

    work_flow.append([work,{}])


    item=makEasy.Item()
    item.Class="sheet"
    item.Weight=w
    item.ClassProperty={"Material":"Fe","Thickness":parameters['sheet_thk']}
    item.Project=makEasy.projectLibrary[projectName]
    item.ProjectParameters=parameters
    item.WorkFlow=work_flow
    return item




project.ValidateParameters = types.MethodType( ValidateParameters, project )
project.Execute = types.MethodType( Execute, project )
#project.ExportDXF = types.MethodType( ExportDXF, project )
makEasy.projectLibrary[project.Name]= project
