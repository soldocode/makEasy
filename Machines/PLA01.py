import makEasy
import types

mac=makEasy.Machines("PLA01","Plasma BBS")

mac.MacProperties= {
    "XMax": 6000,
    "YMax": 2500
  }

mac.TimeParameters={
    "TCLoad": {
      "DEFAULT": 5
    },
    "TPLoad": {
      "DEFAULT": 10
    },
    "TCTool": {
      "DEFAULT": 1
    },
    "TPTool": {
      "DEFAULT": 10
    },
    "TCMove": {
      "DEFAULT": 1
    },
    "TPMove": {
      "DEFAULT": 10
    },
    "TCWork": {
      "DEFAULT": 1
    },
    "TPWork": {
      "DEFAULT":   {"Speed": 2000,"KW": 40},
      "S235JR|2":  {"Speed": 2500,"KW": 16.75},
      "S235JR|25": {"Speed": 750,"KW": 42},
      "S275JR|5":  {"Speed": 2700,"KW": 24.5},
      "S275JR|10": {"Speed": 2100,"KW": 31.50}
    },
    "TCLook": {
      "DEFAULT": 2
    },
    "TPLook": {
      "DEFAULT": 2
    },
    "TCDwLd": {
      "DEFAULT": 2
    },
    "TPDwLd": {
      "DEFAULT": 2
   }        
  }

      
def getParameters(self,id_mat):
    result={}
    for t in makEasy.TTimes:
       if id_mat in self.TimeParameters[t]:
           result[t]=self.TimeParameters[t][id_mat]
       else:
           result[t]=self.TimeParameters[t]["DEFAULT"]  
    return result


mac.getParameters = types.MethodType( getParameters, mac )
makEasy.MACHINES[mac.Id]= mac