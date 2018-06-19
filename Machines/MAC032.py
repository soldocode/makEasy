import makEasy
import types

mac=makEasy.Machine("MAC032","Impianto Taglio Plasma - BBS")
makEasy.WORKSET['PlasmaCut'].Machines.append(mac)

mac.MacProperties= {
    "XMax": 6000,
    "YMax": 2500,
    "HPrices":{"Load":23.00,
               "Tool":23.00,
               "Move":23.00,
               "Work":40.00,
               "Look":23.00,
               "DwLd":23.00}          
  }

mac.Parameters={
        "Load":{
            "DEFAULT":{"CTime":3,"KFactor":1.6,"KW":3.5}
               },
        "Tool":{
            "DEFAULT": {"CTime": 3,"KW": 2.5}       
               },
        "Move":{
            "DEFAULT": {"CTime": 0.1,"Speed":8000,"KW": 13.5}   
               },
        "Work":{
            "DEFAULT":  {"CTime":0.1,"Speed": 2000,"KW":40},
            "S235JR|2": {"Speed": 3000,"KW":21.75},
            "S235JR|3": {"Speed": 2900,"KW":22.75},
            "S235JR|4": {"Speed": 2700,"KW":22.75},
            "S235JR|5": {"Speed": 2500,"KW":22.75},
            "S235JR|6": {"Speed": 2400,"KW":25.75},
            "S235JR|8": {"Speed": 2100,"KW":28.75},
            "S235JR|10": {"Speed": 2000,"KW":33.55},
            "S235JR|12": {"Speed": 1950,"KW":39.00},
            "S235JR|15": {"Speed": 1800,"KW":42.50},
            "S235JR|20": {"Speed": 1050,"KW":43.75},
            "S235JR|25":{"Speed": 750,"KW": 46.50},
            "S275JR|5": {"Speed": 2700,"KW": 24.5},
            "S275JR|10":{"Speed": 2100,"KW": 31.50}
               },
        "Look":{
            "DEFAULT": {"CTime": 1,"KW": 12}   
               },
        "DwLd":{
            "DEFAULT": {"CTime": 0.15,"KW": 3.5}   
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
