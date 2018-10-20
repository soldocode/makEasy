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
    #print (machine.Name)
    #print (blocks)
    print (parameters)
   
    material=makEasy.MATERIALS[parameters['Material']]
    kgmm3=material['weight']
    price_material=material['thickness'][str(parameters['Thickness'])]['price']

    total_area=0
    t_load=parameters['Load']['CTime']
    t_move=0
    t_work=0
    t_dwld=2
    weight_blocks=0
    count_blocks=len(blocks)
    

    for b in blocks:
               
        #print(b.Data)
        shape=b.Data['shape']
        l_cut=shape.perimeter['total']
        n_punch=1+len(shape.perimeter['internal'])
        p_weight=shape.area['total']*kgmm3*parameters['Thickness']
        weight_blocks+=p_weight
        total_area+=shape.boundBox.area
        p_load=0.1
        p_move=parameters['Move']['CTime']*n_punch
        p_work=parameters['Work']['CTime']*n_punch
        p_work+=l_cut/parameters['Work']['Speed']
        p_dwld=parameters['DwLd']['CTime']
        p_dwld+=parameters['Load']['KFactor']*math.log(p_weight+1)
        
        print('lunghezza taglio:',l_cut)
        print('numero sfondamenti:',n_punch)
        print('peso',p_weight)
        partial={}

        #print (material)
        #print (parameters['Thickness'])
        material['thickness'][str(parameters['Thickness'])]
        partial['Weight']={'Kg':p_weight,'Price':price_material}
        for t in makEasy.TTimes:
            partial[t]={"Price":machine.MacProperties['HPrices'][t],
                        "KW":parameters[t]['KW'],
                        "Time":0}
        #partial['Load']['Time']=p_load
        t_load+=p_load
        partial['Move']['Time']=p_move
        partial['Work']['Time']=p_work
        #partial['DwLd']['Time']=p_dwld
        t_dwld+=p_dwld
        b.WorkData=partial
        #print ('b:',b.WorkData)
        
        
    num=len(blocks)    
    weight_area=total_area*kgmm3*parameters['Thickness'] 
    t_load+=(parameters['Load']['KFactor']*math.log(weight_area+1))
    print('t_load',t_load)
    t_tool=parameters['Tool']['CTime']/num
    t_look=float(parameters['Look']['CTime'])/num
    t_dwld+=(parameters['Load']['KFactor']*math.log((weight_area-weight_blocks)+1))
    
    for b in blocks:
        print(t_dwld)
        b.WorkData['Load']['Time']=0.1+t_load/weight_blocks*b.WorkData['Weight']['Kg']
        b.WorkData['Tool']['Time']=t_tool/count_blocks
        b.WorkData['Look']['Time']+=t_look/count_blocks
        b.WorkData['DwLd']['Time']=t_dwld/weight_blocks*b.WorkData['Weight']['Kg']
   
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
