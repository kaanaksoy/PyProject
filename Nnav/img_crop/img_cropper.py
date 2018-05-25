#Credit: Ilya Kavalerov and alexanderankin

#Original algorithm by Ilya Kavalerov
#GitHub Repo by alexanderankin

#See for the original algorithm
#http://artsy.github.io/blog/2014/09/24/using-pattern-recognition-to-automatically-crop-framed-art/

#See repository for the code I've adapted
#https://github.com/alexanderankin/Contours
import cv2
import numpy as np
import sys
import math
import csv
from img_crop_plotter_funcs import dd, ss
from img_crop_helpers import angle_cos, rank, mask_image


# creates a list of 4 coordinates used to crop
# example output: [y_init, y_fin, x_init, x_fin]

def find_minmax(bbox_arr):
    coors = [[],[]]
    for i in range(4):
        for j in range(2):
            coors[j].append(bbox_arr[i][j])

    return [min(coors[1]), max(coors[1]), min(coors[0]), max(coors[0])]

# finds the area of the input coordinates
# input should be the output of find_minmax()
# returns possible_bbox with the area at index 0
# example output: [area, y_init, y_fin, x_init, x_fin]
def find_area(possible_bbox):
    ylen = (possible_bbox[1] - possible_bbox[0])
    xlen = (possible_bbox[3] - possible_bbox[2])
    area = (xlen * ylen * 1.0)
    possible_bbox.insert(0, area)

    return possible_bbox

#finds the largest bbox that is smaller than the image size.
#input is an array of possible_bbox, which is outputted from find_area.
#returns the coors of the best possible crop
# example output: [y_init, y_fin, x_init, x_fin] (largest bbox)
def comp_bboxes(poss_bbox_arr, height, width):
    poss_bbox_arr.sort(key=lambda bbox: bbox[0], reverse=True)
    img_area = (height * width)
    for i in range(len(poss_bbox_arr)):
        area_covered = (poss_bbox_arr[i][0] / img_area) * 100.0
        if 95 > area_covered:
            del poss_bbox_arr[i][0]
            return poss_bbox_arr[i]

def find_biggestbbox(sorted_squares_arr, height, width):
    poss_bbox_arr = []
    for i in range(len(sorted_squares_arr)):
        poss_bbox_arr.append(find_area(find_minmax(sorted_squares_arr[i])))
    biggest_bbox = comp_bboxes(poss_bbox_arr, height, width)
    return biggest_bbox


def crop_img(filename):
    img = cv2.imread(filename,)

    img_copy = img.copy()[:,:,::-1] # color channel plotting mess http://stackoverflow.com/a/15074748/2256243
    height = img.shape[0]
    width = img.shape[1]

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3)) # matrix of ones

    squares = []
    all_contours = []

    for gray in cv2.split(img):
    	dilated = cv2.dilate(src = gray, kernel = kernel, anchor = (-1,-1))

    	blured = cv2.medianBlur(dilated, 7)

    	# Shrinking followed by expanding can be used for removing isolated noise pixels
    	# another way to think of it is "enlarging the background"
    	# http://www.cs.umb.edu/~marc/cs675/cvs09-12.pdf
    	small = cv2.pyrDown(blured, dstsize = (width / 2, height / 2))
    	oversized = cv2.pyrUp(small, dstsize = (width, height))

    	# after seeing utility of later thresholds (non 0 threshold results)
    	# try instead to loop through and change thresholds in the canny filter
    	# also might be interesting to store the contours in different arrays for display to color them according
    	# to the channel that they came from
    	for thrs in xrange(0, 255, 26):
    		if thrs == 0:
    			edges = cv2.Canny(oversized, threshold1 = 0, threshold2 = 50, apertureSize = 3)
    			next = cv2.dilate(src = edges, kernel = kernel, anchor = (-1,-1))
    		else:
    			retval, next = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)

    		contours, hierarchy = cv2.findContours(next, mode = cv2.RETR_LIST, method = cv2.CHAIN_APPROX_SIMPLE)

    		# how are the contours sorted? outwards to inwards? would be interesting to do a PVE
    		# sort of thing where the contours within a contour (and maybe see an elbow plot of some sort)
    		for cnt in contours:
    			all_contours.append(cnt)
    			cnt_len = cv2.arcLength(cnt, True)
    			cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
    			if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
    				cnt = cnt.reshape(-1, 2)
    				max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)])
    				if max_cos < 0.1:
    					squares.append(cnt)

    sorted_squares = sorted(squares, key=lambda square: rank(square, img))

    if len(sorted_squares) and rank(sorted_squares[0], img) < 3:
    	cv2.drawContours(img, squares, -1, (0,255,255), 1) # draw all found squares
    	cv2.drawContours(img, [sorted_squares[0]], -1, (0,255,60), 3)

    crop_coors = find_biggestbbox(sorted_squares, height, width)
    cropped_img = img[crop_coors[0]:crop_coors[1], crop_coors[2]:crop_coors[3]]

    cropped_img = np.require(cropped_img, np.uint8, 'C') # Required to convert CV image to QImage
    return cropped_img
