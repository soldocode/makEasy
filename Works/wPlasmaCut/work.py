###############################################################################
# PlasmaCut - work.py - 2016
#
# Riccardo Soldini - riccardo.soldini@gmail.com
###############################################################################


import makEasy
import math

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


def getData (machine,blocks,parameters):
    print (machine.Name)
    print (blocks[0].Work)
    print (parameters)
    
    result={}
    for t in makEasy.TTimes:
        result[t]={"Price":machine.MacProperties['HPrices'][t],
                   "KW":parameters[t]['KW']}
        
    
    kgmm3=makEasy.MATERIALS[parameters['Material']]['weight']
    total_area=0
    t_load=parameters['Load']['CTime']
    t_move=0
    t_work=0
    t_dwld=0
    

    for b in blocks:
        print(b.Data)
        shape=b.Data['shape']
        l_cut=shape.perimeter['total']
        n_punch=1+len(shape.perimeter['internal'])
        total_area+=shape.boundBox.area
        t_load+=0.1
        t_move+=parameters['Move']['CTime']*n_punch
        t_work+=parameters['Work']['CTime']*n_punch
        t_work+=l_cut/parameters['Work']['Speed']
        t_dwld+=parameters['DwLd']['CTime']
        
        print('lunghezza taglio:',l_cut)
        print('numero sfondamenti:',n_punch)
        
        
    w=total_area*kgmm3*parameters['Thickness']    
    t_load+=parameters['Load']['KFactor']*math.log(w+1)
    t_tool=parameters['Tool']['CTime']
    t_look=parameters['Look']['CTime']
    t_dwld+=parameters['Load']['KFactor']*math.log(w+1)/2
    

    result['Load']['Time']=t_load
    result['Tool']['Time']=t_tool
    result['Move']['Time']=t_move
    result['Work']['Time']=t_work
    result['Look']['Time']=t_look
    result['DwLd']['Time']=t_dwld
    
   
    return result



work=makEasy.Work('PlasmaCut','Taglio Plasma')
work.Type='taglio_plasma'
work.Folder='wPlasmaCut'
work.Execute=Execute
work.getData=getData

makEasy.WORKSET[work.Type]= work
