# Robust-Pupil-Detection-Algorithm

The purpose of this project is to detect the position of the pupil in an image or video, thus enabling ubiquitous eye-tracking applications such as Gaze Estimation, Human-Computer-Interaction, Advanced Driver Assistance.  Accurate pupil detection is crucial as errors in detection can degrade the performance in its respective applications.
Our project proposes a method for robust real time pupil detections with improved accuracy and detection speed which can be integrated into embedded architectures.

Methodology:
1)     Selecting a region of interest (ROI) from the input source and convert it to grayscale and perform CLAHE contrast enhancement.
2)     Utilization of both Median and Gaussian blurring effectively reduces noise, providing improved edge detection using Canny algorithm resulting in overall faster processing speed, contributing to more accurate and efficient pupil detection. Morphological closing operation closes the gaps between detected edges, improving contour detection.
3)     The detected Contours are filtered based on certain area and circularity criteria, with only the best circular contour based on circularity is considered as a potential pupil candidate.
