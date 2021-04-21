# pc3288-codes

Here are versions of the Python scripts used for the UROPS project, **Feature extraction of audio signals for music genre classification** (Jan-April 2021)

In general, the scripts would be stored in the same directory as the .wav files of the tracks. After running the scripts, .txt and/or .csv files would be generated, containing the calculated features.

The branches contain slightly different versions of the script:
- main: used on mono tracks of personal dataset (report section 3.2)
- song-dissection: used on mono tracks of personal dataset, mainly for varying segment and frame sizes (eg. track A and track B. report section 3.2)
- for-stereo: used on stereo tracks of personal dataset (ie. comparison of left and right channels. report section 3.2.1)
- gtzan-settings and gtzan-rms: used on GTZAN dataset (report section 3.3)

There are minor bugs and issues in the script, such as unit conversion/inconsistent naming. They were accounted for (ie. converted/processed outside of the scripts) before the final analysis.

Thanks for reading!
