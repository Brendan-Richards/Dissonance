import os
from scipy.io import wavfile as wav
import math
from scipy.fftpack import fft, fftfreq

myPath = "C:/Users/Brend/Dropbox/github/Dissonance/"

def saveData(freqs, amps, filename):
    myFile1 = open(myPath + "spectrum_plot_data/" + filename[:len(filename)-4] + "_freqs.csv", 'w')
    for x in freqs:
        myFile1.write(str(x) + ',\n')
    myFile1.close()

    myFile2 = open(myPath + "spectrum_plot_data/" + filename[:len(filename)-4] + "_amps.csv", 'w')
    for x in amps:
        myFile2.write(str(x) + ',\n')
    myFile2.close()

def saveSpectra(peakFreqs, peakAmps, filename1, filename2):
    myFile1 = open(myPath + filename1 + ".csv", 'w')
    for x in peakFreqs:
        myFile1.write(str(x) + ',\n')
    myFile1.close()

    myFile2 = open(myPath + filename2 + ".csv", 'w')
    for x in peakAmps:
        myFile2.write(str(x) + ',\n')
    myFile2.close()

# takes a filename and does an FFT on it
# returns a list of frequencies and corresponding amplitudes
def getAmpsAndFreqs(file):
    print("doing FFT for: " + file)
    freqs, amps = doFFT(file)
    return freqs, amps

# opens the audio file given by fn
# and does the fft on it
# returns the list of amplitudes and frequencies for that file
def doFFT(file):

    # the audio file is expected to be mono
    sr, data = wav.read(myPath + "Instrument_samples/" + file)
    powOf2(data)
    L = len(data) / 2  # you only need half of the fft list (it mirrors to the right)
    p = abs(fft(data)[:(L - 1)])  # get the list of power values
    a = [math.sqrt(x) for x in p]  # get amplitudes from power spectrum
    a = normalize(a)  # normalize the amplitudes
    f = list(fftfreq(data.size, 1 / sr)[:(L - 1)])  # get the list of frequencies

    return f, a

# takes a list of amplitudes and divides the whole list by the largest value in the list
# normalizes the highest amplitude to 1
def normalize(amps):
    best = amps[0]
    for i in range(len(amps)):
        if best < amps[i]:
            best = amps[i]

    return [x / best for x in amps]

# pad zeroes onto a numpy array called data to make its length a power of 2
def powOf2(data):
    n = pow(2, math.ceil(math.log(float(data.shape[0])) / math.log(float(2))))
    data.resize((n,), refcheck=False)

# return a list of all the filenames in the given folder
def getWavFiles():
    return os.listdir(myPath + "Instrument_samples/")  # get a list of all the filenames of the audio files

def getSmoothed(fileName):
    temp = []
    myFile1 = open(myPath + '/smoothed_data/' + fileName, 'r')
    for x in myFile1:
        temp.append(float(x))
    myFile1.close()

    return temp
