###############################################################################
# PlasmaCut - work.py - 2016
#
# Riccardo Soldini - riccardo.soldini@gmail.com
###############################################################################


import makEasy
import math,g2
from dxfwrite import DXFEngine as dxf


def Execute (lunghezza, spessore, diametro):
    job = makEasy.Job()
    #job.Work = work
    #job.Time = lunghezza*spessore*diametro/1000

    return job



def WorkOut(args):
    nodes=args['nodes']
    paths=args['paths']
    speed=args['speed']

    tLoad=5
    tTool=5
    tWork=1
    tMove=1
    tLook=2

    for i in paths:
      tWork+=0.5


    res={"time":tLoad+tTool+tWork+tMove+tLook}
    return res


#def getData (machine,blocks,parameters):
def updateWorkData (machine,blocks,parameters):
    print (machine.Name)
    print (blocks)
    print (parameters)
   
    kgmm3=makEasy.MATERIALS[parameters['Material']]['weight']
    total_area=0
    t_load=parameters['Load']['CTime']
    t_move=0
    t_work=0
    t_dwld=0
    weight_blocks=0
    

    for b in blocks:
               
        print(b.Data)
        shape=b.Data['shape']
        l_cut=shape.perimeter['total']
        n_punch=1+len(shape.perimeter['internal'])
        p_w=shape.area['total']*kgmm3*parameters['Thickness']
        weight_blocks+=p_w
        total_area+=shape.boundBox.area
        p_load=0.1
        p_move=parameters['Move']['CTime']*n_punch
        p_work=parameters['Work']['CTime']*n_punch
        p_work+=l_cut/parameters['Work']['Speed']
        p_dwld=parameters['DwLd']['CTime']
        p_dwld+=parameters['Load']['KFactor']*math.log(p_w+1)
        
        print('lunghezza taglio:',l_cut)
        print('numero sfondamenti:',n_punch)
        partial={}
        partial['Weight']=p_w
        for t in makEasy.TTimes:
            partial[t]={"Price":machine.MacProperties['HPrices'][t],
                        "KW":parameters[t]['KW'],
                        "Time":0}
        partial['Load']['Time']=p_load
        partial['Move']['Time']=p_move
        partial['Work']['Time']=p_work
        partial['DwLd']['Time']=p_dwld
        b.WorkData=partial
        print ('b:',b.WorkData)
        
        
    num=len(blocks)    
    w=total_area*kgmm3*parameters['Thickness']    
    t_load+=(parameters['Load']['KFactor']*math.log(w+1))
    t_tool=parameters['Tool']['CTime']/num
    t_look=parameters['Look']['CTime']/num
    t_dwld+=(parameters['Load']['KFactor']*math.log((w-weight_blocks)+1))
    
    for b in blocks:
        b.WorkData['Load']['Time']+=t_load/weight_blocks*b.WorkData['Weight']
        b.WorkData['Tool']['Time']+=t_tool
        b.WorkData['Look']['Time']+=t_look
        b.WorkData['DwLd']['Time']+=t_dwld/weight_blocks*b.WorkData['Weight']
   
    return


def getDXF (data):
    dwg=g2.Drawing()
    dwg.insertGeo('work',data['shape'])
    print(dwg.boundBox)
    dxf_result=dwg.getDXF()
    return dxf_result
    

work=makEasy.Work('PlasmaCut','Taglio Plasma')
work.Folder='wPlasmaCut'
work.Execute=Execute
#work.getData=getData
work.updateWorkData=updateWorkData
work.getDXF=getDXF

makEasy.WORKSET[work.Class]= work
