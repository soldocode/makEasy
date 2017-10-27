# -*- coding: utf-8 -*-
import os
import makEasy
import jsonpickle

path=os.path.dirname(makEasy.__file__)+'\\Materials\\material_quality.json'
f = open(path, 'r')
data=f.read()
f.close()
makEasy.MATERIALS=jsonpickle.decode(data)


