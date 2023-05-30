import cv2
import cvlib as cvl
import time as t
import numpy as np
import pytz
from datetime import datetime as dt
from rest_framework.response import Response
from keras.models import load_model
from keras_preprocessing.image import img_to_array
from datetime import date
from rest_framework.views import APIView
from ads_display import models
class StartEnd(APIView):
    def get(self,request,**kwargs):
        if kwargs:
            if kwargs['status'] == "Yes":
                class Humans:
                    def __init__(self,gender,total_humans):
                        self.gender_model=gender
                        self.total_present_humans=total_humans
                        self.Males=[]
                        self.Females=[]
                        self.count=0
                        self.total_present=[]
                        self.FemaleCounter=0
                        self.MaleCounter=0
                        self.counteHumans=0
                        self.conf_threshold=0.4
                        self.NMS_threshold=0.4
                        self.label=" "
                        self.MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
                        
                    
                    # predictions
                    def  watch_ad(self):
                        timezone=pytz.timezone("Asia/Karachi")
                        now=dt.now(timezone)
                        s = now.strftime("%I:%M:%S")
                        print("Start",s)
                        s2=int(t.time())
                        s3=s2+30
                        s4=s2+60
                        
                        capture=cv2.VideoCapture(0)
                        
                        while capture.isOpened():
                            ret,frame=capture.read()
                            face,confidence=cvl.detect_face(frame)
                            classes,scores,boxes=self.total_present_humans.detect(
                                                    frame,self.conf_threshold,self.NMS_threshold)
                            print("After humans")
                            for i,f in enumerate(face):
                            
                                (startX,startY)=f[0],f[1]
                                (endX,endY)=f[2],f[3]
                                face_crop=np.copy(frame[startY:endY,startX:endY])
                                if (face_crop.shape[0]) <10 or (face_crop.shape[1]) <10:
                                    continue
                                
                                face_crop=cv2.cvtColor(face_crop,cv2.COLOR_BGR2GRAY)
                                face_crop=cv2.resize(face_crop,(150,150))
                                face_crop = np.array(face_crop)
                                #add new dimension
                                face_crop = np.expand_dims(face_crop, axis=0)
                                #convert to 1 channel
                                face_crop = np.expand_dims(face_crop, axis=-1)
                                face_crop=face_crop.astype("float")/255.0
                                #Human prediction
                                result=gender_model.predict(face_crop)
                                print("After gender")
                                prediction=np.argmax(result)
                                
                                
                                if prediction==0:
                                    self.FemaleCounter+=1
                                    female_acc=result[0][0]
                                    female_acc=str(female_acc).split('.')[1]
                                    self.label=f"Female {female_acc[0:2]}%"
                                else:
                                    self.MaleCounter+=1
                                    male_acc=result[0][1]
                                    male_acc=str(male_acc).split('.')[1]
                                    self.label=f"Male {male_acc[0:2]}%"
                                        
                            for cla,accuracy,index in zip(classes,scores,boxes):
                                if cla==0:
                                    self.counteHumans+=1
                                    self.count+=1
                                    accuracy=str(accuracy).split('.')[1]
                                    accuracy=accuracy[0:2]
                                    self.human=f"Human({self.count}) {accuracy}%"
                                    cv2.rectangle(frame, index, (0,255,0),2)
                                    cv2.putText(frame,self.human,(index[0]+10,index[1]+40),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)
                                    cv2.putText(frame,self.label,(index[0]+10,index[1]+60),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)
                                self.count=0
                            self.Males.append(self.MaleCounter)
                            self.Females.append(self.FemaleCounter)
                            self.total_present.append(self.counteHumans)
                            self.counteHumans=0
                            self.MaleCounter=0
                            self.FemaleCounter=0
                            
                            s2_get=int(t.time())
                            if s3<=s2_get:
                                maximum_males=max(self.Males)
                                maximum_Females=max(self.Females)
                                print(self.Males)
                                print(self.Females)
                                
                                Total_humans=maximum_males+maximum_Females
                                print(s,maximum_Females,maximum_males,Total_humans)
                                models.humans.objects.create(Time=s,Date=str(date.today()),Total_Females=maximum_Females,Total_Males=maximum_males,Total_attracted_humans=Total_humans,Total_present_humans=max(self.total_present))
                                timezone=pytz.timezone("Asia/Karachi")
                                
                                now=dt.now(timezone)
                                s = now.strftime("%I:%M:%S")
                                s2=int(t.time())
                                s3=s2+30
                            # cv2.imshow('Video', frame)
                            
                            
                            if (cv2.waitKey(15) & 0xff == ord('q')) or (s4<=int(t.time())):
                                break
                            # if s4<=int(t.time()):
                            #     break
                            else:
                              cv2.imshow('Video', frame)
                                
                                
                        capture.release()
                        cv2.destroyAllWindows()
                    


                def object_detect():
                    frozen_model="ads_display/yolov4-tiny.weights"
                    config_file="ads_display/yolov4-tiny.cfg"
                    net=cv2.dnn.readNet(frozen_model,config_file)
                    model=cv2.dnn_DetectionModel(net)
                    model.setInputParams(size=(416,416),scale=1/255,swapRB=True)
                    return model
             

                present_humans_model=object_detect() 
                gender_model=load_model("ads_display/male_female_model.h5")
                
                adv_obj=Humans(gender_model,present_humans_model)
                adv_obj.watch_ad()
        
                return Response({"status":"ok"})
            return Response({"status":"Bad Request"})
        