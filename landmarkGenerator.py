from retinaface import RetinaFace
import mediapipe as mp
import cv2
import configs.config_landmarks
import pandas as pd
from mediapipe.python import solutions

class mediapipe_landmarks:
    
    def __init__(self,imageName,imageOrPath,detectionThreshold=0.8,debugMode=False,outputPath="./temp/landmarks/"):
        
        self.imageName = imageName
        self.debugMode = debugMode
        self.detectionThreshold = detectionThreshold
        self.resp = None
        self.mpDrawing = solutions.drawing_utils
        self.mpDrawingStyle = solutions.drawing_styles
        self.mpFaceMesh = mp.solutions.face_mesh
        self.drawingSpec = self.mpDrawing.DrawingSpec(thickness=1,circle_radius=1)
        self.imageList = None
        self.imagePath = None
        self.image = None
        self.outputPath = outputPath
        self.imageLandmarks = configs.config_landmarks.config_landmarks(self.imageName)
        self.outputImage = None
        self.results = None
        self.landmarks = None
        self.landmarksYaml = pd.DataFrame()
        self.landmarksScaledYaml = pd.DataFrame()
        self.points = []
        self.pointsScaled = []
        
        if type(imageOrPath) is str:
            self.imagePath = imageOrPath
            self.image = cv2.imread(self.imagePath)
        else:
            self.image = imageOrPath
            
        self.resp = RetinaFace.detect_faces(self.image,threshold=detectionThreshold,)

    def set_landmarks_config(self):
        self.imageLandmarks.land_set_parameters(landmarks=self.landmarksYaml.to_dict(orient='records'),scaledLandmarks=self.landmarksScaledYaml.to_dict(orient='records'),inputImagePath=self.imagePath,outputImagePath=self.outputPath)
    
    def enable_debug_mode(self):
        self.debugMode = True
        
    def disable_debug_mode(self):
        self.debugMode = False
        
    def print_faces(self):
        print("No.of faces in image: ",len(self.resp))
        iter=0
        for face in self.resp:
            iter+=1
            print("Face no:",iter)
            print(face)
    
    def generate_face_mesh(self):
    
        with self.mpFaceMesh.FaceMesh(
            static_image_mode = True,
            min_detection_confidence = self.detectionThreshold) as faceMesh:
            
            #convert from bgr to rgb
            #self.image = self.image[:,:,::-1]
            self.imageList = [self.image]

            for faceNo, img in enumerate(self.imageList):
                
                if self.debugMode:
                    print(faceNo+1)
                self.results = faceMesh.process(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))
        
                if not self.results.multi_face_landmarks:
                    continue
                
                annotated_image = img[:,:,::-1].copy()
                for face_landmarks in self.results.multi_face_landmarks:
                    
                    if self.debugMode:
                        print('face landmarks',face_landmarks)
                    
                    self.mpDrawing.draw_landmarks(
                        image = annotated_image,
                        landmark_list = face_landmarks,
                        connections = self.mpFaceMesh.FACEMESH_TESSELATION,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_tesselation_style()
                    )
                    self.mpDrawing.draw_landmarks(
                        image = annotated_image,
                        landmark_list = face_landmarks,
                        connections = self.mpFaceMesh.FACEMESH_CONTOURS,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_contours_style()
                    )
                    solutions.drawing_utils.draw_landmarks(
                        image=annotated_image,
                        landmark_list=face_landmarks,
                        connections=mp.solutions.face_mesh.FACEMESH_IRISES,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_iris_connections_style()
                    )
                    
                self.landmarks = self.results.multi_face_landmarks[0].landmark
                #print(type(self.results.multi_face_landmarks[0].landmark[0].x))
                #print('face landmarks',self.results.multi_face_landmarks[0].landmark)

                iter = 0
                for face in self.results.multi_face_landmarks:
                    
                    iter+=1
                    for landmark in face.landmark:
                        
                        x = landmark.x
                        y = landmark.y
                        z = landmark.z
                        
                        point = [x,y,z]
                        self.points.append(point)

                        shape = img.shape 
                        relative_x = int(x * shape[1])
                        relative_y = int(y * shape[0])
                        
                        point = [relative_x,relative_y,z]
                        self.pointsScaled.append(point)

                        cv2.circle(img, (relative_x, relative_y), radius=1, color=(225, 0, 0), thickness=1)
                
                self.landmarksYaml = pd.DataFrame(self.points,columns=['x','y','z'])
                self.landmarksScaledYaml = pd.DataFrame(self.pointsScaled,columns=['x','y','z'])
                self.outputImage = img
                cv2.imwrite(self.outputPath + self.imageName +str(iter) + ".jpg",img)
    
testimg = cv2.imread("./output/22_4.jpg")    
test = mediapipe_landmarks(imageName="Florence",imageOrPath="./output/22_4.jpg")
test.generate_face_mesh()
test.set_landmarks_config()
test.print_faces()