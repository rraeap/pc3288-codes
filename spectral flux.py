from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
import scipy.fft as FF

SAMPLERATE = 48000


#FUNCTION DEFINITIONS

def frame(segment, startpt, FRAMESIZE):
    return segment[startpt:startpt+FRAMESIZE]*np.hanning(FRAMESIZE)

def segment(track, DURATION, SAMPLERATE): #take segment from middle of song. 
    
    #set starting point
    start = int(len(track)/2 + DURATION*SAMPLERATE/2)
    
    #find suitable binary exponent
    n = 1
    while 2**n <= DURATION*SAMPLERATE:
        n = n+1
    
    #create segment
    seg = track[start:2**n+start]
    return seg


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


def filenameTrackNo(num, dp, TYPE, aob, tags):
    numS = str(num)
    while (len(numS)<dp):
        numS = "0" + numS
    return aob + numS + tags + TYPE


def extracting(num, DURATION, SAMPLERATE, FRAMESIZE, OVERLAP): #input track number (int)
    #import file
    z, track = wavfile.read(filenameTrackNo(num, 2, ".wav", "","")) #assumes .wav uses MONO channel
    
    #cut segment and find qty: specFlux
    seg = segment(track, DURATION, SAMPLERATE)
    qty = segment_spectralFlux(seg, FRAMESIZE, OVERLAP) #change the RHS as required
    
    #note info, then export qty to .txt (change as necessary)
    aob = "[specFlux-""fr"+str(FRAMESIZE)+" NORM] track"
    np.savetxt(filenameTrackNo(num, 2, ".txt", aob, ""), qty)
    return qty




##### RUNNING THE CODE #####

#segment settings/parameters. change as necessary. 
DURATION = 20 #in seconds
FRAMESIZE = 2**10 #~20ms per frame
OVERLAP = 0.5

#directory settings
TRACKS = 2
GENRE = "trial run WITH normalization"


import pandas as pd
df = pd.DataFrame(columns = ["average spec.flux", "greatest spec.flux", "smallest spec.flux", "stdev", "N"])
row={}


for NUM in range(1, TRACKS+1):
    specFluxes = []
    specFluxes = extracting(NUM, DURATION, SAMPLERATE, FRAMESIZE, OVERLAP) #extracting will save qty as .txt in directory.
    #exporting to dataframe
    ave = np.mean(specFluxes)
    large = np.max(specFluxes)
    small = np.min(specFluxes)
    row["average spec.flux"] = ave
    row["greatest spec.flux"] = large
    row["smallest spec.flux"] = small
    row["stdev"] = np.std(specFluxes)
    row["N"] = len(specFluxes)
    rowdf = pd.DataFrame(row, index = [NUM])
    df = pd.concat([df, rowdf], ignore_index=True)

    #idk if I wanna do a pyplot but nvm think about it later lol
    #nts: specFluxes array is alr outputted in the extracting() function

pd.DataFrame(df).to_csv(GENRE + " spectral flux.csv") #please input the relevant array and desired file name





    
