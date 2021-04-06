#directory settings (pls change as necessary)
TRACKS = 100 #Number of tracks
GENRES = ["blues.", "classical.", "country.", "disco.", "hiphop.", "jazz.", "metal.", "pop.", "reggae.", "rock."]
DP = 5


## this program will find:

import pandas as pd
df = pd.DataFrame(columns = ["track no.", "genre", "average diff. peaks", "stdev"])
row={}



############# START OF CODES #############

#packages #define

import numpy as np

#misc functions (like file i/o)

def filenameTrackNo(num, dp, TYPE, aob, tags):
    numS = str(num)
    while (len(numS)<dp):
        numS = "0" + numS
    return aob + numS + tags + TYPE


#main function


for g in range(len(GENRES)): #cycle through all genres
    for NUM in range(TRACKS): #cycle through all tracks in genre

        row["track no."] = NUM
        row["genre"] = GENRES[g]
            
        if (g==5) and (NUM==54): #account for defective jazz54 track
            row["average diff. peaks"] = 0
            row["stdev"] = 0

        else:
            temp = []
            RMSes = np.loadtxt(filenameTrackNo(NUM, DP, ".txt", GENRES[g], "trackPeaks"))
            for i in range(len(RMSes)-2):
                temp.append(abs(RMSes[i]-RMSes[i+1]))
            row["average diff. peaks"] = np.mean(temp)
            row["stdev"] = np.std(temp)

        rowdf = pd.DataFrame(row, index = [i])
        df = pd.concat([df, rowdf], ignore_index=True)


pd.DataFrame(df).to_csv("gtzan change in loudness trackPeaks.csv")
