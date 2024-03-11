import glob
import json


#create classes dict
def find_label_name(filepath,dict_label):
  #open json file
  with open(filepath,'r',encoding='UTF-8') as f:
    result = json.load(f)
    annotations = result[0]['annotations']
    #find json['annotations'][label]
    for annotation in annotations:
      label_name = annotation['label']
      if label_name in dict_label:
        index = dict_label[label_name] + 1
        dict_label[label_name] = index
        print(label_name + ':  '+ str(dict_label[label_name]))
      else:
        dict_label[label_name] = 1


if __name__ == "__main__":
  
  #Input Path(Only json)
  original_txt_path = "E:/Projects/Image_Handle/Original_Img/*.json"
  #original_txt_path = "/content/drive/MyDrive/ZS/PythonImageHandle/Original_Img/*.txt"

  #label quantity total
  dict_label = {}
  for text_file in glob.glob(original_txt_path):
      find_label_name(text_file,dict_label)
      print(dict_label)
