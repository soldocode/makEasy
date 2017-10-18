__author__ = 'Riccardo'

import makEasy

def Execute ():
    job = {}

    return job

work=makEasy.Work()
work.Type='drill'
work.Path='wBending'
work.Title='Foratura'
work.Execute=Execute

makEasy.WORKSET[work.Type]= work
