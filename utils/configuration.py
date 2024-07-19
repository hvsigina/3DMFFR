from email.policy import default
import yaml

class configuration:
    
    default_config1 = [
        {
        '%defaultName%': {
        'settingName' : 'settingValue'
                }
        }
    ] 
    
    def __init__(self,configFile,configurationName):
          
        #all settings and options here
        self.configFile = configFile
        self.configurationName = configurationName
        self.data = None
        try:#open existing config file           
            config = open(configFile,"r")
            self.set_data(yaml.load(config, Loader=yaml.FullLoader))
            config.close()
            if self.get_data() is None:
                self.create_config()        
        except:#if config file doesnt exist, then create file with default parameters
            self.create_config()
        
    def set_data(self,data):
        self.data = data
           
    def get_data(self):
        if self.data is None:
            return None
        return self.data

    def create_config(self):
        try:
            config =  open(self.configFile, 'w')
            self.set_data(self.default_config1)
            self.data[0][self.configurationName]=self.data[0]['%defaultName%']
            del self.data[0]['%defaultName%']
            yaml.dump(self.get_data(), config)
            config.close()
            return True
        except:
            return False
            
    def set_config_entry(self,key,value):
        #create or set a config entry
        try:
            config = open(self.configFile,"w")
            data_ = self.get_data()
            data_[0][self.configurationName][key] = value
            self.set_data(data_)
            yaml.dump(self.get_data(), config)
            config.close()
        except:
            return False
        else:
            return True
    
    def get_config_entry(self,key):
        #fetch config entry
        try:
            with open(self.configFile,"r") as config:
                self.set_data(yaml.load(config, Loader=yaml.FullLoader)) 
                
                if key in self.data[0][self.configurationName]:
                    return self.data[0][self.configurationName][key]
                    config.close()
                else:
                    return "Invalid" 
        except:
            config.close()
            return None

#config_tab_1 = configuration("config.yaml","Tab1")
#print("final1 ",config_tab_1.get_data())