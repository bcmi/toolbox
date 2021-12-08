import json
import cv2
import os
import csv
import matplotlib.pyplot as plt
import tkinter as tk
import platform

def GetScreenParam():
    root = tk.Tk()
    return root.winfo_screenwidth(), root.winfo_screenheight()

sysstr = platform.system()
if(sysstr =="Windows"):
    print ("Windows")
    LEFT = 0
    UP   = 1
    RIGHT= 2
    DOWN = 3
    ESC  = 27
elif(sysstr == "Linux"):
    print ("Linux")
    LEFT = 81
    UP   = 82
    RIGHT= 83
    DOWN = 84
    ESC  = 27
elif(sysstr == 'Darwin'):
    print ("Mac OS")
    LEFT = 81
    UP = 82
    RIGHT = 83
    DOWN = 84
    ESC = 27
else:
    print("Unrecognized system")


if __name__ == '__main__':
    # image_root = '/workspace/aesthetic_cropping/human_centric/code/related_work/visualization/best_crop_comparison'
    image_root = '../data'
    if not os.path.exists(image_root):
        image_root = './best_crop_comparison'
    assert os.path.exists(image_root), image_root
    #image_list = [f for f in os.listdir(image_root) if f.endswith('.jpg')]
    image_list = [str(i)+'.jpg' for i in range(1,953)]

    anno_file  = os.path.join(image_root, '..', 'annotations.json')
    previous_done = 856
    index = previous_done
    if os.path.exists(anno_file):
        labels = json.load(open(anno_file, 'r'))
        while index < len(image_list):
            if image_list[index] in labels:
                index += 1
            else:
                break
    else:
        labels = dict()
    print(f'begin with {index+1}.jpg')
    key_label = dict()
    for i in range(1,8):
        key_label[ord(str(i))] = i
    screenwidth, screenheight  = GetScreenParam()
    print('Screen ', screenwidth, screenheight)
    win_name = 'select best posistion'
    top,left = 10, 10
    win_w, win_h = screenwidth, screenheight
    cv2.namedWindow(win_name)
    cv2.resizeWindow(win_name, win_w, win_h)
    cv2.moveWindow(win_name, top, left)

    while len(image_list)-previous_done > len(labels):
        image_name = image_list[index]
        image_file = os.path.join(image_root, image_name)
        im = cv2.imread(image_file)
        if im.shape[0] > screenheight or im.shape[1] > screenwidth:
            ratio = max(float(im.shape[0]) / screenheight, float(im.shape[1] / screenwidth))
            im    = cv2.resize(im, (int(im.shape[1] / ratio), int(im.shape[0] / ratio)))
        title = '{}, Complete {}/{}'.format(image_name,len(labels), len(image_list)-previous_done)
        fontcolor = (0, 255, 0) if (len(labels) / len(image_list)) < 0.9 else (0,0,255)
        cv2.putText(im, title, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, fontcolor, 2)
        cv2.imshow(win_name, im)
        key_num = cv2.waitKey(0)

        if key_num == ord('s'):
            with open(anno_file, 'w') as f:
                json.dump(labels, f)
                print('Save annotations to ', anno_file)
                previous_done = index
            key_num = cv2.waitKey(0)

        if key_num in [ord('q'), ESC]:
            break
        elif key_num in key_label:
            best_crop = key_label[key_num]
            print(f'file {image_name} choose {best_crop}')
            labels[image_name] = best_crop
            index = (index + 1) % len(image_list)
        elif key_num in [UP, LEFT]: # up or left
            print('last image key_num=',key_num)
            index = max(0,(index - 1)) % len(image_list)
        elif key_num in [RIGHT, DOWN]: # down or right
            print('next image')
            index = max(0, (index + 1)) % len(image_list)
        else:
            print('Undefined key_num ', key_num)
    try:
        cv2.destroyAllWindows()
        with open(anno_file, 'w') as f:
            json.dump(labels, f)
        print('Save annotations to ', anno_file)
        if len(image_list) == len(labels):
            print('Thank you very much !')
    except:
        pass

