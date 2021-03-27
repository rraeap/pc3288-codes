## COMBINE SPECTRAL FLUX AND SPECTRAL SHAPE FEATURES codes. bc might as well. (see other branches)

#directory settings (change as necessary)
TRACKS = 0 #number of tracks
GENRE = ""

#this program will find:

import pandas as pd
df = pd.DataFrame(columns = ["average spec.flux", "greatest spec.flux", "smallest spec.flux", "stdev", "N"])
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

def centroid(y, FREQBINS, FRAMESIZE, SAMPLERATE): #y = abs(FF.rfft(frameArr))
    centroid = np.sum(y*FREQBINS)/np.sum(y)
    return centroid
  
def rolloff(y, FREQBINS, FRAMESIZE, SAMPLERATE):
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
  
#! spectral slope

def slope(y):
  #i think it's just a LLS fit of the spectrum then return the gradient or intercept idk
  specSlope = 0
  return specSlope


#spectral flux function defs:

def spectralFlux(segment, start, FRAMESIZE):
    frame1 = frame(segment, start, FRAMESIZE)
    frame2 = frame(segment, start+FRAMESIZE, FRAMESIZE)
    freqComponents1 = abs(FF.rfft(frame1))
    freqComponents2 = abs(FF.rfft(frame2))
    return abs(sum(freqComponents1)/max(freqComponents1)-sum(freqComponents2)/max(freqComponents2))

def segment_spectralFlux(segment, FRAMESIZE, overlap):
    N = len(segment)
    start = 0 #start at first sample
    arr = [0] #initialize array
    #some loop control, to cycle through the whole segment
    while(start <= N-2*FRAMESIZE):
        if (start == 0):
            arr[0] = spectralFlux(segment, start, FRAMESIZE)
        else:
            arr.append(spectralFlux(segment, start, FRAMESIZE))
        start += int(FRAMESIZE*overlap) #set new starting point
    return arr #arr storing all the flux values


############ feature extractor ############

def extracting(num, GENRE): #input track number (int) and genre (genre can be NULL too ofc.)
    #import file
    z, track = wavfile.read(filenameTrackNo(num, 2, ".wav", GENRE,"")) #assumes .wav uses MONO channel
    return track


#delete the other extracting def later
def extracting(num, SAMPLERATE, FRAMESIZE, OVERLAP): #input track number (int)
    #import file
    z, track = wavfile.read(filenameTrackNo(num, 2, ".wav", "","")) #assumes .wav uses MONO channel
    
    #cut segment and find qty: specFlux
    seg = segment(track, SAMPLERATE)
    qty = segment_spectralFlux(seg, FRAMESIZE, OVERLAP) #change the RHS as required
    
    #note info, then export qty to .txt (change as necessary)
    aob = "[specFlux-" + "fr" + str(FRAMESIZE) +"] track"
    np.savetxt(filenameTrackNo(num, 2, ".txt", aob, ""), qty)
    return qty


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
    specFluxes = []
    
    N = 0 #number of frames. 
    
    frameNo = 0
    while (frameNo*FRAMESIZE <= len(trackLPCM)-FRAMESIZE):
        #get FFT of current frame
        frameCurrent = frame(trackLPCM, frameNo*FRAMESIZE, FRAMESIZE)
        frameCurrent_FFT = abs(FF.rfft(frameCurrent))
           
        #find and store centroid, rolloff, and slope of current frame
        
        #if frame is not first frame,
        if framePrevious_FFT != []:
            #compare spectra for current and previous frame to get spec flux.
            
        #store data in df, export to .txt
        
        framePrevious_FFT = frameCurrent_FFT
        N += 1
    
  
    
# FILE I/O: export findings    
pd.DataFrame(df).to_csv(GENRE + " spectral flux.csv") #please input the relevant array and desired file name
