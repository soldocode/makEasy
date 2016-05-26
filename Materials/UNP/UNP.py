#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2015-2016                                               *
#*   Riccardo Soldini <riccardo.soldini@gmail.com>                         *
#*                                                                         *
#*   last update: 18/04/16                                                 *
#***************************************************************************


import json
from dxfwrite import DXFEngine as dxf
import math
import tkFileDialog
import geoFunNew as geo
import meDXF



param={"30":
	{"nodes":
         [[-16.5,0],[-16.5,15.0],[16.5,15.0],[16.5,12.55],[15.57,10.18],[13.28,9.06],[-5.06,7.60],[-9.64,5.37],[-11.50,0.62],[-11.50,0]]	
        },
       "160":
	{"nodes":
	 [[-32.5,0],[-32.5,80.0],[32.5,80.0],[32.5,77.18],[31.04,73.45],[27.44,71.70],[-15.34,68.27],[-22.21,64.93],[-25.0,57.81],[-25.0,0]]	
        }
       }
path=[["line",17,1],
      ["line",1,2],
      ["line",2,3],
      ["arc",3,5,4],
      ["line",5,6],
      ["arc",6,8,7],
      ["line",8,10],
      ["arc",10,12,11],
      ["line",12,13],
      ["arc",13,15,14],
      ["line",15,16],
      ["line",16,17]]


file= tkFileDialog.asksaveasfilename(filetypes= [('DXF files', '.DXF')],
                                     title='Salva DXF',
                                     defaultextension = '.DXF')

drawing = dxf.drawing(file)
x=0

for u in param:
    print u
    nodes=param[u]["nodes"]
    ccwnodes=list(nodes)
    ccwnodes.reverse()
    
    for i in range(1,9):
        nodes.append([ccwnodes[i][0],ccwnodes[i][1]*-1])
    print nodes    

    p={'path':path,                                        
       'nodes':nodes,                                    
       'drawing':drawing,
       'position':[x,0]}

    meDXF.Draw(p)
    x+=150


drawing.save()
