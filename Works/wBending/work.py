__author__ = 'Riccardo'

import makEasy

def Execute ():
    job = makEasy.Job()

    return job

work=makEasy.Work()
work.Type='piegatura'
work.Path='wBending'
work.Title='Piegatura'
work.Execute=Execute

makEasy.WORKSET[work.Type]= work
