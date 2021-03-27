#directory settings (pls change as necessary)
TRACKS = 0 #Number of tracks
GENRE = ""
DP = 5

## this program will find:

import pandas as pd
df = pd.DataFrame(columns = ["average peak", "largest peak", "smallest peak", "loudness range", "% of low energy", "stdev", "N"])
row={}

#based on the following settings of:

#segment settings
DURATION = 3
OVERLAP = 0.5


############# START OF CODES #############

#packages #define

from scipy.io import wavfile
import numpy as np

SAMPLERATE = 48000

#misc functions (like file i/o)

def filenameTrackNo(num, dp, TYPE, aob, tags):
    numS = str(num)
    while (len(numS)<dp):
        numS = "0" + numS
    return aob + numS + tags + TYPE

#function defs and #define for dBFS conversion

from math import log10

MAXAMPLITUDE = 2**31 #32-bit PCM .wav encoding
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

def track_segmentPeaks(trackFromWav, DURATION, SAMPLERATE, OVERLAP): #long term feature (ie. segment peaks), traverse the whole track
    arr = [] #declare array to store peaks
    
    #set starting point
    ALLOWANCE = 0 #no need allowance for gtzan
    trackStart = ALLOWANCE*SAMPLERATE
    segmentSize = DURATION*SAMPLERATE
    
    #convert from LPCM to dBFS
    track = dBFS_array(trackFromWav, 2**31, 0.000001) #zz python y no #define and no globals://

    #"visit" all segments
    for segmentStart in range(trackStart, len(track)-ALLOWANCE*SAMPLERATE, int(DURATION*SAMPLERATE*OVERLAP)):
        arr.append(max(track[segmentStart:(segmentStart+DURATION*SAMPLERATE)]))
    
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
    return track_segmentPeaks(track, DURATION, SAMPLERATE, OVERLAP)


############## END OF DEFINITIONS ##############



############ EXCECUTION OF CODE ############

for i in range(TRACKS):
    trackPeaks = [] #reset track before loop
    trackPeaks = extracting(i+1, DURATION, OVERLAP, SAMPLERATE, MAXAMPLITUDE, EPSILON)
   
    #find features, update table
    ave = np.mean(trackPeaks)
    large = np.max(trackPeaks)
    small = np.min(trackPeaks)
    percentageL = percentageLow_value(trackPeaks)
    row["average peak"] = ave
    row["largest peak"] = large
    row["smallest peak"] = small
    row["loudness range"] = large-small
    row["% of low energy"] = percentageL
    row["stdev"] = np.std(trackPeaks)
    row["N"] = len(trackPeaks)
    rowdf = pd.DataFrame(row, index = [i])
    df = pd.concat([df, rowdf], ignore_index=True)
    #export trackPeaks array
    np.savetxt(filenameTrackNo(i+1, DP, ".txt", GENRE, "trackPeaks"), trackPeaks)


# FILE I/O: export findings
pd.DataFrame(df).to_csv(GENRE + "loudness features.csv") #please input the relevant array and desired file name




