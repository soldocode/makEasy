__author__ = 'Riccardo'

import makEasy

def Execute (lunghezza, spessore, diametro):
    job = makEasy.Job()
    #job.Work = work
    #job.Time = lunghezza*spessore*diametro/1000

    return job

work=makEasy.Work()
work.Type='cesoiatura'
work.Execute=Execute

makEasy.workset[work.Type]= work
