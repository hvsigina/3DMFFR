import cv2
import numpy as np
import insightface
import utils.bounding_intersection as inter
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image
from insightface.utils import face_align

np.int = np.int32
mouth_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

def rotate_image(image2, angle):
  image=image2.copy()
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

def left_right_eye(eye_1,eye_2):
    if eye_1[0] < eye_2[0]: 
        left_eye = eye_1 
        right_eye = eye_2 
        flag = True
    else: 
        left_eye = eye_2 
        right_eye = eye_1 
        flag = False
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
    
    return [left_eye_x,left_eye_y,right_eye_x,right_eye_y,flag]

def determine_face_tilt(image2):
    
    image=image2.copy()
        
    grey = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    angle = 0
   
    index = 0
    indexm = 0
    eye_1 = [None, None, None, None]
    eye_2 = [None, None, None, None]
    mouth_1 = [None, None, None, None]
    
    eye_cascade_scalefactor = 1.3
    eye_cascade_scalefactor_scale = 0.01
    
    iter = 0
    while (eye_1[0] is None) or (eye_2[0] is None) and (eye_cascade_scalefactor-(iter*eye_cascade_scalefactor_scale)>1):
        #keep trying to find eyes with different scalefactors
        eyes = eye_cascade.detectMultiScale(grey, eye_cascade_scalefactor-(iter*eye_cascade_scalefactor_scale), 6) 

        iter += 1
        h,w,_ = image.shape
        x = 0
        y = 0

        for (ex, ey, ew, eh) in eyes: 
            if index == 0: 
                eye_1 = [ex, ey, ew, eh]

            else: 
                eye_2 = [ex, ey, ew, eh]
                #check if both detected eyes are different
                if eye_2[0] != None:
                    if inter.boxIntersect(eye_1[0],eye_1[1],eye_1[2],eye_1[3],eye_2[0],eye_2[1],eye_2[2],eye_2[3]):
                        eye_2 = [None, None, None, None]
             
            index = index + 1
            if eye_2[0] is not None:
                cv2.rectangle(image[y:(y + h), x:(x + w)], (ex, ey), 
                        (ex + ew, ey + eh), (0, 0, 255), 2)
                break
   
    
    if eye_1[0]==None or eye_2[0]==None:
        return 0
    
    #now find mouth
    iter2 = 0
    neigh = 11
    while (mouth_1[0] is None):
        scale_f = ((eye_cascade_scalefactor-(iter2*eye_cascade_scalefactor_scale))+0.1)
        if scale_f <=1:
            break
        mouths = mouth_cascade.detectMultiScale(grey, scale_f, neigh) 
        iter2 += 1
        for (mx, my, mw, mh) in mouths:
            if indexm == 0:
                mouth_1 = [mx, my, mw, mh]
                        
                indexm += 1
                if inter.boxIntersect(eye_1[0],eye_1[1],eye_1[2],eye_1[3],mx,my,mw,mh) or inter.boxIntersect(eye_2[0],eye_2[1],eye_2[2],eye_2[3],mx,my,mw,mh):
                    mouth_1 = [None, None, None, None]
                elif not (ew<=mw<=(3*mw)):
                    mouth_1 = [None, None, None, None]
                elif not (eh<=mh<=(2*mh)):
                    mouth_1 = [None, None, None, None]
     
    #print("mouth_1",mouth_1)
    
    #if mouth is not found, slope calculated with eyes data
    if mouth_1==[None,None,None,None]:
        
        if (eye_1[0] is not None) and (eye_2[0] is not None):
            left_eye_x,left_eye_y,right_eye_x,right_eye_y,eye_flag = left_right_eye(eye_1,eye_2)
            delta_x = right_eye_x - left_eye_x 
            delta_y = right_eye_y - left_eye_y
            
            if delta_x == 0:
                #cv2.imwrite("./output/"+str(i)+"_"+str(selected)+"_detected.jpg",image)
                return 0
            elif delta_y == 0:
                #cv2.imwrite("./output/"+str(i)+"_"+str(selected)+"_detected.jpg",image)
                return -90
        
            # Slope of line formula 
            angle = np.arctan(delta_y / delta_x)   
          
            # Converting radians to degrees 
            angle = (angle * 180) / np.pi
        else:
            #cv2.imwrite("./output/"+str(i)+"_"+str(selected)+"_detected.jpg",image)
            return 0
            
    else :    
        cv2.rectangle(image[y:(y + h), x:(x + w)], (mouth_1[0], mouth_1[1]), 
                                    (mouth_1[0] + mouth_1[2], mouth_1[1] + mouth_1[3]), (0, 255, 0), 2)
        left_eye_x,left_eye_y,right_eye_x,right_eye_y,eye_flag = left_right_eye(eye_1,eye_2)
  
        delta_x = right_eye_x - left_eye_x 
        delta_y = right_eye_y - left_eye_y 
        
        mideye_x = left_eye_x + (delta_x/2)
        mideye_y = left_eye_y + (delta_y/2)
        
        midmouth_x = mouth_1[0] + (mouth_1[2]/2)
        midmouth_y = mouth_1[1] + (mouth_1[3]/2)
        
        delta_eye_mouth_x = 0
        delta_eye_mouth_y = 0
        
        if mideye_x>midmouth_x :
            delta_eye_mouth_x = mideye_x-midmouth_x
        else:
            delta_eye_mouth_x = midmouth_x-mideye_x
        
        if mideye_y>midmouth_y :
            delta_eye_mouth_y = mideye_y-midmouth_y
        else:
            delta_eye_mouth_y = midmouth_y-mideye_y
        
        #print("mideye_x,mideye_y",mideye_x,mideye_y)
        #print("midmouth_x,midmouth_y",midmouth_x,midmouth_y)
        #print("delta_eye_mouth_x",delta_eye_mouth_x)
        #print("delta_eye_mouth_y",delta_eye_mouth_y)
        
        if delta_eye_mouth_x == 0:
            #cv2.imwrite("./output/"+str(i)+"_"+str(selected)+"_detected.jpg",image)
            return -90
        elif delta_eye_mouth_y == 0:
            #cv2.imwrite("./output/"+str(i)+"_"+str(selected)+"_detected.jpg",image)
            return 0
        
        # Slope of line formula 
        angle = np.arctan(delta_eye_mouth_x / delta_eye_mouth_y)   
          
        # Converting radians to degrees 
        angle = (angle * 180) / np.pi
    #cv2.imwrite("./output/"+str(i)+"_"+str(selected)+"_detected.jpg",image)
    
    return angle

