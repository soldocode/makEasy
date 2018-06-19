import makEasy
import types

mac=makEasy.Machine("MAC014","Piegatrice 200 Ton - COLGAR")

mac.MacProperties= {
    "XMax": 4000,
    "HPrices":{"Load":24.00,
               "Tool":23.00,
               "Move":23.00,
               "Work":26.00,
               "Look":23.00,
               "DwLd":24.00}          
  }

mac.Parameters={
        "Load":{
            "DEFAULT":{"CTime":3,"KFactor":1.6,"KW":3.5}
               },
        "Tool":{
            "DEFAULT": {"CTime": 3,"KW": 2.5}       
               },
        "Move":{
            "DEFAULT": {"CTime": 0.1,"KW": 13.5}   
               },
        "Work":{
            "DEFAULT":  {"CTime":0.1,"KW":20},
            "S235JR|2": {"KW":10}
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
