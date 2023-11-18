import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd

def extract_middle_roi(image, target_width, offset_X, offset_Y):
    """
    Extract the middle region of an image with a specified target width.

    Args:
        image (numpy.ndarray): Input image.
        target_width (int): Desired width of the extracted region.

    Returns:
        numpy.ndarray: Extracted middle region of the image.
    """
    height, width = image.shape[:2]
    aspect_ratio = width / height
    target_height = int(target_width / aspect_ratio)
    x = int((width - target_width) / 2) + offset_X
    y = int((height - target_height) / 2) + offset_Y
    x2 = x + target_width 
    y2 = y + target_height 
    middle_roi = image[y:y2, x:x2]
    return middle_roi


def preprocess_image(image_path, threshold_val=0):
    """
    Preprocess an image by cropping and thresholding.

    Args:
        image_path (str): Path to the input grayscale image.
        threshold_val (int, optional): Threshold value for image thresholding.

    Returns:
        tuple: Tuple containing threshold value and path to the preprocessed image.
    """
    # Load the grayscale image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Crop image
    image = extract_middle_roi(image, 1500)

    if threshold_val == 0:
        threshold_val = 5
        # Find threshold with sd
        for x in range(5, 10):
            mask = np.where(image < x, 1, 0)
            masked_intensities = image[mask == 1]
            mean_intensity = np.mean(masked_intensities)
            sd_intensity = np.std(masked_intensities)
            two_sd = (mean_intensity + (2 * sd_intensity))
            three_sd = (mean_intensity + (3 * sd_intensity))
            print("current threshold: {}".format(x))
            print("two_sd: {}".format(two_sd))
            print("three_sd: {}".format(three_sd))

            if x >= two_sd and x <= three_sd:
                threshold_val = x
                break

    # Filter out pixels with intensities below the threshold_val
    _, image_filtered = cv2.threshold(image, threshold_val, 255, cv2.THRESH_TOZERO)

    print("Threshold value:", threshold_val)

    # Save and download to local disk
    # Extract the filename from the original image path
    filename = image_path.split("/")[-1]

    # Create the new path by concatenating the desired directory and the filename
    new_path = os.path.dirname(image_path) + "/thresholded/"

    # Create the folder if it doesn't exist
    if not os.path.exists(new_path):
        os.makedirs(new_path)

    new_path += filename

    cv2.imwrite(new_path, image_filtered)

    print("Saved thresholded image to: {}".format(new_path))

    return threshold_val, new_path


