__author__ = 'Riccardo'

import makEasy

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
        
    for i in paths
      tWork+=0.5
    
    
    res={"time":tLoad+tTool+tWork+tMove+tLook}
    return res

    
def Run (args):
    block={"WorkClass":"PlasmaCut",
           "Id":'',
           "Nodes":args['nodes'],
           "Chain":args['paths']}
    ### calcolo area ###
    ### calcolo bound box ###
    ### calcolo perimetro ###
    ### calcolo inneschi ###
    ### calcolo peso ###
    ### calcolo tempo ###

    return block



work=makEasy.Work()
work.Type='taglio_plasma'
work.Class='PlasmaCut'
work.Title='Taglio Plasma'
work.Path='wPlasmaCut'
work.Execute=Execute
work.Run=Run

makEasy.WORKSET[work.Type]= work
