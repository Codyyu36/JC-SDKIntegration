import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd
import skimage
# Area:
# R     70
# G     50 + 50
# B    100
def hi():
    print('hi')
    
def signal_sum(image, array):
    sum = 0
    for point in array:
        sum = sum + image[point[0]][point[1]]
    return sum

def get_signal_mapping(image, mapping):
    new_map = {}
    for key in mapping:
        new_map[key] = signal_sum(image, mapping[key])
    return new_map

def mean_pooling(image, kernal_size):
    return skimage.measure.block_reduce(image, (kernal_size,kernal_size), np.mean)

def signal_sum_overlap(image, key, array, overlap_map):
    sum = 0
    idx = -1
    for point in array:
        if overlap_map[point[0]][point[1]] > 0:
            sum = sum + int (image[point[0]][point[1]] * overlap_map[point[0]][point[1]])
            idx = key
        else:
            sum = sum + image[point[0]][point[1]]
    return sum, idx

def get_signal_mapping_overlap(image, mapping, overlap_map):
    new_map = {}
    idx_set = []
    for key in mapping:
        new_map[key], idx = signal_sum_overlap(image, key,mapping[key], overlap_map)
        if idx != -1:
            idx_set.append(idx)
    return new_map, idx_set

def generate_RGB_dataframes(red_covered_pixels_mapping, green_covered_pixels_mapping, blue_covered_pixels_mapping, is_down_sample=False, kernal=5, overlap_percentage=None, mask=None):
    clear_image_4 = cv2.imread('/Users/codyyu/Desktop/leakage_data_WHITE_TEST/reduced/4_4_4_clear_140000000.bmp', cv2.IMREAD_GRAYSCALE)

    if type(mask) == type(None):
        mask = np.ones_like(clear_image_4)

    clear_image_4 = cv2.imread('/Users/codyyu/Desktop/leakage_data_WHITE_TEST/reduced/4_4_4_clear_140000000.bmp', cv2.IMREAD_GRAYSCALE) * mask
    clear_image_8 = cv2.imread('/Users/codyyu/Desktop/leakage_data_WHITE_TEST/reduced/8_8_8_clear_49000000.bmp', cv2.IMREAD_GRAYSCALE) * mask
    clear_image_16 = cv2.imread('/Users/codyyu/Desktop/leakage_data_WHITE_TEST/reduced/16_16_16_clear_11200000.bmp', cv2.IMREAD_GRAYSCALE) * mask
    clear_image_32 = cv2.imread('/Users/codyyu/Desktop/leakage_data_WHITE_TEST/reduced/32_32_32_clear_2800000.bmp', cv2.IMREAD_GRAYSCALE) * mask
    clear_image_64 = cv2.imread('/Users/codyyu/Desktop/leakage_data_WHITE_TEST/reduced/64_64_64_clear_489999.bmp', cv2.IMREAD_GRAYSCALE) * mask
    clear_image_128 = cv2.imread('/Users/codyyu/Desktop/leakage_data_WHITE_TEST/reduced/128_128_128_clear_125999.bmp', cv2.IMREAD_GRAYSCALE) * mask
    clear_image_255 = cv2.imread('/Users/codyyu/Desktop/leakage_data_WHITE_TEST/reduced/255_255_255_clear_21000.bmp', cv2.IMREAD_GRAYSCALE) * mask

    red_image_4 = cv2.imread('/Users/codyyu/Desktop/leakage_data_WHITE_TEST/reduced/4_4_4_X_140000000.bmp', cv2.IMREAD_GRAYSCALE) * mask
    red_image_8 = cv2.imread('/Users/codyyu/Desktop/leakage_data_WHITE_TEST/reduced/8_8_8_X_49000000.bmp', cv2.IMREAD_GRAYSCALE) * mask
    red_image_16 = cv2.imread('/Users/codyyu/Desktop/leakage_data_WHITE_TEST/reduced/16_16_16_X_11200000.bmp', cv2.IMREAD_GRAYSCALE) * mask
    red_image_32 = cv2.imread('/Users/codyyu/Desktop/leakage_data_WHITE_TEST/reduced/32_32_32_X_3500000.bmp', cv2.IMREAD_GRAYSCALE) * mask
    red_image_64 = cv2.imread('/Users/codyyu/Desktop/leakage_data_WHITE_TEST/reduced/64_64_64_X_595000.bmp', cv2.IMREAD_GRAYSCALE) * mask
    red_image_128 = cv2.imread('/Users/codyyu/Desktop/leakage_data_WHITE_TEST/reduced/128_128_128_X_125999.bmp', cv2.IMREAD_GRAYSCALE) * mask
    red_image_255 = cv2.imread('/Users/codyyu/Desktop/leakage_data_WHITE_TEST/reduced/255_255_255_X_21000.bmp', cv2.IMREAD_GRAYSCALE) * mask


    green_image_4 = cv2.imread('/Users/codyyu/Desktop/leakage_data_WHITE_TEST/reduced/4_4_4_Y_140000000.bmp', cv2.IMREAD_GRAYSCALE) * mask
    green_image_8 = cv2.imread('/Users/codyyu/Desktop/leakage_data_WHITE_TEST/reduced/8_8_8_Y_28000000.bmp', cv2.IMREAD_GRAYSCALE) * mask
    green_image_16 = cv2.imread('/Users/codyyu/Desktop/leakage_data_WHITE_TEST/reduced/16_16_16_Y_8750000.bmp', cv2.IMREAD_GRAYSCALE) * mask
    green_image_32 = cv2.imread('/Users/codyyu/Desktop/leakage_data_WHITE_TEST/reduced/32_32_32_Y_2100000.bmp', cv2.IMREAD_GRAYSCALE) * mask
    green_image_64 = cv2.imread('/Users/codyyu/Desktop/leakage_data_WHITE_TEST/reduced/64_64_64_Y_455000.bmp', cv2.IMREAD_GRAYSCALE) * mask
    green_image_128 = cv2.imread('/Users/codyyu/Desktop/leakage_data_WHITE_TEST/reduced/128_128_128_Y_91000.bmp', cv2.IMREAD_GRAYSCALE) * mask
    green_image_255 = cv2.imread('/Users/codyyu/Desktop/leakage_data_WHITE_TEST/reduced/255_255_255_Y_17500.bmp', cv2.IMREAD_GRAYSCALE) * mask


    blue_image_4 = cv2.imread('/Users/codyyu/Desktop/leakage_data_WHITE_TEST/reduced/4_4_4_Z_210000000.bmp', cv2.IMREAD_GRAYSCALE) * mask
    blue_image_8 = cv2.imread('/Users/codyyu/Desktop/leakage_data_WHITE_TEST/reduced/8_8_8_Z_77000000.bmp', cv2.IMREAD_GRAYSCALE) * mask
    blue_image_16 = cv2.imread('/Users/codyyu/Desktop/leakage_data_WHITE_TEST/reduced/16_16_16_Z_14699999.bmp', cv2.IMREAD_GRAYSCALE) * mask
    blue_image_32 = cv2.imread('/Users/codyyu/Desktop/leakage_data_WHITE_TEST/reduced/32_32_32_Z_4550000.bmp', cv2.IMREAD_GRAYSCALE) * mask
    blue_image_64 = cv2.imread('/Users/codyyu/Desktop/leakage_data_WHITE_TEST/reduced/64_64_64_Z_770000.bmp', cv2.IMREAD_GRAYSCALE) * mask
    blue_image_128 = cv2.imread('/Users/codyyu/Desktop/leakage_data_WHITE_TEST/reduced/128_128_128_Z_140000.bmp', cv2.IMREAD_GRAYSCALE) * mask
    blue_image_255 = cv2.imread('/Users/codyyu/Desktop/leakage_data_WHITE_TEST/reduced/255_255_255_Z_28000.bmp', cv2.IMREAD_GRAYSCALE) * mask

    overlap_set = []
    if is_down_sample:
        clear_image_4 = mean_pooling(clear_image_4, kernal).astype(np.int16)
        clear_image_8 = mean_pooling(clear_image_8, kernal).astype(np.int16)
        clear_image_16 = mean_pooling(clear_image_16, kernal).astype(np.int16)
        clear_image_32 = mean_pooling(clear_image_32, kernal).astype(np.int16)
        clear_image_64 = mean_pooling(clear_image_64, kernal).astype(np.int16)
        clear_image_128 = mean_pooling(clear_image_128, kernal).astype(np.int16)
        clear_image_255 = mean_pooling(clear_image_255, kernal).astype(np.int16)

        red_image_4 = mean_pooling(red_image_4, kernal).astype(np.int16)
        red_image_8 = mean_pooling(red_image_8, kernal).astype(np.int16)
        red_image_16 = mean_pooling(red_image_16, kernal).astype(np.int16)
        red_image_32 = mean_pooling(red_image_32, kernal).astype(np.int16)
        red_image_64 = mean_pooling(red_image_64, kernal).astype(np.int16)
        red_image_128 = mean_pooling(red_image_128, kernal).astype(np.int16)
        red_image_255 = mean_pooling(red_image_255, kernal).astype(np.int16)


        green_image_4 = mean_pooling(green_image_4, kernal).astype(np.int16)
        green_image_8 = mean_pooling(green_image_8, kernal).astype(np.int16)
        green_image_16 = mean_pooling(green_image_16, kernal).astype(np.int16)
        green_image_32 = mean_pooling(green_image_32, kernal).astype(np.int16)
        green_image_64 = mean_pooling(green_image_64, kernal).astype(np.int16)
        green_image_128 = mean_pooling(green_image_128, kernal).astype(np.int16)
        green_image_255 = mean_pooling(green_image_255, kernal).astype(np.int16)


        blue_image_4 = mean_pooling(blue_image_4, kernal).astype(np.int16)
        blue_image_8 = mean_pooling(blue_image_8, kernal).astype(np.int16)
        blue_image_16 = mean_pooling(blue_image_16, kernal).astype(np.int16)
        blue_image_32 = mean_pooling(blue_image_32, kernal).astype(np.int16)
        blue_image_64 = mean_pooling(blue_image_64, kernal).astype(np.int16)
        blue_image_128 = mean_pooling(blue_image_128, kernal).astype(np.int16)
        blue_image_255 = mean_pooling(blue_image_255, kernal).astype(np.int16)
    
    if overlap_percentage is not None:
        print('overlap_percentage loading....')
        red_signal_map_4, a = get_signal_mapping_overlap(clear_image_4, red_covered_pixels_mapping, overlap_percentage[0])
        overlap_set = overlap_set + (a)
        red_signal_map_8 = get_signal_mapping_overlap(clear_image_8, red_covered_pixels_mapping, overlap_percentage[0])[0]
        red_signal_map_16 = get_signal_mapping_overlap(clear_image_16, red_covered_pixels_mapping, overlap_percentage[0])[0]
        red_signal_map_32 = get_signal_mapping_overlap(clear_image_32, red_covered_pixels_mapping, overlap_percentage[0])[0]
        red_signal_map_64 = get_signal_mapping_overlap(clear_image_64, red_covered_pixels_mapping, overlap_percentage[0])[0]
        red_signal_map_128 = get_signal_mapping_overlap(clear_image_128, red_covered_pixels_mapping, overlap_percentage[0])[0]
        red_signal_map_255 = get_signal_mapping_overlap(clear_image_255, red_covered_pixels_mapping, overlap_percentage[0])[0]

        green_signal_map_4,a = get_signal_mapping_overlap(clear_image_4, green_covered_pixels_mapping, overlap_percentage[1])
        overlap_set = overlap_set + (a)
        green_signal_map_8 = get_signal_mapping_overlap(clear_image_8, green_covered_pixels_mapping, overlap_percentage[1])[0]
        green_signal_map_16 = get_signal_mapping_overlap(clear_image_16, green_covered_pixels_mapping, overlap_percentage[1])[0]
        green_signal_map_32 = get_signal_mapping_overlap(clear_image_32, green_covered_pixels_mapping, overlap_percentage[1])[0]
        green_signal_map_64 = get_signal_mapping_overlap(clear_image_64, green_covered_pixels_mapping, overlap_percentage[1])[0]
        green_signal_map_128 = get_signal_mapping_overlap(clear_image_128, green_covered_pixels_mapping, overlap_percentage[1])[0]
        green_signal_map_255 = get_signal_mapping_overlap(clear_image_255, green_covered_pixels_mapping, overlap_percentage[1])[0]

        blue_signal_map_4,a = get_signal_mapping_overlap(clear_image_4, blue_covered_pixels_mapping, overlap_percentage[2])
        overlap_set = overlap_set + (a)
        blue_signal_map_8 = get_signal_mapping_overlap(clear_image_8, blue_covered_pixels_mapping, overlap_percentage[2])[0]
        blue_signal_map_16 = get_signal_mapping_overlap(clear_image_16, blue_covered_pixels_mapping, overlap_percentage[2])[0]
        blue_signal_map_32 = get_signal_mapping_overlap(clear_image_32, blue_covered_pixels_mapping, overlap_percentage[2])[0]
        blue_signal_map_64 = get_signal_mapping_overlap(clear_image_64, blue_covered_pixels_mapping, overlap_percentage[2])[0]
        blue_signal_map_128 = get_signal_mapping_overlap(clear_image_128, blue_covered_pixels_mapping, overlap_percentage[2])[0]
        blue_signal_map_255 = get_signal_mapping_overlap(clear_image_255, blue_covered_pixels_mapping, overlap_percentage[2])[0]

    else:
        red_signal_map_4 = get_signal_mapping(clear_image_4, red_covered_pixels_mapping)
        red_signal_map_8 = get_signal_mapping(clear_image_8, red_covered_pixels_mapping)
        red_signal_map_16 = get_signal_mapping(clear_image_16, red_covered_pixels_mapping)
        red_signal_map_32 = get_signal_mapping(clear_image_32, red_covered_pixels_mapping)
        red_signal_map_64 = get_signal_mapping(clear_image_64, red_covered_pixels_mapping)
        red_signal_map_128 = get_signal_mapping(clear_image_128, red_covered_pixels_mapping)
        red_signal_map_255 = get_signal_mapping(clear_image_255, red_covered_pixels_mapping)

        green_signal_map_4 = get_signal_mapping(clear_image_4, green_covered_pixels_mapping)
        green_signal_map_8 = get_signal_mapping(clear_image_8, green_covered_pixels_mapping)
        green_signal_map_16 = get_signal_mapping(clear_image_16, green_covered_pixels_mapping)
        green_signal_map_32 = get_signal_mapping(clear_image_32, green_covered_pixels_mapping)
        green_signal_map_64 = get_signal_mapping(clear_image_64, green_covered_pixels_mapping)
        green_signal_map_128 = get_signal_mapping(clear_image_128, green_covered_pixels_mapping)
        green_signal_map_255 = get_signal_mapping(clear_image_255, green_covered_pixels_mapping)

        blue_signal_map_4 = get_signal_mapping(clear_image_4, blue_covered_pixels_mapping)
        blue_signal_map_8 = get_signal_mapping(clear_image_8, blue_covered_pixels_mapping)
        blue_signal_map_16 = get_signal_mapping(clear_image_16, blue_covered_pixels_mapping)
        blue_signal_map_32 = get_signal_mapping(clear_image_32, blue_covered_pixels_mapping)
        blue_signal_map_64 = get_signal_mapping(clear_image_64, blue_covered_pixels_mapping)
        blue_signal_map_128 = get_signal_mapping(clear_image_128, blue_covered_pixels_mapping)
        blue_signal_map_255 = get_signal_mapping(clear_image_255, blue_covered_pixels_mapping)

    red_signal_map_ground_truth_4 = get_signal_mapping(red_image_4, red_covered_pixels_mapping)
    red_signal_map_ground_truth_8 = get_signal_mapping(red_image_8, red_covered_pixels_mapping)
    red_signal_map_ground_truth_16 = get_signal_mapping(red_image_16, red_covered_pixels_mapping)
    red_signal_map_ground_truth_32 = get_signal_mapping(red_image_32, red_covered_pixels_mapping)
    red_signal_map_ground_truth_64 = get_signal_mapping(red_image_64, red_covered_pixels_mapping)
    red_signal_map_ground_truth_128 = get_signal_mapping(red_image_128, red_covered_pixels_mapping)
    red_signal_map_ground_truth_255 = get_signal_mapping(red_image_255, red_covered_pixels_mapping)

    green_signal_map_ground_truth_4 = get_signal_mapping(green_image_4, green_covered_pixels_mapping)
    green_signal_map_ground_truth_8 = get_signal_mapping(green_image_8, green_covered_pixels_mapping)
    green_signal_map_ground_truth_16 = get_signal_mapping(green_image_16, green_covered_pixels_mapping)
    green_signal_map_ground_truth_32 = get_signal_mapping(green_image_32, green_covered_pixels_mapping)
    green_signal_map_ground_truth_64 = get_signal_mapping(green_image_64, green_covered_pixels_mapping)
    green_signal_map_ground_truth_128 = get_signal_mapping(green_image_128, green_covered_pixels_mapping)
    green_signal_map_ground_truth_255 = get_signal_mapping(green_image_255, green_covered_pixels_mapping)

    blue_signal_map_ground_truth_4 = get_signal_mapping(blue_image_4, blue_covered_pixels_mapping)
    blue_signal_map_ground_truth_8 = get_signal_mapping(blue_image_8, blue_covered_pixels_mapping)
    blue_signal_map_ground_truth_16 = get_signal_mapping(blue_image_16, blue_covered_pixels_mapping)
    blue_signal_map_ground_truth_32 = get_signal_mapping(blue_image_32, blue_covered_pixels_mapping)
    blue_signal_map_ground_truth_64 = get_signal_mapping(blue_image_64, blue_covered_pixels_mapping)
    blue_signal_map_ground_truth_128 = get_signal_mapping(blue_image_128, blue_covered_pixels_mapping)
    blue_signal_map_ground_truth_255 = get_signal_mapping(blue_image_255, blue_covered_pixels_mapping)


    red_df = pd.DataFrame()
    green_df = pd.DataFrame()
    blue_df = pd.DataFrame()

    red_df["4_ground_truth_mapping"] = red_signal_map_ground_truth_4.values()
    red_df["8_ground_truth_mapping"] = red_signal_map_ground_truth_8.values()
    red_df["16_ground_truth_mapping"] = red_signal_map_ground_truth_16.values()
    red_df["32_ground_truth_mapping"] = red_signal_map_ground_truth_32.values()
    red_df["64_ground_truth_mapping"] = red_signal_map_ground_truth_64.values()
    red_df["128_ground_truth_mapping"] = red_signal_map_ground_truth_128.values()
    red_df["255_ground_truth_mapping"] = red_signal_map_ground_truth_255.values()

    red_df["4_mapping"] = red_signal_map_4.values()
    red_df["8_mapping"] = red_signal_map_8.values()
    red_df["16_mapping"] = red_signal_map_16.values()
    red_df["32_mapping"] = red_signal_map_32.values()
    red_df["64_mapping"] = red_signal_map_64.values()
    red_df["128_mapping"] = red_signal_map_128.values()
    red_df["255_mapping"] = red_signal_map_255.values()

    red_df["4_diff"] = red_df["4_ground_truth_mapping"] - red_df["4_mapping"]
    red_df["8_diff"] = red_df["8_ground_truth_mapping"] - red_df["8_mapping"]
    red_df["16_diff"] = red_df["16_ground_truth_mapping"] - red_df["16_mapping"]
    red_df["32_diff"] = red_df["32_ground_truth_mapping"] - red_df["32_mapping"]
    red_df["64_diff"] = red_df["64_ground_truth_mapping"] - red_df["64_mapping"]
    red_df["128_diff"] = red_df["128_ground_truth_mapping"] - red_df["128_mapping"]
    red_df["255_diff"] = red_df["255_ground_truth_mapping"] - red_df["255_mapping"]

    red_df["4_to_gt_ratio"] = red_df["4_mapping"] / red_df["4_ground_truth_mapping"]
    red_df["8_to_gt_ratio"] = red_df["8_mapping"] / red_df["8_ground_truth_mapping"] 
    red_df["16_to_gt_ratio"] = red_df["16_mapping"] / red_df["16_ground_truth_mapping"]
    red_df["32_to_gt_ratio"] = red_df["32_mapping"] / red_df["32_ground_truth_mapping"]
    red_df["64_to_gt_ratio"] = red_df["64_mapping"] / red_df["64_ground_truth_mapping"]
    red_df["128_to_gt_ratio"] = red_df["128_mapping"] / red_df["128_ground_truth_mapping"]
    red_df["255_to_gt_ratio"] = red_df["255_mapping"] / red_df["255_ground_truth_mapping"]

    red_df["4_diff_percentage"] = ((red_df['4_to_gt_ratio'].mean() - 1) * 100)
    red_df["8_diff_percentage"] = ((red_df['8_to_gt_ratio'].mean() - 1) * 100)
    red_df["16_diff_percentage"] = ((red_df['16_to_gt_ratio'].mean() - 1) * 100)
    red_df["32_diff_percentage"] = ((red_df['32_to_gt_ratio'].mean() - 1) * 100)
    red_df["64_diff_percentage"] = ((red_df['64_to_gt_ratio'].mean() - 1) * 100)
    red_df["128_diff_percentage"] = ((red_df['128_to_gt_ratio'].mean() - 1) * 100)
    red_df["255_diff_percentage"] = ((red_df['255_to_gt_ratio'].mean() - 1) * 100)

    red_df['4_normalized'] = red_df['4_to_gt_ratio'].mean() * red_df["4_ground_truth_mapping"]
    red_df['8_normalized'] = red_df['8_to_gt_ratio'].mean() * red_df["8_ground_truth_mapping"]
    red_df['16_normalized'] = red_df['16_to_gt_ratio'].mean() * red_df["16_ground_truth_mapping"]
    red_df['32_normalized'] = red_df['32_to_gt_ratio'].mean() * red_df["32_ground_truth_mapping"]
    red_df['64_normalized'] = red_df['64_to_gt_ratio'].mean() * red_df["64_ground_truth_mapping"]
    red_df['128_normalized'] = red_df['128_to_gt_ratio'].mean() * red_df["128_ground_truth_mapping"]
    red_df['255_normalized'] = red_df['255_to_gt_ratio'].mean() * red_df["255_ground_truth_mapping"]




    green_df["4_ground_truth_mapping"] = green_signal_map_ground_truth_4.values()
    green_df["8_ground_truth_mapping"] = green_signal_map_ground_truth_8.values()
    green_df["16_ground_truth_mapping"] = green_signal_map_ground_truth_16.values()
    green_df["32_ground_truth_mapping"] = green_signal_map_ground_truth_32.values()
    green_df["64_ground_truth_mapping"] = green_signal_map_ground_truth_64.values()
    green_df["128_ground_truth_mapping"] = green_signal_map_ground_truth_128.values()
    green_df["255_ground_truth_mapping"] = green_signal_map_ground_truth_255.values()

    green_df["4_mapping"] = green_signal_map_4.values()
    green_df["8_mapping"] = green_signal_map_8.values()
    green_df["16_mapping"] = green_signal_map_16.values()
    green_df["32_mapping"] = green_signal_map_32.values()
    green_df["64_mapping"] = green_signal_map_64.values()
    green_df["128_mapping"] = green_signal_map_128.values()
    green_df["255_mapping"] = green_signal_map_255.values()

    green_df["4_diff"] = green_df["4_ground_truth_mapping"] - green_df["4_mapping"]
    green_df["8_diff"] = green_df["8_ground_truth_mapping"] - green_df["8_mapping"]
    green_df["16_diff"] = green_df["16_ground_truth_mapping"] - green_df["16_mapping"]
    green_df["32_diff"] = green_df["32_ground_truth_mapping"] - green_df["32_mapping"]
    green_df["64_diff"] = green_df["64_ground_truth_mapping"] - green_df["64_mapping"]
    green_df["128_diff"] = green_df["128_ground_truth_mapping"] - green_df["128_mapping"]
    green_df["255_diff"] = green_df["255_ground_truth_mapping"] - green_df["255_mapping"]

    green_df["4_to_gt_ratio"] = green_df["4_mapping"] / green_df["4_ground_truth_mapping"]
    green_df["8_to_gt_ratio"] = green_df["8_mapping"] / green_df["8_ground_truth_mapping"] 
    green_df["16_to_gt_ratio"] = green_df["16_mapping"] / green_df["16_ground_truth_mapping"]
    green_df["32_to_gt_ratio"] = green_df["32_mapping"] / green_df["32_ground_truth_mapping"]
    green_df["64_to_gt_ratio"] = green_df["64_mapping"] / green_df["64_ground_truth_mapping"]
    green_df["128_to_gt_ratio"] = green_df["128_mapping"] / green_df["128_ground_truth_mapping"]
    green_df["255_to_gt_ratio"] = green_df["255_mapping"] / green_df["255_ground_truth_mapping"]

    green_df["4_diff_percentage"] = ((green_df['4_to_gt_ratio'].mean() - 1) * 100)
    green_df["8_diff_percentage"] = ((green_df['8_to_gt_ratio'].mean() - 1) * 100)
    green_df["16_diff_percentage"] = ((green_df['16_to_gt_ratio'].mean() - 1) * 100)
    green_df["32_diff_percentage"] = ((green_df['32_to_gt_ratio'].mean() - 1) * 100)
    green_df["64_diff_percentage"] = ((green_df['64_to_gt_ratio'].mean() - 1) * 100)
    green_df["128_diff_percentage"] = ((green_df['128_to_gt_ratio'].mean() - 1) * 100)
    green_df["255_diff_percentage"] = ((green_df['255_to_gt_ratio'].mean() - 1) * 100)

    green_df['4_normalized'] = green_df['4_to_gt_ratio'].mean() * green_df["4_ground_truth_mapping"]
    green_df['8_normalized'] = green_df['8_to_gt_ratio'].mean() * green_df["8_ground_truth_mapping"]
    green_df['16_normalized'] = green_df['16_to_gt_ratio'].mean() * green_df["16_ground_truth_mapping"]
    green_df['32_normalized'] = green_df['32_to_gt_ratio'].mean() * green_df["32_ground_truth_mapping"]
    green_df['64_normalized'] = green_df['64_to_gt_ratio'].mean() * green_df["64_ground_truth_mapping"]
    green_df['128_normalized'] = green_df['128_to_gt_ratio'].mean() * green_df["128_ground_truth_mapping"]
    green_df['255_normalized'] = green_df['255_to_gt_ratio'].mean() * green_df["255_ground_truth_mapping"]



    blue_df["4_ground_truth_mapping"] = blue_signal_map_ground_truth_4.values()
    blue_df["8_ground_truth_mapping"] = blue_signal_map_ground_truth_8.values()
    blue_df["16_ground_truth_mapping"] = blue_signal_map_ground_truth_16.values()
    blue_df["32_ground_truth_mapping"] = blue_signal_map_ground_truth_32.values()
    blue_df["64_ground_truth_mapping"] = blue_signal_map_ground_truth_64.values()
    blue_df["128_ground_truth_mapping"] = blue_signal_map_ground_truth_128.values()
    blue_df["255_ground_truth_mapping"] = blue_signal_map_ground_truth_255.values()

    blue_df["4_mapping"] = blue_signal_map_4.values()
    blue_df["8_mapping"] = blue_signal_map_8.values()
    blue_df["16_mapping"] = blue_signal_map_16.values()
    blue_df["32_mapping"] = blue_signal_map_32.values()
    blue_df["64_mapping"] = blue_signal_map_64.values()
    blue_df["128_mapping"] = blue_signal_map_128.values()
    blue_df["255_mapping"] = blue_signal_map_255.values()

    blue_df["4_diff"] = blue_df["4_ground_truth_mapping"] - blue_df["4_mapping"]
    blue_df["8_diff"] = blue_df["8_ground_truth_mapping"] - blue_df["8_mapping"]
    blue_df["16_diff"] = blue_df["16_ground_truth_mapping"] - blue_df["16_mapping"]
    blue_df["32_diff"] = blue_df["32_ground_truth_mapping"] - blue_df["32_mapping"]
    blue_df["64_diff"] = blue_df["64_ground_truth_mapping"] - blue_df["64_mapping"]
    blue_df["128_diff"] = blue_df["128_ground_truth_mapping"] - blue_df["128_mapping"]
    blue_df["255_diff"] = blue_df["255_ground_truth_mapping"] - blue_df["255_mapping"]

    blue_df["4_to_gt_ratio"] = blue_df["4_mapping"] / blue_df["4_ground_truth_mapping"]
    blue_df["8_to_gt_ratio"] = blue_df["8_mapping"] / blue_df["8_ground_truth_mapping"] 
    blue_df["16_to_gt_ratio"] = blue_df["16_mapping"] / blue_df["16_ground_truth_mapping"]
    blue_df["32_to_gt_ratio"] = blue_df["32_mapping"] / blue_df["32_ground_truth_mapping"]
    blue_df["64_to_gt_ratio"] = blue_df["64_mapping"] / blue_df["64_ground_truth_mapping"]
    blue_df["128_to_gt_ratio"] = blue_df["128_mapping"] / blue_df["128_ground_truth_mapping"]
    blue_df["255_to_gt_ratio"] = blue_df["255_mapping"] / blue_df["255_ground_truth_mapping"]

    blue_df["4_diff_percentage"] = ((blue_df['4_to_gt_ratio'].mean() - 1) * 100)
    blue_df["8_diff_percentage"] = ((blue_df['8_to_gt_ratio'].mean() - 1) * 100)
    blue_df["16_diff_percentage"] = ((blue_df['16_to_gt_ratio'].mean() - 1) * 100)
    blue_df["32_diff_percentage"] = ((blue_df['32_to_gt_ratio'].mean() - 1) * 100)
    blue_df["64_diff_percentage"] = ((blue_df['64_to_gt_ratio'].mean() - 1) * 100)
    blue_df["128_diff_percentage"] = ((blue_df['128_to_gt_ratio'].mean() - 1) * 100)
    blue_df["255_diff_percentage"] = ((blue_df['255_to_gt_ratio'].mean() - 1) * 100)

    blue_df['4_normalized'] = blue_df['4_to_gt_ratio'].mean() * blue_df["4_ground_truth_mapping"]
    blue_df['8_normalized'] = blue_df['8_to_gt_ratio'].mean() * blue_df["8_ground_truth_mapping"]
    blue_df['16_normalized'] = blue_df['16_to_gt_ratio'].mean() * blue_df["16_ground_truth_mapping"]
    blue_df['32_normalized'] = blue_df['32_to_gt_ratio'].mean() * blue_df["32_ground_truth_mapping"]
    blue_df['64_normalized'] = blue_df['64_to_gt_ratio'].mean() * blue_df["64_ground_truth_mapping"]
    blue_df['128_normalized'] = blue_df['128_to_gt_ratio'].mean() * blue_df["128_ground_truth_mapping"]
    blue_df['255_normalized'] = blue_df['255_to_gt_ratio'].mean() * blue_df["255_ground_truth_mapping"]


    red_new_df = pd.DataFrame()

    red_new_df['4_diff'] = 100 * ((red_df['4_mapping'] / red_df['4_mapping'].mean()) - (red_df['4_ground_truth_mapping'] / red_df['4_ground_truth_mapping'].mean()))/((red_df['4_ground_truth_mapping'] / red_df['4_ground_truth_mapping'].mean()))
    red_new_df['8_diff'] = 100 * ((red_df['8_mapping'] / red_df['8_mapping'].mean()) - (red_df['8_ground_truth_mapping'] / red_df['8_ground_truth_mapping'].mean()))/((red_df['8_ground_truth_mapping'] / red_df['8_ground_truth_mapping'].mean()))
    red_new_df['16_diff'] = 100 * ((red_df['16_mapping'] / red_df['16_mapping'].mean()) - (red_df['16_ground_truth_mapping'] / red_df['16_ground_truth_mapping'].mean()))/((red_df['16_ground_truth_mapping'] / red_df['16_ground_truth_mapping'].mean()))
    red_new_df['32_diff'] = 100 * ((red_df['32_mapping'] / red_df['32_mapping'].mean()) - (red_df['32_ground_truth_mapping'] / red_df['32_ground_truth_mapping'].mean()))/((red_df['32_ground_truth_mapping'] / red_df['32_ground_truth_mapping'].mean()))
    red_new_df['64_diff'] = 100 * ((red_df['64_mapping'] / red_df['64_mapping'].mean()) - (red_df['64_ground_truth_mapping'] / red_df['64_ground_truth_mapping'].mean()))/((red_df['64_ground_truth_mapping'] / red_df['64_ground_truth_mapping'].mean()))
    red_new_df['128_diff'] = 100 * ((red_df['128_mapping'] / red_df['128_mapping'].mean()) - (red_df['128_ground_truth_mapping'] / red_df['128_ground_truth_mapping'].mean()))/((red_df['128_ground_truth_mapping'] / red_df['128_ground_truth_mapping'].mean()))
    red_new_df['255_diff'] = 100 * ((red_df['255_mapping'] / red_df['255_mapping'].mean()) - (red_df['255_ground_truth_mapping'] / red_df['255_ground_truth_mapping'].mean()))/((red_df['255_ground_truth_mapping'] / red_df['255_ground_truth_mapping'].mean()))

    red_new_df['A-1_4'] = 100 * ((red_df['4_mapping'] / red_df['4_mapping'].mean()) - 1)
    red_new_df['A-1_8'] = 100 * ((red_df['8_mapping'] / red_df['8_mapping'].mean()) - 1)
    red_new_df['A-1_16'] = 100 * ((red_df['16_mapping'] / red_df['16_mapping'].mean()) - 1)
    red_new_df['A-1_32'] = 100 * ((red_df['32_mapping'] / red_df['32_mapping'].mean()) - 1)
    red_new_df['A-1_64'] = 100 * ((red_df['64_mapping'] / red_df['64_mapping'].mean()) - 1)
    red_new_df['A-1_128'] = 100 * ((red_df['128_mapping'] / red_df['128_mapping'].mean()) - 1)
    red_new_df['A-1_255'] = 100 * ((red_df['255_mapping'] / red_df['255_mapping'].mean()) - 1)

    red_new_df['B-1_4'] = 100 * ((red_df['4_ground_truth_mapping'] / red_df['4_ground_truth_mapping'].mean()) - 1)
    red_new_df['B-1_8'] = 100 * ((red_df['8_ground_truth_mapping'] / red_df['8_ground_truth_mapping'].mean()) - 1)
    red_new_df['B-1_16'] = 100 * ((red_df['16_ground_truth_mapping'] / red_df['16_ground_truth_mapping'].mean()) - 1)
    red_new_df['B-1_32'] = 100 * ((red_df['32_ground_truth_mapping'] / red_df['32_ground_truth_mapping'].mean()) - 1)
    red_new_df['B-1_64'] = 100 * ((red_df['64_ground_truth_mapping'] / red_df['64_ground_truth_mapping'].mean()) - 1)
    red_new_df['B-1_128'] = 100 * ((red_df['128_ground_truth_mapping'] / red_df['128_ground_truth_mapping'].mean()) - 1)
    red_new_df['B-1_255'] = 100 * ((red_df['255_ground_truth_mapping'] / red_df['255_ground_truth_mapping'].mean()) - 1)


    green_new_df = pd.DataFrame()

    green_new_df['4_diff'] = 100 * ((green_df['4_mapping'] / green_df['4_mapping'].mean()) - (green_df['4_ground_truth_mapping'] / green_df['4_ground_truth_mapping'].mean()))/((green_df['4_ground_truth_mapping'] / green_df['4_ground_truth_mapping'].mean()))
    green_new_df['8_diff'] = 100 * ((green_df['8_mapping'] / green_df['8_mapping'].mean()) - (green_df['8_ground_truth_mapping'] / green_df['8_ground_truth_mapping'].mean()))/((green_df['8_ground_truth_mapping'] / green_df['8_ground_truth_mapping'].mean()))
    green_new_df['16_diff'] = 100 * ((green_df['16_mapping'] / green_df['16_mapping'].mean()) - (green_df['16_ground_truth_mapping'] / green_df['16_ground_truth_mapping'].mean()))/((green_df['16_ground_truth_mapping'] / green_df['16_ground_truth_mapping'].mean()))
    green_new_df['32_diff'] = 100 * ((green_df['32_mapping'] / green_df['32_mapping'].mean()) - (green_df['32_ground_truth_mapping'] / green_df['32_ground_truth_mapping'].mean()))/((green_df['32_ground_truth_mapping'] / green_df['32_ground_truth_mapping'].mean()))
    green_new_df['64_diff'] = 100 * ((green_df['64_mapping'] / green_df['64_mapping'].mean()) - (green_df['64_ground_truth_mapping'] / green_df['64_ground_truth_mapping'].mean()))/((green_df['64_ground_truth_mapping'] / green_df['64_ground_truth_mapping'].mean()))
    green_new_df['128_diff'] = 100 * ((green_df['128_mapping'] / green_df['128_mapping'].mean()) - (green_df['128_ground_truth_mapping'] / green_df['128_ground_truth_mapping'].mean()))/((green_df['128_ground_truth_mapping'] / green_df['128_ground_truth_mapping'].mean()))
    green_new_df['255_diff'] = 100 * ((green_df['255_mapping'] / green_df['255_mapping'].mean()) - (green_df['255_ground_truth_mapping'] / green_df['255_ground_truth_mapping'].mean()))/((green_df['255_ground_truth_mapping'] / green_df['255_ground_truth_mapping'].mean()))

    green_new_df['A-1_4'] = 100 * ((green_df['4_mapping'] / green_df['4_mapping'].mean()) - 1)
    green_new_df['A-1_8'] = 100 * ((green_df['8_mapping'] / green_df['8_mapping'].mean()) - 1)
    green_new_df['A-1_16'] = 100 * ((green_df['16_mapping'] / green_df['16_mapping'].mean()) - 1)
    green_new_df['A-1_32'] = 100 * ((green_df['32_mapping'] / green_df['32_mapping'].mean()) - 1)
    green_new_df['A-1_64'] = 100 * ((green_df['64_mapping'] / green_df['64_mapping'].mean()) - 1)
    green_new_df['A-1_128'] = 100 * ((green_df['128_mapping'] / green_df['128_mapping'].mean()) - 1)
    green_new_df['A-1_255'] = 100 * ((green_df['255_mapping'] / green_df['255_mapping'].mean()) - 1)

    green_new_df['B-1_4'] = 100 * ((green_df['4_ground_truth_mapping'] / green_df['4_ground_truth_mapping'].mean()) - 1)
    green_new_df['B-1_8'] = 100 * ((green_df['8_ground_truth_mapping'] / green_df['8_ground_truth_mapping'].mean()) - 1)
    green_new_df['B-1_16'] = 100 * ((green_df['16_ground_truth_mapping'] / green_df['16_ground_truth_mapping'].mean()) - 1)
    green_new_df['B-1_32'] = 100 * ((green_df['32_ground_truth_mapping'] / green_df['32_ground_truth_mapping'].mean()) - 1)
    green_new_df['B-1_64'] = 100 * ((green_df['64_ground_truth_mapping'] / green_df['64_ground_truth_mapping'].mean()) - 1)
    green_new_df['B-1_128'] = 100 * ((green_df['128_ground_truth_mapping'] / green_df['128_ground_truth_mapping'].mean()) - 1)
    green_new_df['B-1_255'] = 100 * ((green_df['255_ground_truth_mapping'] / green_df['255_ground_truth_mapping'].mean()) - 1)


    blue_new_df = pd.DataFrame()

    blue_new_df['4_diff'] = 100 * ((blue_df['4_mapping'] / blue_df['4_mapping'].mean()) - (blue_df['4_ground_truth_mapping'] / blue_df['4_ground_truth_mapping'].mean()))/((blue_df['4_ground_truth_mapping'] / blue_df['4_ground_truth_mapping'].mean()))
    blue_new_df['8_diff'] = 100 * ((blue_df['8_mapping'] / blue_df['8_mapping'].mean()) - (blue_df['8_ground_truth_mapping'] / blue_df['8_ground_truth_mapping'].mean()))/((blue_df['8_ground_truth_mapping'] / blue_df['8_ground_truth_mapping'].mean()))
    blue_new_df['16_diff'] = 100 * ((blue_df['16_mapping'] / blue_df['16_mapping'].mean()) - (blue_df['16_ground_truth_mapping'] / blue_df['16_ground_truth_mapping'].mean()))/((blue_df['16_ground_truth_mapping'] / blue_df['16_ground_truth_mapping'].mean()))
    blue_new_df['32_diff'] = 100 * ((blue_df['32_mapping'] / blue_df['32_mapping'].mean()) - (blue_df['32_ground_truth_mapping'] / blue_df['32_ground_truth_mapping'].mean()))/((blue_df['32_ground_truth_mapping'] / blue_df['32_ground_truth_mapping'].mean()))
    blue_new_df['64_diff'] = 100 * ((blue_df['64_mapping'] / blue_df['64_mapping'].mean()) - (blue_df['64_ground_truth_mapping'] / blue_df['64_ground_truth_mapping'].mean()))/((blue_df['64_ground_truth_mapping'] / blue_df['64_ground_truth_mapping'].mean()))
    blue_new_df['128_diff'] = 100 * ((blue_df['128_mapping'] / blue_df['128_mapping'].mean()) - (blue_df['128_ground_truth_mapping'] / blue_df['128_ground_truth_mapping'].mean()))/((blue_df['128_ground_truth_mapping'] / blue_df['128_ground_truth_mapping'].mean()))
    blue_new_df['255_diff'] = 100 * ((blue_df['255_mapping'] / blue_df['255_mapping'].mean()) - (blue_df['255_ground_truth_mapping'] / blue_df['255_ground_truth_mapping'].mean()))/((blue_df['255_ground_truth_mapping'] / blue_df['255_ground_truth_mapping'].mean()))

    blue_new_df['A-1_4'] = 100 * ((blue_df['4_mapping'] / blue_df['4_mapping'].mean()) - 1)
    blue_new_df['A-1_8'] = 100 * ((blue_df['8_mapping'] / blue_df['8_mapping'].mean()) - 1)
    blue_new_df['A-1_16'] = 100 * ((blue_df['16_mapping'] / blue_df['16_mapping'].mean()) - 1)
    blue_new_df['A-1_32'] = 100 * ((blue_df['32_mapping'] / blue_df['32_mapping'].mean()) - 1)
    blue_new_df['A-1_64'] = 100 * ((blue_df['64_mapping'] / blue_df['64_mapping'].mean()) - 1)
    blue_new_df['A-1_128'] = 100 * ((blue_df['128_mapping'] / blue_df['128_mapping'].mean()) - 1)
    blue_new_df['A-1_255'] = 100 * ((blue_df['255_mapping'] / blue_df['255_mapping'].mean()) - 1)

    blue_new_df['B-1_4'] = 100 * ((blue_df['4_ground_truth_mapping'] / blue_df['4_ground_truth_mapping'].mean()) - 1)
    blue_new_df['B-1_8'] = 100 * ((blue_df['8_ground_truth_mapping'] / blue_df['8_ground_truth_mapping'].mean()) - 1)
    blue_new_df['B-1_16'] = 100 * ((blue_df['16_ground_truth_mapping'] / blue_df['16_ground_truth_mapping'].mean()) - 1)
    blue_new_df['B-1_32'] = 100 * ((blue_df['32_ground_truth_mapping'] / blue_df['32_ground_truth_mapping'].mean()) - 1)
    blue_new_df['B-1_64'] = 100 * ((blue_df['64_ground_truth_mapping'] / blue_df['64_ground_truth_mapping'].mean()) - 1)
    blue_new_df['B-1_128'] = 100 * ((blue_df['128_ground_truth_mapping'] / blue_df['128_ground_truth_mapping'].mean()) - 1)
    blue_new_df['B-1_255'] = 100 * ((blue_df['255_ground_truth_mapping'] / blue_df['255_ground_truth_mapping'].mean()) - 1)

    return red_new_df, green_new_df, blue_new_df, overlap_set


