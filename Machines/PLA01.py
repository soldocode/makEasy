import makEasy
import types

mac=makEasy.Machines("PLA01","Plasma BBS")

mac.MacProperties= {
    "XMax": 6000,
    "YMax": 2500,
    "HPrices":{"Load":23.00,
               "Tool":20.00,
               "Move":30.00,
               "Work":65.00,
               "Look":20.00,
               "DwLd":23.00}          
  }

mac.Parameters={
        "Load":{
            "DEFAULT":{"CTime":3,"KFactor":1.6,"KW":2}
               },
        "Tool":{
            "DEFAULT": {"CTime": 3,"KW": 2}   
               },
        "Move":{
            "DEFAULT": {"CTime": 0.1,"Speed":8000,"KW": 12}   
               },
        "Work":{
            "DEFAULT":  {"CTime":0.1,"Speed": 2000,"KW":42},
            "S235JR|2": {"Speed": 3000,"KW":16.75},
            "S235JR|3": {"Speed": 2900,"KW":16.75},
            "S235JR|4": {"Speed": 2700,"KW":20.50},
            "S235JR|5": {"Speed": 2500,"KW":20.50},
            "S235JR|6": {"Speed": 2400,"KW":25.75},
            "S235JR|8": {"Speed": 2100,"KW":28.75},
            "S235JR|10": {"Speed": 2000,"KW":30.75},
            "S235JR|12": {"Speed": 2000,"KW":35.75},
            "S235JR|15": {"Speed": 1800,"KW":38.75},
            "S235JR|20": {"Speed": 1050,"KW":40.75},
            "S235JR|25":{"Speed": 750,"KW": 43},
            "S275JR|5": {"Speed": 2700,"KW": 24.5},
            "S275JR|10":{"Speed": 2100,"KW": 31.50}
               },
        "Look":{
            "DEFAULT": {"CTime": 1,"KW": 12}   
               },
        "DwLd":{
            "DEFAULT": {"CTime": 0.15,"KW": 2}   
               }            
            }
        

def getParameters(self,material,thk):
    result={'Material':material,'Thickness':thk}
    id_mat=material+'|'+str(thk)
    for t in makEasy.TTimes:
        result[t]=self.Parameters[t]["DEFAULT"]
        if id_mat in self.Parameters[t]:
            for p in self.Parameters[t][id_mat]:
                result[t][p]=self.Parameters[t][id_mat][p]
            
    return result    
    

mac.getParameters = types.MethodType( getParameters, mac )
makEasy.MACHINES[mac.Id]= mac