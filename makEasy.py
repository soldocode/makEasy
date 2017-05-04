#***************************************************************************
#*                                                                         *
#*   makEasy - python module - 2015                                        *
#*   Riccardo Soldini <riccardo.soldini@gmail.com>                         *
#*   Last Update:23/06/16
#*                                                                         *
#***************************************************************************

import jsonpickle
from dxfwrite import DXFEngine as dxf
import geoFun, math
import cStringIO

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


class Position(object):
    def __init__(self,
                 x=0, y=0, z=0,
                 xrot=0, yrot=0, zrot=0):
        """

        :type yrot: object
        """
        self.X = x
        self.Y = y
        self.Z = z
        self.XRot = xrot
        self.YRot = yrot
        self.ZRot = zrot


class Item(object):
    def __init__(self,
                 ID=None,
                 Title='',
                 Project=None,
                 Class=None):
        self.Id = ID
        self.Class = Class  #'assembly','sheet','profile?','component'
        self.ClassProperty=None
        self.Title = Title
        self.Project = Project
        self.ProjectParameters = {}
        self.Prices = None
        self.Weight = 0
        self.Position = Position()
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
        self.WorkFlow.append({"WorkClass":wClass,
                              "Time":0})
        return len(self.WorkFlow)


    def SaveAs(filePath):
        jp=jsonpickle.encode(self)
        print jp
        return



    def ExportDXF (self):
        output = cStringIO.StringIO()
        drawing = dxf.drawing('c:/item.dxf')
        if len(self.WorkFlow)>0:
            works=self.WorkFlow
            for work in works:

                if work['WorkClass']=='Taglio Plasma':
                    nodes=work['Nodes']

                    chains=work['Chain']
                    if len(chains)>0:
                        for chain in chains:
                            for geo in chain:

                                if geo[0]=='Line':
                                    drawing.add(dxf.line((nodes[geo[1]]['X'],
                                                          nodes[geo[1]]['Y']),
                                                         (nodes[geo[2]]['X'],
                                                          nodes[geo[2]]['Y'])))
                                    print drawing
                                elif geo[0]=='Arc':
                                    arcgen=geoFun.CircleFrom3Points([nodes[geo[1]]['X'],
                                                                     nodes[geo[1]]['Y']],
                                                                    [nodes[geo[3]]['X'],
                                                                     nodes[geo[3]]['Y']],
                                                                    [nodes[geo[2]]['X'],
                                                                     nodes[geo[2]]['Y']])
                                    #print 'arcgen',arcgen
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
                                    #print 'direction',arcgen['Direction']


                                elif geo[0]=='Circle':
                                    radius=nodes[geo[2]]['X']-nodes[geo[1]]['X']
                                    drawing.add(dxf.circle(radius,(nodes[geo[1]]['X'], nodes[geo[1]]['Y'])))


        drawing.save_to_fileobj(output)
        dxf_result=[output.getvalue()]

        return dxf_result


    def WorkFlowTree(self):
        print 'WorkFlow:'
        for w in self.WorkFlow:
            print '- ',w['WorkClass']


class Job(object):
    def __init__(self):
        self.ID = None
        self.Time = 0


class Work(object):
    def __init__(self,
                 wclass=None,
                 wtitle=None):
        self.ID = None
        self.Title = wtitle
        self.Class = wclass


class WorkPlan(object):
    def __init__(self,
                 ID=None,
                 Title="WP",
                 Class=None):
        self.ID = ID
        self.Title = Title
        self.Class = Class
        self.Machine = None
        self.Items= []
        self.Positions = {}
        self.JobSequence = {}
        self.Times={}

   # def addItem(self,Item=None):
   #     self.add=1


   # def removeItem(self,IdItem=None):
   #     self.remove=1
        # cercare nell'elenco l'item passato ed eliminare


#workset = {} ELIMINARE???
projectLibrary={}
WORKSET = {}
MATERIALS ={}

from Works import *
from Projects import *


def newItemFromProject(projectName,parameters):

    item=projectLibrary[projectName].Execute(parameters)
    jp=jsonpickle.encode(item)
    #print jp

    return item

