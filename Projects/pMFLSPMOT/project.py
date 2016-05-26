#***************************************************************************
#*                                                                         *
#*   Project MFL- Supporti Motore                                          *
#*   Copyright (c) 2016                                                    *
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



projectName='MFL-Supporti Motore'
projectPath='pMFLSPMOT'
project=makEasy.Project(name=projectName,path=projectPath)


def ValidateParameters(self,parameters):

    return True


def Execute(self,prm):
    self.ProjectExecuted=True
    ValidateParameters(self,prm)
    print prm

    #### sviluppo dei parametri ####
    rdn=math.radians(prm["inclinazione"])
    hp=prm["h_piano_piastre"]-prm["h_tubo_aria"]-prm["sp_piatto_gambe"]
    hp+=prm["dis_centro_piastra"]*math.sin(rdn)+prm["sp_piastra"]*math.cos(rdn)
    print "altezza centro piastra:",hp

    dfu=prm["dis_piastra-blocco_mot"]+prm["sp_piatto_mot"]+prm["sp_supporto"]
    print "differenza utile piastra-supporto:",dfu

    pr=dfu*math.cos(rdn)
    h=hp-pr
    print "altezza di riferimento:",h

    spo=prm["nerv_sotto_piatto"]
    spo+=(prm["interasse_blocco_mot"]/2-prm["larg_piatto_mot"]/2-prm["dist_all_piatto"])*math.cos(rdn)
    print "spostamento orizzontale:",spo

    spv=spo*math.tan(rdn)

    sv=prm["nerv_sotto_piatto"]/math.cos(rdn)+h-2
    svsb=sv-spv
    svsa=sv+spv
    print "SV supp basso:",svsb
    print "SV supp alto:",svsa
     

    #### calcola la sequenza di lavorazione ###
    work_flow=''

    item=makEasy.Item()
    item.Class="assembly"
    item.ClassProperty={"Material":"Fe"}
    item.Project=makEasy.projectLibrary[projectName]
    item.ProjectParameters=prm
    item.WorkFlow=work_flow
    return item



def ExportDXF(self,param):
    output = cStringIO.StringIO()
    drawing = dxf.drawing('MFLSPMOT.dxf')

    cx=0
    cy=0
    cutid=1
    
    nf=[]
    nt=[]
    nl=[]


    #misure utili
   

    #Vista in Pianta
    

    
    # Vista di Fronte
    



    # Vista Laterale

    

    drawing.save_to_fileobj(output)
    dxf_result=[output.getvalue()]
    return dxf_result


project.ValidateParameters   = types.MethodType( ValidateParameters, project )
project.Execute = types.MethodType( Execute, project )
project.ExportDXF = types.MethodType( ExportDXF, project )
makEasy.projectLibrary[project.Name]= project
