from utils.configuration import configuration

class config1(configuration):
    
    def __init__(self,configName):
        super().__init__("config_"+configName+".yaml", configName)
        #initialize default parameters
        super().set_config_entry("imageCount",0)
        super().set_config_entry("maxImageCount",1)
        super().set_config_entry("facesetResolution",256)
        super().set_config_entry("faceType",'wholeface')
        super().set_config_entry("advancedSettings",None)
        
    def tab1_get_imageCount(self):
        return super().get_config_entry('imageCount')
    
    def tab1_get_maxImageCount(self):
        return super().get_config_entry('maxImageCount')
    
    def tab1_get_facesetResolution(self):
        return super().get_config_entry('facesetResolution')
    
    def tab1_get_faceType(self):
        return super().get_config_entry('faceType')
    
    def tab1_get_advancedSettings(self):
        return super().get_config_entry('advancedSettings')
    
    def tab1_set_parameters(self,imageCount=None,maxImageCount=None,facesetResolution=None,faceType=None,advancedSettings=None):
        
        #print(super().get_data())
        if not imageCount is None:
            super().set_config_entry("imageCount",imageCount)
        if not maxImageCount is None:
            super().set_config_entry("maxImageCount",maxImageCount)
        if not facesetResolution is None:
            super().set_config_entry("facesetResolution",facesetResolution)
        if not faceType is None:
            super().set_config_entry("faceType",faceType)
        if not advancedSettings is None:
            super().set_config_entry("advancedSettings",advancedSettings)
        #print(super().get_data())
        
        return 