
import makEasy
import types,json
import meTime as mT

LASER_MATERIALS={'S275JR':'Steel',
                 'AISI304':'Stainless Steel',
                 'AISI316':'Stainless Steel',
                 'GEN_ZINC':'Galvanized',
                 'GEN_ALLU':'Aluminium'}

f = open(makEasy.FOLDER+"\\Machines\\MAC099\\MaterialParameters.json", "r")
LASER_PARAMETERS=json.loads(f.read())
f.close()

Machine=makEasy.Machine("MAC099","Laser")


def getTimeParameters(self,work_parameters):
    wt=mT.WorkTime()
    material=work_parameters['sheet_mat']
    thk=work_parameters['sheet_thk']
    #{'Material':material,'Thickness':thk}
    #id_mat=material+'|'+str(thk)
    #print(LASER_PARAMETERS)
    #print(LASER_MATERIALS[material])
    lp=LASER_PARAMETERS[LASER_MATERIALS[material]][str(thk)]
    mp=lp[list(lp.keys())[0]]
    print(mp)
    wt.Load.TimeParameters=mT.TimeParameters(BlockTime=15)
    wt.Tool.TimeParameters=mT.TimeParameters(BlockTime=1)
    wt.Work.TimeParameters=mT.TimeParameters(BlockTime=mp['PiercingTime']/3600,
                                             Speed=mp['Speed'])
    wt.Move.TimeParameters=mT.TimeParameters(BlockTime=0.001,Speed=12000.0)
    wt.Dwld.TimeParameters=mT.TimeParameters(BlockTime=30)
    #result['Speed']=mp['Speed']
    #result['PiercingTime']=mp['PiercingTime']

    #for t in makEasy.TTimes:
    #    result[t]=self.Parameters[t]["DEFAULT"]
    #    if id_mat in self.Parameters[t]:
    #        for p in self.Parameters[t][id_mat]:
    #            result[t][p]=self.Parameters[t][id_mat][p]

    return wt


Machine.getTimeParameters = types.MethodType( getTimeParameters, Machine )
makEasy.MACHINES[Machine.Id]= Machine
