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

model_path = 'experiments/train_test_dataset37/models/net_g_latest.pth'  # models/RRDB_ESRGAN_x4.pth OR models/RRDB_PSNR_x4.pth
device = torch.device('cuda')  # if you want to run on CPU, change 'cuda' -> cpu
# device = torch.device('cpu')
#assert len(model_path) == len(dni_weight), 'model_path and dni_weight should have the save length.'
loadnet = torch.load(model_path, map_location=torch.device('cpu'))
if 'params_ema' in loadnet:
            keyname = 'params_ema'
else:
    keyname = 'params'




test_img_folder = 'img_car_for_cuongdetectlp'

model = arch.RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
model.load_state_dict(loadnet[keyname], strict=True)
model.eval()
model = model.to(device)

print('Model path {:s}. \nTesting...'.format(model_path))

idx = 0

for path_name in os.listdir(test_img_folder):
    path = osp.join(test_img_folder,path_name)
    idx += 1
    base = osp.splitext(osp.basename(path))[0]
    print(idx, base)
    # read images
    print("path", path)
    img = wide_lp_singleimage.wide_img_lp(path)
    cv2.imwrite('result_preprocessing/{:s}_rlt.png'.format(base), img)
    #img = cv2.imread(path, cv2.IMREAD_COLOR)

    #h, w, c = img.shape
    #img = cv2.resize(img,(int(w/4),int(h/4)))
    img = img * 1.0 / 255
    img = torch.from_numpy(np.transpose(img[:, :, [2, 1, 0]], (2, 0, 1))).float()
    img_LR = img.unsqueeze(0)
    img_LR = img_LR.to(device)
    t0 = time.time()
    with torch.no_grad():
        output = model(img_LR).data.squeeze().float().cpu().clamp_(0, 1).numpy()
    output = np.transpose(output[[2, 1, 0], :, :], (1, 2, 0))
    output = (output * 255.0).round()
    t1 = time.time()
    print("time",t1-t0)
    cv2.imwrite('results/{:s}_rlt.png'.format(base), output)
    # 
    #print(output)
    text = ocr.paddele_ocr(output)
    print("text",text)
