
import makEasy
import types,json
import meTime as mT
from pathlib import Path


LASER_MATERIALS={'S275JR':'Steel',
                 'HB400':'Steel',
                 'AISI304':'Stainless Steel',
                 'AISI316':'Stainless Steel',
                 'GEN_ZINC':'Galvanized',
                 'GEN_ALLU':'Aluminium'}

f = open(Path(makEasy.FOLDER+"/Machines/MAC099")/"MaterialParameters.json", "r")
LASER_PARAMETERS=json.loads(f.read())
f.close()

Machine=makEasy.Machine("MAC099","Laser")


def getTimeParameters(self,work_parameters):
    wt=mT.WorkTime()
    material=work_parameters['sheet_mat']
    thk=work_parameters['sheet_thk']
    max_area=3.0*1.5
    pa=work_parameters['total_area']/max_area
    lp=LASER_PARAMETERS[LASER_MATERIALS[material]][str(thk)]
    mp=lp[list(lp.keys())[0]]
    print(mp)
    wt.Load.TimeParameters=mT.TimeParameters(BlockTime=4+thk*pa)
    wt.Tool.TimeParameters=mT.TimeParameters(BlockTime=1)
    wt.Work.TimeParameters=mT.TimeParameters(BlockTime=mp['PiercingTime']/60000,
                                             Speed=mp['Speed'])
    wt.Move.TimeParameters=mT.TimeParameters(BlockTime=0.027,Speed=120000.0)
    wt.Dwld.TimeParameters=mT.TimeParameters(BlockTime=30)
    return wt


def newMacWorkTime(self,work_parameters):
    wt=mT.WorkTime()
    wt.Load.HourlyCost=20.00
    wt.Tool.HourlyCost=20.00
    wt.Move.HourlyCost=60.00
    wt.Work.HourlyCost=90.00
    wt.Look.HourlyCost=20.00
    wt.Dwld.HourlyCost=20.00
    material=work_parameters['sheet_mat']
    thk=work_parameters['sheet_thk']
    max_area=3.0*1.5
    
    #load
    pa=work_parameters['total_area']/max_area
    wt.Load.TimeParameters=mT.TimeParameters(BlockTime=5+(thk/2)*pa)
    print('load',wt.Load.TimeParameters)
    
    #tool
    wt.Tool.TimeParameters=mT.TimeParameters(BlockTime=0.5)
    print('tool',wt.Tool.TimeParameters)
    
    #move
    wt.Move.TimeParameters=mT.TimeParameters(BlockTime=0.027,Speed=120000.0)
    print('move',wt.Move.TimeParameters)
    
    #work
    lp=LASER_PARAMETERS[LASER_MATERIALS[material]][str(thk)]
    mp=lp[list(lp.keys())[0]]
    print(mp)
    wt.Work.TimeParameters=mT.TimeParameters(BlockTime=mp['PiercingTime']/60000,
                                             Speed=mp['Speed'])
    print('work',wt.Work.TimeParameters)

    #look
    wt.Look.TimeParameters=mT.TimeParameters(BlockTime=2)
    print('look',wt.Look.TimeParameters)
    
    #dwld
    wt.Dwld.TimeParameters=mT.TimeParameters(BlockTime=0.3,Speed=1/thk)
    print('dwld',wt.Dwld.TimeParameters)
    
    return wt



Machine.getTimeParameters = types.MethodType( getTimeParameters, Machine )
Machine.newMacWorkTime = types.MethodType( newMacWorkTime, Machine )
makEasy.MACHINES[Machine.Id]= Machine
