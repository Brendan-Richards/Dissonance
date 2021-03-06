import os
from scipy.io import wavfile as wav
import math
from scipy.fftpack import fft, fftfreq
from pydub import AudioSegment

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

def getDoubleAmpsAndFreqs(file):
    print("doing FFT for: " + file)
    freqs, amps = doDoubleFFT(file)
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

def doDoubleFFT(file):

    # the audio file is expected to be mono
    sr, data = wav.read(myPath + "combined_sounds/" + file)
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

def getDoubleWavFiles():
    return os.listdir(myPath + "combined_sounds/")  # get a list of all the filenames of the combined audio files


def getSmoothed(fileName):
    temp = []
    myFile1 = open(myPath + '/smoothed_data/' + fileName, 'r')
    for x in myFile1:
        temp.append(float(x))
    myFile1.close()

    return temp


def saveDissonanceVals(yVals, fileName):
    myFile1 = open(myPath + 'dissonance_curve_data/' + 'dissonance_curve_data_for_' + fileName + ".csv", 'w')
    for x in yVals:
        myFile1.write(str(x) + ",\n")
    myFile1.close()

def getDissonanceVals(fileName):
    temp = []
    myFile1 = open(myPath + 'dissonance_curve_data/' + 'dissonance_curve_data_for_' + fileName + ".csv", 'r')
    for x in myFile1:
        temp.append(float(x[:-3]))
    myFile1.close()
    return temp

def getPartials(filename):
    freqs = []
    amps = []
    myFile1 = open(myPath + 'partials/' + 'peak_freqs_' + filename + ".csv", 'r')
    for x in myFile1:
        freqs.append(float(x[:-3]))
    myFile1.close()

    myFile2 = open(myPath + 'partials/' + 'peak_amps_' + filename + ".csv", 'r')
    for x in myFile2:
        amps.append(float(x[:-3]))
    myFile1.close()

    return freqs, amps


def combineSounds(files):
    for i in range(1,len(files)):
        for j in range(1,len(files)):
            if os.path.exists(myPath + "combined_sounds/" + files[i][:-4] + " and " + files[j]) or os.path.exists(myPath + "combined_sounds/" + files[j][:-4] + " and " + files[i]) or files[i] == files[j]:
                continue

            sound1 = AudioSegment.from_file(myPath + "/instrument_samples/" + files[i])
            sound2 = AudioSegment.from_file(myPath + "/instrument_samples/" + files[j])

            combined = sound1.overlay(sound2)

            combined.export(myPath + "combined_sounds/" + files[i][:-4] + " and " + files[j], format='wav')