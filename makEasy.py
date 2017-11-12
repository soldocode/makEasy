#***************************************************************************
#*                                                                         *
#*   makEasy - python module - 2015                                        *
#*   Riccardo Soldini <riccardo.soldini@gmail.com>                         *
#*   Last Update:21/10/17
#*                                                                         *
#***************************************************************************

import jsonpickle
from dxfwrite import DXFEngine as dxf
import geoFun, math
import sys

if sys.version_info[0]==3:
    import io
else:    
    import cStringIO as io


jsonpickle.set_encoder_options('simplejson', indent=4)


class Project(object):
    def __init__(self,
                 project_id=None,
                 name='',
                 description='',
                 path=''):

        self.ID = project_id
        self.Name = name
        self.Description = description
        self.Path =path


class Material(object):
    def __init__(self,
                Id=None,
                Thickness=0):
        self.Id=Id
        self.Thickness=Thickness


#class Position(object): ### forse non va bene qui
#    def __init__(self,
#                 x=0, y=0, z=0,
#                 xrot=0, yrot=0, zrot=0):

#        self.X = x
#        self.Y = y
#        self.Z = z
#        self.XRot = xrot
#        self.YRot = yrot
#        self.ZRot = zrot


class Item(object):
    def __init__(self,
                 Title='',
                 Project=None,
                 Class=None,
                 Id=None):
        self.Id = Id
        self.Class = Class  #'assembly','sheet','profile?','component'
        self.ClassProperty=None
        self.ClassProperties={}
        self.Title = Title
        self.Project = Project
        self.ProjectParameters = {}
        self.Prices = None
        self.Weight = 0
        self.Position = None # forse non serve qui
        self.FreeCADObj = None
        self.WorkFlow = []


    def ValidateProjectParameters(self):
        self.Project.ValidateParameters(self.ProjectParameters)
        self.ProjectParametersValidated=True
        return True

        
    def toJson(self):
        jsonItem=jsonpickle.encode(self)
        return jsonItem

        
    def addWork(self,wClass):
        self.WorkFlow.append({"Class":wClass,
                              "Time":0})
        return len(self.WorkFlow)

        
    def SaveAs(filePath):
        jp=jsonpickle.encode(self)
#        print jp
        return
               
        
    def ExportDXF (self):
        output = io.StringIO()
        drawing = dxf.drawing('c:/item.dxf')
        if len(self.WorkFlow)>0:
            works=self.WorkFlow
            for work in works:
                if work[0].Class=='PlasmaCut':
                    nodes=work[1]['Nodes']
                    chains=work[1]['Chain']
                    if len(chains)>0:
                        for chain in chains:
                            for geo in chain:

                                if geo[0]=='Line':
                                    print ('Line')
                                    drawing.add(dxf.line((nodes[geo[1]]['X'],
                                                          nodes[geo[1]]['Y']),
                                                         (nodes[geo[2]]['X'],
                                                          nodes[geo[2]]['Y'])))
                                elif geo[0]=='Arc':
                                    print('arc')
                                    arcgen=geoFun.CircleFrom3Points([nodes[geo[1]]['X'],
                                                                     nodes[geo[1]]['Y']],
                                                                    [nodes[geo[3]]['X'],
                                                                     nodes[geo[3]]['Y']],
                                                                    [nodes[geo[2]]['X'],
                                                                     nodes[geo[2]]['Y']])

                                    if arcgen['Direction']>0:
                                        drawing.add(dxf.arc(arcgen['Radius'],
                                                           (arcgen['Center'][0],arcgen['Center'][1]),
                                                            math.degrees(arcgen['P3Degree']),
                                                            math.degrees(arcgen['P1Degree'])))
                                    else:
                                        drawing.add(dxf.arc(arcgen['Radius'],
                                                           (arcgen['Center'][0],arcgen['Center'][1]),
                                                            math.degrees(arcgen['P1Degree']),
                                                            math.degrees(arcgen['P3Degree'])))



                                elif geo[0]=='Circle':
                                    print('circle')
                                    radius=nodes[geo[2]]['X']-nodes[geo[1]]['X']
                                    drawing.add(dxf.circle(radius,(nodes[geo[1]]['X'], nodes[geo[1]]['Y'])))

        drawing.save_to_fileobj(output)
        dxf_result=[output.getvalue()]

        return dxf_result


class WorkStep(object):
    def __init__(self,w,d={}):
        self.Id = None
        #self.Times = {'total':0}
        self.Work = w
        self.Data = d
        self.WorkData = {}
        self.Item = None
        self.WorkPlan = None
        #self.Costs = {'total':0}
        
    def getDXF(self):
        return self.Work.getDXF(self.Data) 
    
    def saveAs(self,file_type,file_path):
        content_to_save={'DXF':self.getDXF}
        content=content_to_save[file_type]()
        f=open(file_path+"."+file_type,'w')
        f.write(content)
        f.close()
        return
        
        
    def __repr__(self):
        return repr(self.Work)+" on "+repr(self.Item)


class Work(object):
    def __init__(self,
                 wclass=None,
                 wtitle=None):
        self.Id = None
        self.Title = wtitle
        self.Class = wclass
       
    def __repr__(self):
        return  str(self.Class)     


class WorkPlan(object):
    def __init__(self,
                 ID=None,
                 Title="WP",
                 Class=None):
        self.ID = ID
        self.Title = Title
        self.ClassWork = Class
        self.Machine = None
        self.Parameters ={}
        self.Items= []
        self.Positions = [] #?????
        self.JobSequence = []
        self.Times={}
        
    def updateWorkData(self):#????????????????
        blocks=[]
        times={}
        for i in self.Items:
            for step in i.WorkFlow:
               if self.ClassWork==step.Work:
                   blocks.append(step)
        times=self.ClassWork.getData(self.Machine,blocks,self.Parameters)          
        return times
        
        
    def getTimes(self):
        blocks=[]
        times={}
        for i in self.Items:
            for step in i.WorkFlow:
               if self.ClassWork==step.Work:
                   blocks.append(step)
        times=self.ClassWork.getData(self.Machine,blocks,self.Parameters)          
        return times


class Machine(object):
    def __init__(self,Id=None,Name=""):
        self.Id=Id
        self.Name=Name
        self.MacProperties={}
        self.TimeParameters={}
        
    def getParameters(self,material):
        return {}


projectLibrary={}
WORKSET = {}
MATERIALS ={}
MACHINES={}

TTimes={"Load",
         "Tool",
         "Move",
         "Work",
         "Look",
         "DwLd"}


from Works import *
from Projects import *
from Machines import *
import Materials


def newItemFromProject(projectName,parameters,Id=None):

    item=projectLibrary[projectName].Execute(parameters)
    item.Id=Id
    jp=jsonpickle.encode(item)
    #print jp

    return item

