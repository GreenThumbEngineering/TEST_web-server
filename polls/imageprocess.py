from __future__ import division
import sys, traceback
from cv2 import imread, imwrite, split
import numpy as np
import argparse
from plantcv import plantcv as pcv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, hsv_to_rgb
from django.conf import settings

def crop(img, pos, name):
    image = imread(img)
    height, width = image.shape[:2]
    middle = int(width/2)
    # Borders
    left = 220
    right = 200
    top = 165
    bot = 110
    if pos == 1:
        crop_img = image[top:height-bot, left:middle]
    elif pos == 2:
        crop_img = image[top:height-bot, middle:width-right]
    else:
        crop_img = image[top:height-bot, left:width-right]
    
    imwrite('./polls/media/images/' + str(name) + '.jpg', crop_img)

def segmentation(imgW, imgNIR, shape, DeviceId, timestamp):

    s_threshold = 165
    b_threshold = 200
    # Read image
    img, path, img_filename = pcv.readimage(filename=imgW, mode="native")
    imgNIR, pathNIR, imgNIR_filename = pcv.readimage(filename=imgNIR, mode="native")

    # Convert RGB to HSV and extract the saturation channel
    s = pcv.rgb2gray_hsv(rgb_img=img, channel='s')

    # Threshold the saturation image
    s_thresh = pcv.threshold.binary(gray_img=s, threshold=s_threshold, max_value=255, object_type='light')

    # Median Blur
    s_mblur = pcv.median_blur(gray_img=s_thresh, ksize=5)
    s_cnt = pcv.median_blur(gray_img=s_thresh, ksize=5)

    # Convert RGB to LAB and extract the Blue channel
    b = pcv.rgb2gray_lab(rgb_img=img, channel='b')

    # Threshold the blue image ORIGINAL 160
    b_thresh = pcv.threshold.binary(gray_img=b, threshold=b_threshold, max_value=255, object_type='light')
    b_cnt = pcv.threshold.binary(gray_img=b, threshold=b_threshold, max_value=255, object_type='light')

    # Join the thresholded saturation and blue-yellow images
    bs = pcv.logical_or(bin_img1=s_mblur, bin_img2=b_cnt)

    # Apply Mask (for VIS images, mask_color=white)
    masked = pcv.apply_mask(img=img, mask=bs, mask_color='white')

    # Convert RGB to LAB and extract the Green-Magenta and Blue-Yellow channels
    masked_a = pcv.rgb2gray_lab(rgb_img=masked, channel='a')
    masked_b = pcv.rgb2gray_lab(rgb_img=masked, channel='b')

    # Threshold the green-magenta and blue images
    # 115
    # 135
    # 128
    maskeda_thresh = pcv.threshold.binary(gray_img=masked_a, threshold=115, max_value=255, object_type='dark')
    maskeda_thresh1 = pcv.threshold.binary(gray_img=masked_a, threshold=135, max_value=255, object_type='light')
    maskedb_thresh = pcv.threshold.binary(gray_img=masked_b, threshold=128, max_value=255, object_type='light')

    # Join the thresholded saturation and blue-yellow images (OR)
    ab1 = pcv.logical_or(bin_img1=maskeda_thresh, bin_img2=maskedb_thresh)
    ab = pcv.logical_or(bin_img1=maskeda_thresh1, bin_img2=ab1)

    # Fill small objects
    ab_fill = pcv.fill(bin_img=ab, size=200)

    # Apply mask (for VIS images, mask_color=white)
    masked2 = pcv.apply_mask(img=masked, mask=ab_fill, mask_color='white')

    # Identify objects
    id_objects, obj_hierarchy = pcv.find_objects(img=masked2, mask=ab_fill)

    # Define ROI
    height = shape[0]
    width = shape[1]
    roi1, roi_hierarchy= pcv.roi.rectangle(img=masked2, x=0, y=0, h=height, w=width)

    # Decide which objects to keep
    roi_objects, hierarchy3, kept_mask, obj_area = pcv.roi_objects(img=img, roi_contour=roi1, 
                                                               roi_hierarchy=roi_hierarchy, 
                                                               object_contour=id_objects, 
                                                               obj_hierarchy=obj_hierarchy,
                                                               roi_type='partial')

    # Object combine kept objects
    obj, mask = pcv.object_composition(img=img, contours=roi_objects, hierarchy=hierarchy3)
    
    # Filling holes in the mask, works great for alive plants, not so good for dead plants
    filled_mask = pcv.fill_holes(mask)

    final = pcv.apply_mask(img=imgNIR, mask=mask, mask_color='white')
    pcv.print_image(final, "./polls/segment/" + str(DeviceId) + "_" + str(timestamp.strftime("%Y-%m-%d_%H-%M-%S")) + "_segment" + ".png")
    pcv.print_image(final, "./polls/segment/segment-temp.png")

def NDVI(segmented, DeviceId, timestamp):
    colors = np.load('./polls/colors.npy', allow_pickle=True)
    #img = Image.open('./output/final.png').convert("RGB")
    #img = cv2.imread('./segment/segment-temp.png')
    img = imread(segmented)
    mask = np.asarray(img)
    #imgR, imgG, imgB = img.split()
    imgB, imgG, imgR = split(img)

    arrG = np.asarray(imgG).astype('float')
    arrR = np.asarray(imgR).astype('float')
    arrB = np.asarray(imgB).astype('float')

    redBlueDiff = (arrR  - arrB)
    redBlueSum = (arrR + arrB)

    redBlueSum[redBlueSum ==0] = 0.01

    arrNDVI = redBlueDiff/redBlueSum
    arrNDVI[arrNDVI == 0] = -1
    sumAll = 0
    amount = 0.00001


    for row in arrNDVI:
        for pix in row:
             if pix != -1:
                sumAll += pix
                amount += 1

    fastiecm=LinearSegmentedColormap.from_list('mylist', colors)

    #saves the final NDVI calculated image
    plt.imsave("./polls/ndvi-calculated/" + str(DeviceId) + "_" + str(timestamp.strftime("%Y-%m-%d_%H-%M-%S")) + "_" +  "%.4f.jpg" % (sumAll/float(amount)),arrNDVI,cmap=fastiecm, vmin=-1.0, vmax=1.0)
    
    return sumAll/float(amount)

def main(imgW, imgNIR, DeviceId, timestamp):
    #Crops both pics here
    #Segments image, gets mask from cropW, and applies it to cropNIR

    shape = imread(imgW).shape[:2]
    segmentation(imgW, imgNIR, shape, DeviceId, timestamp)

    #NDVI from segmented image
    ndvi = NDVI('./polls/segment/segment-temp.png', DeviceId, timestamp)

    return ndvi

if __name__== "__main__":
    parser = argparse.ArgumentParser(description="Give images and location")
    parser.add_argument("-w", "--imageW", help="Input white image file.", required=True)
    parser.add_argument("-n", "--imageNIR", help="Input NIR image file.", required=True)
    parser.add_argument("-p", "--position", help="1 or 2", required=True)
    args = parser.parse_args()
    main(imgW=args.imageW, imgNIR=args.imageNIR, pos=args.position)
