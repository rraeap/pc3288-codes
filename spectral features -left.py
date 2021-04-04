#directory settings (change as necessary)
TRACKS = 0 #number of tracks
GENRE = ""
DP = 2 #number of decimal places for track

#this program will find:

import pandas as pd
df = pd.DataFrame(columns = ["ave. centroid", "centroid stdev", "ave. rolloff", "rolloff stdev", "ave. spec.flux", "spec.flux stdev", "channel", "N"])
row={}

#based on the following settings of:

#segment settings: no segmentation. to vary after getting results and check what is a suitable length to be used as "texture window" 

#frame settings:
FRAMESIZE = 2**10 #~20ms per frame
OVERLAP = 0.5


############# START OF CODES #############

#include #define

from scipy.io import wavfile
import numpy as np
import scipy.fft as FF

SAMPLERATE = 48000

#misc functions (like file i/o)

def filenameTrackNo(num, dp, TYPE, aob, tags):
    numS = str(num)
    while (len(numS)<dp):
        numS = "0" + numS
    return aob + numS + tags + TYPE

#function defs for frame making (short-term features)

FREQBINS = abs(FF.rfftfreq(FRAMESIZE, 1/SAMPLERATE)) 

def frame(segment, startpt, FRAMESIZE):
    return segment[startpt:startpt+FRAMESIZE]*np.hanning(FRAMESIZE)

def segment(track, SAMPLERATE): # this version just scans the entire track. cut into segments manually on excel or otherwise
    
    #start from start of track
    ALLOWANCE = 2 #allowance in case of silence from recording
    start = ALLOWANCE * SAMPLERATE
    
    #create segment
    seg = track[start:len(track)-start]
    return seg

#spectral shape features function defs:

def centroid(y, FREQBINS): #y = abs(FF.rfft(frameArr))
    centroid = np.sum(y*FREQBINS)/np.sum(y)
    return centroid
  
def rolloff(y, FREQBINS):
    PERCENTAGE = 0.85
    rolloff = 0
    cutoffSum = np.sum(y*FREQBINS) * PERCENTAGE
    #sum from first bin to last bin until hit cutoffSum. then return rolloff frequency
    cu = 0 #i cant rmb the real name for the cummulative thing but anw
    binNo = 0
    while(cu<cutoffSum):
        cu = cu + FREQBINS[binNo]*y[binNo]
        binNo = binNo + 1
    return FREQBINS[binNo]
 
def specFlux(y1, y0):
    return abs(sum(y1)/max(y1)-sum(y0)/max(y0))

# track importer

def extracting(num, GENRE): #input track number (int) and genre (genre can be NULL too ofc.)
    #import file
    z, channels = wavfile.read(filenameTrackNo(num, DP, ".wav", GENRE,"")) #assumes .wav uses MONO channel
    track = [:0] #left channel
    return track


############## END OF DEFINITIONS ##############



############ EXCECUTION OF CODE ############

for NUM in range(1, TRACKS+1):
    # arrays for "raw" track/spectra
    trackLPCM = [] # should be a good idea
    trackLPCM = segment(extracting(NUM, GENRE), SAMPLERATE)
    frameFFTs = []
    
    frameCurrent_FFT = []
    framePrevious_FFT = []
    
    #arrays for features across all frames
    centroids = []
    rolloffs= []
    specFluxes = []
    
    N = 0 #count number of frames. 
    frameStart = 0
    
    while (frameStart <= len(trackLPCM)-FRAMESIZE):
        #get FFT of current frame
        frameCurrent = frame(trackLPCM, frameStart, FRAMESIZE)
        frameCurrent_FFT = abs(FF.rfft(frameCurrent))
           
        #find and store centroid, and rolloff of current frame
        frameCentroid = centroid(frameCurrent_FFT, FREQBINS)
        centroids.append(frameCentroid)
        frameRolloff = rolloff(frameCurrent_FFT, FREQBINS)
        rolloffs.append(frameRolloff)
        
        frameSpecFlux = 0
        #if frame is not first frame,
        if framePrevious_FFT != []:
            #compare spectra for current and previous frame to get spec flux.
            frameSpecFlux = specFlux(frameCurrent_FFT, framePrevious_FFT)
            specFluxes.append(frameSpecFlux)
            
        #necessary updates
        framePrevious_FFT = frameCurrent_FFT
        N += 1
        
        #go to next frame
        frameStart += int(FRAMESIZE*OVERLAP)
        ##end while
    
    
    #export to .txt
    np.savetxt(filenameTrackNo(NUM, DP, ".txt", GENRE, "centroids -left"), centroids)
    np.savetxt(filenameTrackNo(NUM, DP, ".txt", GENRE, "rolloffs -left"), rolloffs)
    np.savetxt(filenameTrackNo(NUM, DP, ".txt", GENRE, "specFluxes -left"), specFluxes)
    
    #update track's average features in df table
    row["ave. centroid"] = np.mean(centroids)
    row["centroid stdev"] = np.std(centroids)
    row["ave. rolloff"] = np.mean(rolloffs)
    row["rolloff stdev"] = np.std(rolloffs)
    row["ave. spec.flux"] = np.mean(specFluxes)
    row["spec.flux stdev"] = np.std(specFluxes)
    row["channel"] = "left"
    row["N"] = N
    rowdf = pd.DataFrame(row, index = [NUM])
    df = pd.concat([df, rowdf], ignore_index=True)
        
    #end of loop. go to next track.
    
    
# FILE I/O: export findings    
pd.DataFrame(df).to_csv(GENRE + "spectral features -left.csv") #please input the relevant array and desired file name
