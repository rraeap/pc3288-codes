#directory settings (pls change as necessary)
TRACKS = 1 #Number of tracks
GENRE = ""
DP = 2

## this program will find:

import pandas as pd
df = pd.DataFrame(columns = ["average rms", "largest rms", "smallest rms", "diff. in energy", "% of low energy", "stdev", "segment duration (s)", "N"])
row={}

#based on the following settings of:

#segment settings to be tested:
DURATIONS = [0.5,1,2,3,4,5]
DURATIONS_str = ["0.5", "1", "2", "3", "4", "5"]
OVERLAP = 0.5


############# START OF CODES #############

#packages #define

from scipy.io import wavfile
import numpy as np

SAMPLERATE = 48000
BYTES = 4

#misc functions (like file i/o)

def filenameTrackNo(num, dp, TYPE, aob, tags):
    numS = str(num)
    while (len(numS)<dp):
        numS = "0" + numS
    return aob + numS + tags + TYPE

#function defs and #define for dBFS conversion

from math import log10

MAXAMPLITUDE = 2**15 #16-bit PCM .wav encoding
EPSILON = 0.000001 #arbituary value close to zero, to protect input to log function

def dBFS(amplitude, MAXAMPLITUDE, EPSILON):
    v = abs(float(amplitude)/float(MAXAMPLITUDE)) + EPSILON
    return 20*log10(v)

def dBFS_array(amplitudes, MAXAMPLITUDE, EPSILON):
    v = []
    v_i = 0
    for i in range(len(amplitudes)):
        v_i = abs(float(amplitudes[i])/float(MAXAMPLITUDE)) + EPSILON
        v.append(20*log10(v_i))
    return v

#loudness features function defs:

from audioop import rms

def track_RMS(track, DURATION, SAMPLERATE, OVERLAP): #long term feature, traverse the whole track
    arr = [] #declare array to store RMS of each segment
    
    #set starting point
    ALLOWANCE = 2
    trackStart = ALLOWANCE*SAMPLERATE
    segmentSize = DURATION*SAMPLERATE
    
    #"visit" all segments
    for segmentStart in range(trackStart, len(track)-int(ALLOWANCE*SAMPLERATE), int(DURATION*SAMPLERATE*OVERLAP)):
        seg = track[segmentStart:int(segmentStart+DURATION*SAMPLERATE)]
        arr.append(rms(seg, BYTES))
    
    return arr


def percentageLow(trackPeaks): #input array containing all track peaks
    #code
    trackPeak_ave = np.mean(trackPeaks)
    percentageL = np.where(trackPeaks<trackPeak_ave, 1, 0)
    return percentageL

def percentageLow_value(trackPeaks):
    PL = percentageLow(trackPeaks)
    return sum(PL)/len(PL)


############ feature extractor ############

def extracting(num, DURATION, OVERLAP, SAMPLERATE, MAXAMPLITUDE, EPSILON):
#import track
    z, track = wavfile.read(filenameTrackNo(num, DP, ".wav", "", ""))
# FIND PEAKS
    return track_RMS(track, DURATION, SAMPLERATE, OVERLAP)


############## END OF DEFINITIONS ##############



############ EXCECUTION OF CODE ############

for m in range(len(DURATIONS)):
    row["segment duration (s)"] = DURATIONS_str[m]
    DURATION = DURATIONS[m]

    for i in range(TRACKS):
        trackPeaks = [] #reset track before loop
        trackPeaks = extracting(i+1, DURATION, OVERLAP, SAMPLERATE, MAXAMPLITUDE, EPSILON)
       
        #find features, update table
        ave = np.mean(trackPeaks)
        large = np.max(trackPeaks)
        small = np.min(trackPeaks)
        percentageL = percentageLow_value(trackPeaks)
        row["average rms"] = ave
        row["largest rms"] = large
        row["smallest rms"] = small
        row["diff. in energy"] = large-small
        row["% of low energy"] = percentageL
        row["stdev"] = np.std(trackPeaks)
        row["N"] = len(trackPeaks)
        rowdf = pd.DataFrame(row, index = [i])
        df = pd.concat([df, rowdf], ignore_index=True)
        #export trackPeaks array
        np.savetxt(filenameTrackNo(i+1, DP, ".txt", GENRE, DURATIONS_str[m] + " trackRMS"), trackPeaks)


# FILE I/O: export findings
pd.DataFrame(df).to_csv(GENRE + "loudness features - RMS.csv") #please input the relevant array and desired file name
