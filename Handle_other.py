
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
import os.path
import glob
import numpy as np
import cv2


def convertpng(indir,outdir):
    #opcv compression Handle
    filename = os.path.join(outdir,os.path.basename(indir))  
    img = cv2.imread(indir)
    #zoom level
    fscale = 0.5
    img = cv2.resize(img, None, fx=fscale, fy=fscale,interpolation=cv2.INTER_CUBIC)    
    blur_image = cv2.GaussianBlur(img, (5, 5), 0)
    #GaussianBlured image save
    cv2.imwrite(filename,blur_image)
    #compressed image save
    opcv_filename = filename.replace("Compression_Img","Opencv_Img")
    cv2.imwrite(opcv_filename,img)
    

def calculate_cut_img_position(filepath):

   original_img_path = filepath.replace(".txt",".png")
   opcv_img_path =  original_img_path.replace("Original_Img","Opencv_Img")
   compressed_img_path = original_img_path.replace("Original_Img","Compression_Img")
   convert_Img_path = original_img_path.replace("Original_Img","Convert_Img")

   opcv_img = Image.open(opcv_img_path)
   opcv_img_width = opcv_img.size[0]
   opcv_img_height = opcv_img.size[1]

   compressed_img = Image.open(compressed_img_path)
   
   with open(filepath, "r") as lines_pos:
     lines = lines_pos.readlines()
     for line in lines:
       line_ = line.replace("\n","")
       line_pos = line_.split(' ')
       pos_left = int(float(line_pos[1])*opcv_img_width - ((float(line_pos[3])*opcv_img_width)/2))
       pos_upper = int(float(line_pos[2])*opcv_img_height - ((float(line_pos[4])*opcv_img_height)/2))
       pos_right = int(float(line_pos[1])*opcv_img_width + ((float(line_pos[3])*opcv_img_width)/2))
       pos_lower = int(float(line_pos[2])*opcv_img_height + ((float(line_pos[4])*opcv_img_height)/2))
       
       local_image = opcv_img.crop((pos_left,pos_upper,pos_right,pos_lower))
       local_image =local_image.convert('L')
       
       compressed_img.paste(local_image,(pos_left,pos_upper,pos_right,pos_lower))
       compressed_img.save(convert_Img_path)
   print('convert_Img_path:'+ convert_Img_path+'------Save Finished')


if __name__ == "__main__":
  
  #In Path(Only png)
  original_img_path = "E:/Projects/Image_Handle/Original_Img/*.png"
  #Out path
  compressed_img_path = "E:/Projects/Image_Handle/Compression_Img"
  for indir in glob.glob(original_img_path):
    convertpng(indir,compressed_img_path)
    print('Compression  Finished')
  
  original_txt_path = "E:/Projects/Image_Handle/Original_Img/*.txt"
  for text_file in glob.glob(original_txt_path):
     calculate_cut_img_position(text_file)



