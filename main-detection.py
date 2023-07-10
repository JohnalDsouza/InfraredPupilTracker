import cv2
import numpy as np
import random as rng
import math
import time

video_path = 'output3aa.mp4'  # Replace with your video file path
cap = cv2.VideoCapture(video_path)

while cap.isOpened():
    
    ret, frame = cap.read()
    
    if not ret:
        break
    t1 = time.time()
    roi = frame[0:350, 0:500]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    cl1 = cv2.createCLAHE(clipLimit=8, tileGridSize=(8, 8))
    clahe = cl1.apply(gray)
    blur = cv2.medianBlur(clahe,17)
    blurred = cv2.GaussianBlur(blur, (21, 21), 1.5, 1.5, cv2.BORDER_REPLICATE)
    t3 = time.time()
    edges = cv2.Canny(blurred, threshold1=55, threshold2=100)
    
    t4 = time.time()
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10,10))
    output = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    
    _contours, _ = cv2.findContours(output, cv2.RETR_LIST, cv2.CHAIN_APPROX_TC89_KCOS)
    drawing = np.copy(roi)
    _drawing = np.copy(roi)

    _contours_filtered = []

    # FINDING CIRCULAR CONTOURS
    for contour_index, contour in enumerate(_contours):
        convex_hull = cv2.convexHull(contour)
        area_hull = cv2.contourArea(convex_hull)
    
        if area_hull>280:
            # print(area_hull)
            circumference_hull = cv2.arcLength(convex_hull, True)
            
            if circumference_hull <= 300:
                circularity_hull = (4 * np.pi * area_hull) / circumference_hull ** 2
                if  circularity_hull > 0.85:
                    # print(circularity_hull)
                    _contours_filtered.append(convex_hull)
                    
    min_circularity = 1.5  
    min_circularity_circle = None
    
    minEllipse = [cv2.fitEllipse(c) for c in _contours_filtered]

    # SELECTING THE BEST CIRCULAR CONTOUR ie. PUPIL
    for i, ellipse in enumerate(minEllipse):
        circumference = cv2.arcLength(_contours_filtered[i], True)
        circularity = circumference ** 2 / (4 * math.pi * cv2.contourArea(_contours_filtered[i]))

        if circularity < min_circularity:
            min_circularity = circularity
            min_circularity_circle = ellipse
            # print(ellipse)
            
    # DRAWING THE PUPIL            
    if min_circularity_circle is not None:
        contour_points = cv2.ellipse2Poly((int(min_circularity_circle[0][0]), int(min_circularity_circle[0][1])),
                                          (int(min_circularity_circle[1][0] / 2), int(min_circularity_circle[1][1] / 2)),
                                          int(min_circularity_circle[2]), 0, 360, 1)
        m = cv2.moments(contour_points)
        if m['m00'] != 0:
            center = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
            cv2.circle(_drawing, center, 3, (0, 255, 0), -1)   
        try:
            cv2.ellipse(_drawing, box=min_circularity_circle, color=(0, 255, 0),thickness = 2)   
        except:
            pass

    
    t2 = time.time()
    cv2.putText(_drawing,"FPS : {:.2f}".format((t2-t1)),(5,150),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,255,255),2)
    # print(t4-t3)
    cv2.imshow('gray2', blurred)
    cv2.imshow('edges', edges)
    cv2.imshow('circles', _drawing)

    if cv2.waitKey(10) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()