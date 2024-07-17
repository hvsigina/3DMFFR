import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image
from insightface.utils import face_align

np.int = np.int32
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

def rotate_image(image2, angle):
  image=image2.copy()
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

def determine_face_tilt(image2):
    
    image=image2.copy()
    cv2.imwrite("./output/"+str(i)+"_"+str(selected)+"_beforeRotation.jpg",rotated)    

    grey = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    angle = 0
    
    faces = face_cascade.detectMultiScale(grey,1.1,5)
    x, y, w, h = 0, 0, 0, 0
    
    for (x, y, w, h) in faces: 
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2) 
        cv2.circle(image, (x + int(w * 0.5), y +
                          int(h * 0.5)), 4, (0, 255, 0), -1) 
    eyes = eye_cascade.detectMultiScale(grey[y:(y + h), x:(x + w)], 1.1, 4) 
    index = 0
    eye_1 = [None, None, None, None]
    eye_2 = [None, None, None, None]
    
    for (ex, ey, ew, eh) in eyes: 
        if index == 0: 
            eye_1 = [ex, ey, ew, eh] 
        elif index == 1: 
            eye_2 = [ex, ey, ew, eh] 
        cv2.rectangle(image[y:(y + h), x:(x + w)], (ex, ey), 
                     (ex + ew, ey + eh), (0, 0, 255), 2) 
        index = index + 1
        
    if (eye_1[0] is not None) and (eye_2[0] is not None): 
        if eye_1[0] < eye_2[0]: 
            left_eye = eye_1 
            right_eye = eye_2 
        else: 
            left_eye = eye_2 
            right_eye = eye_1 
        left_eye_center = ( 
            int(left_eye[0] + (left_eye[2] / 2)),  
          int(left_eye[1] + (left_eye[3] / 2))) 
          
        right_eye_center = ( 
            int(right_eye[0] + (right_eye[2] / 2)), 
          int(right_eye[1] + (right_eye[3] / 2))) 
          
        left_eye_x = left_eye_center[0] 
        left_eye_y = left_eye_center[1] 
        right_eye_x = right_eye_center[0] 
        right_eye_y = right_eye_center[1] 
  
        delta_x = right_eye_x - left_eye_x 
        delta_y = right_eye_y - left_eye_y 
        
        print(delta_x)
        print(delta_y)
          
        # Slope of line formula 
        angle = np.arctan(delta_y / delta_x)   
          
        # Converting radians to degrees 
        angle = (angle * 180) / np.pi
    
    return angle

mode_str = ["face","wholeface","head"]
mode_value = [4] #0,2,4

selected = mode_value[0]

app = FaceAnalysis(providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(640, 640))
img = ins_get_image('t1')
faces = app.get(img)

i=0
for face in faces:
    
    i+=1
    imgHeight,imgWidth,_ = img.shape
    bbox = face.bbox.astype(int)
    
    #bounding box adjust for rotation
    #bbox[1]-=int((bbox[1]*selected)/100)
    #bbox[3]+=int((bbox[3]*selected)/100)
    #bbox[0]-=int((bbox[0]*selected)/100)
    #bbox[2]+=int((bbox[2]*selected)/100)
    
    #if bbox[1]<0:
        #bbox[1]=0
        
    #if bbox[3]>imgWidth:
        #bbox[3]=imgWidth
        
    #if bbox[0]<0:
     #   bbox[0]=0
        
    #if bbox[2]>imgHeight:
     #   bbox[2]=imgHeight
            
    #face_images.append(img[bbox[1]:bbox[3],bbox[0]:bbox[2]])
    angle = determine_face_tilt(img[bbox[1]:bbox[3],bbox[0]:bbox[2]])
    print(angle)
    rotated = rotate_image(img[bbox[1]:bbox[3],bbox[0]:bbox[2]],angle)
    cv2.imwrite("./output/"+str(i)+"_"+str(selected)+"_beforeRotation.jpg",rotated)    
    
    #cv2.imwrite("./output/"+str(i)+"_"+str(selected)+"_afterDetermine.jpg",img[bbox[1]:bbox[3],bbox[0]:bbox[2]])

    #cv2.imwrite("./output/"+str(i)+"_"+str(selected)+"_output.jpg",rotate_image(img[bbox[1]:bbox[3],bbox[0]:bbox[2]],angle)
    