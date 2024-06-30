import os.path as osp
import glob
import cv2
import numpy as np
import torch
import RRDBNet_arch as arch
import time
import wide_lp_singleimage
import os
#import ocr_singleimg as ocr
import ocr 

model_path = 'experiments/train_test_dataset41/models/net_g_latest.pth'  # models/RRDB_ESRGAN_x4.pth OR models/RRDB_PSNR_x4.pth
device = torch.device('cuda')  # if you want to run on CPU, change 'cuda' -> cpu
# device = torch.device('cpu')
#assert len(model_path) == len(dni_weight), 'model_path and dni_weight should have the save length.'
loadnet = torch.load(model_path, map_location=torch.device('cpu'))
if 'params_ema' in loadnet:
            keyname = 'params_ema'
else:
    keyname = 'params'

model = arch.RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
model.load_state_dict(loadnet[keyname], strict=True)
model.eval()
model = model.to(device)

print('Model path {:s}. \nTesting...'.format(model_path))




def process_lp(img):
    img_lp = wide_lp_singleimage.wide_img_lp(img)
    img = img_lp * 1.0 / 255
    img = torch.from_numpy(np.transpose(img[:, :, [2, 1, 0]], (2, 0, 1))).float()
    img_LR = img.unsqueeze(0)
    img_LR = img_LR.to(device)
    t0 = time.time()
    with torch.no_grad():
        output = model(img_LR).data.squeeze().float().cpu().clamp_(0, 1).numpy()
    output = np.transpose(output[[2, 1, 0], :, :], (1, 2, 0))
    output = (output * 255.0).round()
    print("shape", output.shape)
    cv2.imwrite("/home/minhanh/Downloads/jetson_nano_MOT/results/esr_img.png",output)
    
    t1 = time.time()
    print("time",t1-t0)
    if output.dtype == np.float32:  # Kiểm tra kiểu dữ liệu
        output = output.astype(np.uint8)
    text = ocr.paddele_ocr(output)
    
    return text

if __name__ == "__main__":
      img_path = "img_car_for_cuongdetectlp/img car_screenshot7_03.06.2024.png"
      img =  cv2.imread(img_path)
      text = process_lp(img)
      print("text",text)