def RGB_mask(image_path, output_path, threshold_val, offsetX, offsetY, threshold_area=100):
    """
    Preprocess an image by cropping and thresholding.

    Args:
        image_path (str): Path to the input grayscale image.
        threshold_val (int, optional): Threshold value for image thresholding.

    Returns:
        tuple: Tuple containing threshold value and path to the preprocessed image.
    """

    df = pd.DataFrame(columns=['id', 'x', 'y', 'area', 'perimeter', 'total_signal'])

    # Load the grayscale image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Crop image
    image = extract_middle_roi(image, 1500, offsetX, offsetY)
 
    # Filter out pixels with intensities below the threshold_val
    _, image_filtered = cv2.threshold(image, threshold_val, 255, cv2.THRESH_TOZERO)





    print("Threshold value:", threshold_val)

    # Save and download to local disk
    # Extract the filename from the original image path
    filename = image_path.split("/")[-1]

    # Create the new path by concatenating the desired directory and the filename
    new_path = os.path.dirname(image_path) + "/thresholded/"

    # Create the folder if it doesn't exist
    if not os.path.exists(new_path):
        os.makedirs(new_path)

    for row in range(image_filtered.shape[0]):
        for col in range(image_filtered.shape[1]):
            pixel_value = image_filtered[row, col]
            if pixel_value > 0:
                pass
                #image_filtered[row,col]=255
        

       # if (image[row, col] != 0 and blue_img[row,col]==0):
        #    pixel_value = image[row, col]
         #   blue_pixel_value = blue_img[row, col]
          #  print(f'Pixel at ({row}, {col}): {pixel_value}')
           # print(f'Blue Pixel at ({row}, {col}): {blue_pixel_value}')
            #image[row,col]=0

    contours, _ = cv2.findContours(image_filtered, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    filtered_contours = []
    # Create a copy of the original image
    image_with_rectangles = np.copy(image_filtered)

    
    

    id = 0
    for i in range(0, len(contours)):
        contour = contours[i]
    #for contour in contours:
        area = cv2.contourArea(contour)    
             
        if area > threshold_area:  
            filtered_contours.append(contour)
            x, y, w, h = cv2.boundingRect(contour)
            #cv2.rectangle(image_with_rectangles, (x, y), (x + w, y + h), (155), 1)  # Adjust color and thickness as needed
            cv2.drawContours(image_with_rectangles, [contour], -1, 100, 1)

            M = cv2.moments(contour)
            area = M["m00"]
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            # Perimeter
            perimeter = cv2.arcLength(contour, True)
            centroid = [cX, cY]
            cv2.circle(image_with_rectangles, (cX, cY), 0, (0), -1)
            cv2.putText(image_with_rectangles, str(id), (cX - 2, cY - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255, 1)
            

            signal = sum_contour(contour, image)
            df.loc[len(df.index)] = [id, cX, cY, area, perimeter, signal]
            print("ID :", id)
            id = id + 1
    


                
    #Check the images with bounding rectangles
    cv2.imwrite(output_path, image_with_rectangles)
    

    binary_image = np.where(image_filtered > 0,100,0)
    cv2.imwrite("binary.jpg", binary_image)


    new_path += filename

    cv2.imwrite(new_path, image_filtered)
    

    print("Saved thresholded image to: {}".format(new_path))

    return threshold_val, new_path, filtered_contours, df, binary_image


def apply_mask(original_image, contours, output_image, offset_X, offset_Y):
    clear_image = cv2.imread(original_image, cv2.IMREAD_GRAYSCALE)
    clear_image = extract_middle_roi(clear_image, 1500, offset_X, offset_Y)
    mask_image = np.zeros(clear_image.shape)
    for i in range(0, len(contours)): 
        # contour = contours[i]
        cv2.drawContours(mask_image, contours, i, color=1, thickness=-1)
        cv2.imwrite(output_image, clear_image * mask_image)
 
def RGB_mask_no_roi(image_path, output_path, threshold_val):
    """
    Preprocess an image by cropping and thresholding.

    Args:
        image_path (str): Path to the input grayscale image.
        threshold_val (int, optional): Threshold value for image thresholding.

    Returns:
        tuple: Tuple containing threshold value and path to the preprocessed image.
    """

    df = pd.DataFrame(columns=['id', 'x', 'y', 'area', 'perimeter', 'total_signal'])

    # Load the grayscale image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

 
    # Filter out pixels with intensities below the threshold_val
    _, image_filtered = cv2.threshold(image, threshold_val, 255, cv2.THRESH_TOZERO)


    binary_image = np.where(image_filtered > 0,255,0)
    cv2.imwrite("binary.jpg", binary_image)


    print("Threshold value:", threshold_val)

    # Save and download to local disk
    # Extract the filename from the original image path
    filename = image_path.split("/")[-1]

    # Create the new path by concatenating the desired directory and the filename
    new_path = os.path.dirname(image_path) + "/thresholded/"

    # Create the folder if it doesn't exist
    if not os.path.exists(new_path):
        os.makedirs(new_path)

    contours, _ = cv2.findContours(image_filtered, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
   # cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    filtered_contours = []
    # Create a copy of the original image
    image_with_rectangles = np.copy(image_filtered)

    
    threshold_area = 100

    id = 0
    for i in range(0, len(contours)):
        contour = contours[i]
    #for contour in contours:
        area = cv2.contourArea(contour)    
             
        if area > threshold_area:  
            filtered_contours.append(contour)
            x, y, w, h = cv2.boundingRect(contour)
            #cv2.rectangle(image_with_rectangles, (x, y), (x + w, y + h), (155), 1)  # Adjust color and thickness as needed
            cv2.drawContours(image_with_rectangles, [contour], -1, 100, 1)

            M = cv2.moments(contour)
            area = M["m00"]
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            # Perimeter
            perimeter = cv2.arcLength(contour, True)
            centroid = [cX, cY]
            cv2.circle(image_with_rectangles, (cX, cY), 0, (0), -1)
            cv2.putText(image_with_rectangles, str(id), (cX - 2, cY - 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255, 1)
            

            signal = sum_contour(contour, image)
            df.loc[len(df.index)] = [id, cX, cY, area, perimeter, signal]
            print("ID :", id)
            id = id + 1
                
    #Check the images with bounding rectangles
    cv2.imwrite(output_path, image_with_rectangles)
    
    new_path += filename

    cv2.imwrite(new_path, image_filtered)

    print("Saved thresholded image to: {}".format(new_path))

    return threshold_val, new_path, filtered_contours, df, binary_image

def read_and_filter_image(image_path, output_path, threshold=8):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    image = extract_middle_roi(image, 1500)
    _, image_filtered = cv2.threshold(image, threshold, 255, cv2.THRESH_TOZERO)
    cv2.imwrite(output_path, image_filtered)
    

def mean_contour_pixel_diff(image1_path, image2_path, num_of_contour):
    image1 = cv2.imread(image1_path, cv2.IMREAD_GRAYSCALE)
    image2 = cv2.imread(image2_path, cv2.IMREAD_GRAYSCALE)
    diff = cv2.absdiff(image1, image2)
    count = (np.count_nonzero(image1 > 0) + np.count_nonzero(image2 > 0)) / 2
    return cv2.sumElems(diff)[0] / count

def sum_contour(contour, image):
    sum = 0
    mask = np.zeros_like(image)
    
    for dot in contour:
        #print([dot[0][0], "   ", dot[0][1]])
        sum = sum + image[dot[0][1], dot[0][0]]
    return sum

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

def signal_sum_overlap(image, array, overlap_map):
    sum = 0
    for point in array:
        if overlap_map[point[0]][point[1]] > 0:
            sum = sum + int (image[point[0]][point[1]] * overlap_map[point[0]][point[1]] / 100)
        else:
            sum = sum + image[point[0]][point[1]]
    return sum

def get_signal_mapping(image, mapping):
    new_map = {}
    for key in mapping:
        new_map[key] = signal_sum(image, mapping[key])
    return new_map

def get_signal_mapping_overlap(image, mapping, overlap_map):
    new_map = {}
    for key in mapping:
        new_map[key] = signal_sum_overlap(image, mapping[key], overlap_map)
    return new_map

def read_and_extract_roi(path, offset_X, offset_Y):
    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    # Crop image
    image = extract_middle_roi(image, 1500, offset_X, offset_Y)
    cv2.imwrite(path + '_roi.jpg', image)
    return image

def generate_mapping(contours, image):
    covered_pixels_mapping = {}
    for i in range(0, len(contours)): 
        contour = contours[i]
        mask_image_1 = np.zeros(image.shape)
        cv2.drawContours(mask_image_1, contours, i, color=1, thickness=-1)
        covered_pixels_mapping[i] = np.argwhere(mask_image_1 > 0)
            #print([dot[0][0], "   ", dot[0][1]])
            #image[dot[0][1], dot[0][0]] = 255
    return covered_pixels_mapping
    