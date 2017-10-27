import makEasy
import types

mac=makEasy.Machines("PLA01","Plasma BBS")

mac.MacProperties= {
    "XMax": 6000,
    "YMax": 2500,
    "HPrices":{"Load":20.00,
               "Tool":20.00,
               "Move":5.00,
               "Work":10.00,
               "Look":5.00,
               "DwLd":5.00}          
  }

  
mac.TimeParameters={
    "TCLoad": {
      "DEFAULT": {"Time": 3,"KW": 2}
    },
    "TPLoad": {
      "DEFAULT": {"Ln":1.6,"KW": 2}
    },
    "TCTool": {
      "DEFAULT": {"Time": 3,"KW": 2}
    },
    "TPTool": {
      "DEFAULT": {"Speed": 30,"KW": 2}
    },
    "TCMove": {
      "DEFAULT": {"Time": 0.1,"KW": 2}
    },
    "TPMove": {
      "DEFAULT": {"Speed": 30,"KW": 2}
    },
    "TCWork": {
      "DEFAULT": {"Time": 0.1,"KW": 2}
    },
    "TPWork": {
      "DEFAULT":   {"Speed": 2000,"KW": 40},
      "S235JR|2":  {"Speed": 2500,"KW": 16.75},
      "S235JR|25": {"Speed": 750,"KW": 42},
      "S275JR|5":  {"Speed": 2700,"KW": 24.5},
      "S275JR|10": {"Speed": 2100,"KW": 31.50}
    },
    "TCLook": {
      "DEFAULT": {"Time": 30,"KW": 2}
    },
    "TPLook": {
      "DEFAULT": {"Speed": 30,"KW": 2}
    },
    "TCDwLd": {
      "DEFAULT": {"Time": 30,"KW": 2}
    },
    "TPDwLd": {
      "DEFAULT": {"Speed": 30,"KW": 2}
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