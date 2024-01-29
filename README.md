# Robust-Pupil-Detection-Algorithm

We presents a method for robust real-time pupil detection using computer vision techniques in OpenCV and Python. The technique focuses on reducing noise caused by eyelashes and other interferences, thus improving the accuracy and speed of detection. This approach is highly relevant for applications like gaze estimation, human-computer interaction, and advanced driver assistance. 

<br>
<div align="center">
<img src="image/eye-glasses.png" width="200" height="200">
</div>
<div align="center">
Eye Camera with Non-Invasive Infrared Camera
</div>  
<br>  
<div style="text-align: justify;">
The methodology includes preprocessing steps like ROI selection, blurring, and Canny Edge Detection, followed by contour extraction and circular contour detection. The best circular contour is selected as the pupil candidate. The paper also discusses the dataset used, which consists of infrared camera footage, and presents the results showing the effectiveness of the method in terms of accuracy, precision, and processing speed.
<br>  
The eye camera is a Raspberry Pi Zero camera with an OmniVision OV5647 camera sensor from Sparkfun. It is a fixed focus 5 MP camera that supports VGA(640x480) @ 90Hz and 720 p@60 Hz. A frame rate of 72 FPS was obtained on a Raspberry Pi model 4B central processing module. It has an ARM Cortex A72 64-bit SoC @ 1.5GHz and 4GB of RAM.
<br>  
This project was part of the course "Recent Advances in Machine Learning" at Universität Siegen, Germany.
<br>  
The implementation is built and modified on the 2023 paper "Raj, Ankur & Bhattarai, Diwas & Van Laerhoven, Kristof. (2023). An Embedded and Real-Time Pupil Detection Pipeline. 10.48550/arXiv.2302.14098."
<div>


