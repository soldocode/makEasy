#***************************************************************************
#*                                                                         *
#*   Project BEND SHEET                                                    *
#*   2017                                                                  *
#*   Riccardo Soldini <riccardo.soldini@gmail.com>                         *
#*                                                                         *
#* PARAMETERS:                                                             *
#*                                                                         *
#*                                                                         *
#*                                                                         *
#*                                                                         *
#*                                                                         *
#***************************************************************************

__author__ = 'Riccardo'

import makEasy

projectName='Lamiera Piegata'
projectPath='pBendSheet'
project=makEasy.Project(name=projectName,path=projectPath)


makEasy.projectLibrary[project.Name]= project