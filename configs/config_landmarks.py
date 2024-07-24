from configs.configuration import configuration

class config_landmarks(configuration):
    
    def __init__(self,configName):
        super().__init__("./landmarks/landmarks_"+configName+".yaml", configName)
        #initialize default parameters
        super().set_config_entry("landmarkType","mediapipe")
        super().set_config_entry("inputImagePath","")
        super().set_config_entry("output_image_path","")
        super().set_config_entry("landmarks",None)
        super().set_config_entry("scaledLandmarks",None)
        
    def land_get_landmarkType(self):
        return super().get_config_entry('landmarkType')
    
    def land_get_landmarks(self):
        return super().get_config_entry('landmarks')
    
    def land_get_scaledLandmarks(self):
        return super().get_config_entry('scaledLandmarks')
    
    def land_get_inputImagePath(self):
        return super().get_config_entry('inputImagePath')
    
    def land_get_outputImagePath(self):
        return super().get_config_entry('outputImagePath')
    
    def land_set_parameters(self,landmarkType="",landmarks=None,scaledLandmarks=None,inputImage=None,outputImage=None,inputImagePath="",outputImagePath=""):
        
        if not landmarkType is None:
            super().set_config_entry("landmarkType",landmarkType)
            
        if not inputImagePath is "":
            super().set_config_entry("inputImagePath",inputImagePath)
            
        if not outputImagePath is "":
            super().set_config_entry("outputImagePath",outputImagePath)
            
        if not landmarks is None:
            super().set_config_entry("landmarks",landmarks)
            
        if not scaledLandmarks is None:
            super().set_config_entry("scaledLandmarks",scaledLandmarks)        