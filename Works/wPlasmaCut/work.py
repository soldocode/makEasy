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

    for i in paths:
      tWork+=0.5


    res={"time":tLoad+tTool+tWork+tMove+tLook}
    return res


def Run (machine,blocks):
    print (machine)
    print (blocks[0].Work)
    
    for b in blocks:
        print (b.Data)
    times=0
    ### calcolo area ###
    ### calcolo bound box ###
    ### calcolo perimetro ###
    ### calcolo inneschi ###
    ### calcolo peso ###
    ### calcolo tempo ###

    return times



work=makEasy.Work('PlasmaCut','Taglio Plasma')
work.Type='taglio_plasma'
#work.Path='wPlasmaCut'
work.Folder='wPlasmaCut'
work.Execute=Execute
work.Run=Run

makEasy.WORKSET[work.Type]= work
