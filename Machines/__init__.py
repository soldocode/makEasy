import os
folder=os.path.dirname(os.path.abspath(__file__))
modules = [dI for dI in os.listdir(folder) if os.path.isdir(os.path.join(folder,dI))]
if '__pycache__' in modules:modules.remove('__pycache__')
#print (modules)
#__all__=['MAC099']
__all__=modules

import makEasy

makEasy.KWH_EURO=0.33
