# -*- coding: utf-8 -*-
#docker run -v /c/Users/Laura/Notflix:/videos -it opencv3
import numpy as np
import cv2
import json

def extract_frame_hsv_histogram(frame):
  bins = [32, 32] 
  hsv_image = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
  channels = [0, 1] # List of channels to analyze.
  ranges = [[0, 180], [0, 256]] # Range per channel.
  
  # We generate a histogram per channel, and then add it to the single-vector histogram.
  for i in range(0, len(channels)):
    channel = channels[i]
    channel_bins = bins[i]
    channel_range = ranges[i]
    histogram = cv2.calcHist(
        [hsv_image],
        [channel],
        None, # one could specify an optional mask here (we don't use this here),
        [channel_bins],
        channel_range
        )   
  histogram = histogram / np.sum(histogram)  # Return a normalized histogram.  
  return histogram.flatten('C')

def hsv_histograms_similarity(hs_histogram0, hs_histogram1):
  similarity = cv2.compareHist(hs_histogram0, hs_histogram1, cv2.HISTCMP_INTERSECT )  
  return similarity

cap = cv2.VideoCapture('house2.mp4')

time = 0
scene = 1
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
timestamps = []
while(time < length): 
    time = time+1
    ret, frame = cap.read()
    ret2, frame2 = cap.read()
    if ret == False or ret2 == False:
        break
    histogram1 = extract_frame_hsv_histogram(frame)
    histogram2 = extract_frame_hsv_histogram(frame2)
    sim = hsv_histograms_similarity(histogram1, histogram2)
    # If similarity is lower than 0.75 possibly a scene change
    if sim < 0.75:
        if scene > 1:
            lastframe1 = cv2.imread("firstframe"+str(scene-1)+".png")
            lastframe2 = cv2.imread("secondframe"+str(scene-1)+".png")
            histogramlast1 = extract_frame_hsv_histogram(lastframe1)
            histogramlast2 = extract_frame_hsv_histogram(lastframe2)
            #sim1 = hsv_histograms_similarity(histogramlast1, histogram1)
            sim2 = hsv_histograms_similarity(histogramlast1, histogram2)
            sim3 = hsv_histograms_similarity(histogramlast2, histogram1)
            sim4 = hsv_histograms_similarity(histogramlast2, histogram2)
            # if they are still pretty similar, the difference with the last scene change frames
            # should be bigger
            if sim > 0.5 :
                if sim2 > 0.6 or sim3 > 0.6 or sim4 > 0.6:
                    continue
            
            if sim2 > 0.8 or sim3 > 0.8 or sim4 > 0.8:
                continue
            
        cv2.imwrite("firstframe"+str(scene)+".png", frame)
        cv2.imwrite("secondframe"+str(scene)+".png", frame2)
        second = (float(time*2) / 24.0)
        timestamps.append(round(second))
        second = float(second)/60.0
        m,s = divmod(second, 1)
        s = s*60.0
        print ("Scene " + str(scene))
        # This is the moment in mm:ss in the video
        print ("Min " + str(int(second)) +" Sec "+ str(int(s)))
        print ("seconds "+str(second*60))
        print ("Sim "+str(sim))
        print (" ")
        scene = scene+1
        print (timestamps[:])

with open("list_timestamps_scenes", 'wb') as outfile:
    json.dump(timestamps, outfile)