def faceset_create(img2,selected,iter):
    rotated_imgs = []
    temp_list = []
    mode_str = ["face","wholeface","head"]
    mode_value = [4] #0,2,4

    #selected = mode_value[0]
    img_name = img2[0].split("\\")[-1]
    img = cv2.imread(img2[0])
    finall = img.copy()
    app = FaceAnalysis(providers=['CPUExecutionProvider'])
    app.prepare(ctx_id=0, det_size=(640, 640))
    #img = ins_get_image('t1')
    faces = app.get(img)

    i=0
    for face in faces:
    
        i+=1
        imgHeight,imgWidth,_ = img.shape
        bbox = face.bbox.astype(int)
    
    #[minx,miny,maxx,maxy]
    #bounding box adjust for rotation
        bbox[0]-=int((bbox[0]*selected)/100)
        bbox[1]-=int((bbox[1]*selected)/100)
        bbox[2]+=int((bbox[2]*selected)/100)
        bbox[3]+=int((bbox[3]*selected)/100)
    
        '''
        if bbox[1]<0:
            bbox[1]=0
        
        if bbox[3]>imgWidth:
            bbox[3]=imgWidth
        
        if bbox[0]<0:
            bbox[0]=0
        
        if bbox[2]>imgHeight:
            bbox[2]=imgHeight
        '''        
        #face_images.append(img[bbox[1]:bbox[3],bbox[0]:bbox[2]])
        angle = determine_face_tilt(img[bbox[1]:bbox[3],bbox[0]:bbox[2]])
        #print("angle=",angle)
        rotated = rotate_image(finall[bbox[1]:bbox[3],bbox[0]:bbox[2]],angle)
        temp_img_path = "./output/"+str(iter)+str(i)+"_"+str(selected)+".jpg"
        temp_list.append(temp_img_path)
        rotated_imgs.append(rotated)
        #print(rotated_imgs[i-1])
        #print(rotated_imgs[i-1].shape)
        cv2.imwrite(temp_img_path,rotated)    
    
    return [temp_list,rotated_imgs]
    #cv2.imwrite("./output/"+str(i)+"_"+str(selected)+"_afterDetermine.jpg",img[bbox[1]:bbox[3],bbox[0]:bbox[2]])

    #cv2.imwrite("./output/"+str(i)+"_"+str(selected)+"_output.jpg",rotate_image(img[bbox[1]:bbox[3],bbox[0]:bbox[2]],angle)
   