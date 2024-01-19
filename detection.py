import cv2
import numpy as np
import random as rng
import math
import time
import datetime
frame_rate = []
time_rate = []
video_path = 'output2jd.mp4'  # Replace with your video file path

cap = cv2.VideoCapture(video_path)
Total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
center_list = {} 
frame_no =1


while cap.isOpened():
    
    ret, frame = cap.read()
    
    if not ret:
        break
    
    start = time.perf_counter()
    
    ###################################
    ##### PREPROCESSING OF IMAGE ######
    ###################################
    
    roi = frame[0:350, 0:500]
    # Convert image to grayscale
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    # Blurring of image
    blur = cv2.medianBlur(gray,5)
    blurred = cv2.GaussianBlur(blur, (7,7), 1.5, 1.5, cv2.BORDER_REPLICATE)
    
    # Detect edges
    edges = cv2.Canny(blurred, threshold1=10, threshold2=50)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1,1))
    edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    
    # Find Contours
    _contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_TC89_KCOS)
    _drawing = np.copy(roi)
    
    
    _contours_filtered = []
    
    ###########################################
    ####### FINDING CIRCULAR CONTOURS #########
    ###########################################
    
    for contour_index, contour in enumerate(_contours):
        convex_hull = cv2.convexHull(contour)
        area_hull = cv2.contourArea(convex_hull)
        if  area_hull>280:
            # print(area_hull)
            circumference_hull = cv2.arcLength(convex_hull, True)
            # print(circumference_hull)
            if circumference_hull <= 400:
                circularity_hull = (4 * np.pi * area_hull) / circumference_hull ** 2
                if  circularity_hull > 0.85:
                    # print(circularity_hull)
                    _contours_filtered.append(convex_hull)
    
    ###################################################################
    ####### SELECTING THE BEST CIRCULAR CONTOUR ie. PUPIL #############
    ###################################################################
    
    min_circularity = 1.5
    min_circularity_circle = None
    
    minEllipse = [cv2.fitEllipse(c) for c in _contours_filtered]
    
    for i, ellipse in enumerate(minEllipse):
        circumference = cv2.arcLength(_contours_filtered[i], True)
        circularity = circumference ** 2 / (4 * math.pi * cv2.contourArea(_contours_filtered[i]))

        if circularity < min_circularity:
            min_circularity = circularity
            min_circularity_circle = ellipse
            
    ################################      
    ###### DRAWING THE PUPIL  ###### 
    ################################ 
    
    if min_circularity_circle is not None:
        contour_points = cv2.ellipse2Poly((int(min_circularity_circle[0][0]), int(min_circularity_circle[0][1])),
                                          (int(min_circularity_circle[1][0] / 2), int(min_circularity_circle[1][1] / 2)),
                                          int(min_circularity_circle[2]), 0, 360, 1)
        m = cv2.moments(contour_points)
        if m['m00'] != 0:
            center = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
            # The center of the pupil is stored in center_list, which will be used for Analysis
            center_list.update({frame_no: center})
            cv2.circle(_drawing, center, 3, (0, 255, 0), -1)   
        try:
            cv2.ellipse(_drawing, box=min_circularity_circle, color=(0, 255, 0),thickness = 2)   
        except:
            pass

    
    end = time.perf_counter()
    dtime = (end-start)
    
    if dtime > 0:  
        fps = 1 / dtime
    else:
        fps = float('inf')  

    
    time_rate.append(dtime)
    frame_rate.append(fps)
    cv2.putText(_drawing,str(fps), (0, 300),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    
    #out.write(_drawing)
    # Display Output
    cv2.imshow('median',blur)
    cv2.imshow('gray2', blurred)
    cv2.imshow('edges', edges)
    cv2.imshow('circles', _drawing)
    
    
    frame_no += 1

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
