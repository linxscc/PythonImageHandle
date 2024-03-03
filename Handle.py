
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
import os.path
import glob


def convertpng(indir,outdir):
    #PIL image compression Handle
    img=Image.open(indir)
    ratio =(178956970 /float(img.size[0]* img.size[1]))** 0.5
    new_width =int(img.size[0]* ratio)
    new_height =int(img.size[1]* ratio)
    new_img=img.resize((new_width,new_height),Image.LANCZOS)   
    new_img.save(os.path.join(outdir,os.path.basename(indir)))
    print(indir+'  Compressed')

def calculate_cut_img_position(filepath):

   original_img_path = filepath.replace(".txt",".png")
   compressed_img_path = original_img_path.replace("Original_Img","Compression_Img")
   convert_Img_path = original_img_path.replace("Original_Img","Convert_Img")

   original_img = Image.open(original_img_path)
   original_img_width = original_img.size[0]
   original_img_height = original_img.size[1]

   compressed_img = Image.open(compressed_img_path)
   compressed_img_width = compressed_img.size[0]
   compressed_img_height = compressed_img.size[1]

   width_offset = compressed_img_width/original_img_width
   height_offset = compressed_img_height/original_img_height
   
   with open(filepath, "r") as lines_pos:
     lines = lines_pos.readlines()
     for line in lines:
       line_ = line.replace("\n","")
       line_pos = line_.split(' ')
       pos_left = int(float(line_pos[1])*original_img_width - ((float(line_pos[3])*original_img_width)/2))
       pos_upper = int(float(line_pos[2])*original_img_height - ((float(line_pos[4])*original_img_height)/2))
       pos_right = int(float(line_pos[1])*original_img_width + ((float(line_pos[3])*original_img_width)/2))
       pos_lower = int(float(line_pos[2])*original_img_height + ((float(line_pos[4])*original_img_height)/2))
       
       local_image = original_img.crop((pos_left,pos_upper,pos_right,pos_lower))
       local_image =local_image.convert('L')
       
       local_image_width = int(local_image.size[0]*width_offset)
       local_image_height = int(local_image.size[0]*height_offset)
       local_image_resize = local_image.resize((local_image_width,local_image_height))

       local_image_left = int(pos_left*width_offset)
       local_image_upper = int(pos_upper*height_offset)
       local_image_right = local_image_left + local_image_width
       local_image_lower = local_image_upper + local_image_height


       compressed_img.paste(local_image_resize,(local_image_left,local_image_upper,local_image_right,local_image_lower))
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
  


