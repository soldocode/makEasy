__author__ = 'Riccardo Soldini'

import makEasy

def WorkOut(args):
    cLen=0
    cWeight=0
    if args["length"]:cLen=args["length"]
    if args["weight"]:cWeight=args["weight"]

    tLoad=5+5
    tTool=5+0
    tWork=1+cLen/80
    tMove=5+cWeight/20
    tLook=5+cWeight/200
    
    res={"time":tLoad+tTool+tWork+tMove+tLook}
    return res

def Execute ():
    job = makEasy.Job()

    return job

work=makEasy.Work()
work.Type='calandratura'
work.Path='wPlateRolls'
work.Title='Calandratura'
work.Execute=Execute
work.WorkOut=WorkOut

makEasy.WORKSET[work.Type]= work
