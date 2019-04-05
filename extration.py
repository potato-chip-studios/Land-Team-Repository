import pandas as pd
import os.path
from image_features_extraction import MyException
import cv2

class Features(object):
  
    def __init__(self, data_frame):
        self.__data_frame = data_frame
        self.__class_name = ''
        self.__class_value=None


    def set_class_name(self, class_name):
        self.__class_name = class_name


    def set_class_value(self, class_value):
        self.__class_value = class_value


    def get_class_name(self):
        return self.__class_name


    def get_class_value(self):
        return self.__class_value


    def merge(self, Features_Obj, how_in='inner'):
       
        df1 = Features_Obj.get_dataframe();
        df2 = pd.merge(self.__data_frame, df1, on='id', how=how_in)
        return Features(df2)


    def save(self, storage_name, type_storage='file', do_append=True):
      
        try:
            if type_storage == 'file':
                return self.__save_file(storage_name, do_append)
            else:
                raise MyException.MyException("error: storage type no specified or not found")
            return 0
        except Exception as e:
            print("one or more input labels might be wrong:{}".format(e))
            return 0


    def __save_file(self, file_name, do_append):
       
        if do_append==True:
            add_header = False
            if os.path.isfile(file_name) == False:
                add_header = True
            with open(file_name, 'a') as f: # it appends or creates a new file
                self.__data_frame.to_csv(f, header=add_header)
        else:
            with open(file_name, 'w') as f: # it creates a new file
                self.__data_frame.to_csv(f, header=True)
        return 1

    def extract_features(image_path, vector_size=32):

    image = imread(image_path, mode="RGB")
    try:
        
        alg = cv2.KAZE_create() # image keypoints
        kps = alg.detect(image) # # Getting first 32 of them
        kps = sorted(kps, key=lambda x: -x.response)[:vector_size]
        kps, dsc = alg.compute(image, kps) #feature vector
        dsc = dsc.flatten() #descriptor vector 64
        needed_size = (vector_size * 64)
        
		if dsc.size < needed_size:
            
            dsc = np.concatenate([dsc, np.zeros(needed_size - dsc.size)])
    except cv2.error as e:
        print ("Error ", e)
        return -1


    def get_dataframe(self, include_class=False):
       
       
        try:
            df = self.__data_frame.copy()

            if include_class == True:
                if self.__class_name == '':
                    raise MyException.MyException("error: class name not set")
                if self.__class_value is None:
                    raise MyException.MyException("error: class value not set")
                df[self.__class_name]=self.__class_value

            return df
        except MyException.MyException as e:
            print(e.args)
            return None