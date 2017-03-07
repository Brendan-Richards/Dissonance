import matplotlib.pyplot as plt
import math
import numpy as np
from scipy.fftpack import fft, fftfreq
from scipy.io import wavfile as wav
import os
import FindDissonanceCurves as dc

# takes a list of x and y values and returns the local minima of the graph
def findLocalMinima(x, y):
    m = []
    for i in range(len(y)):
        if i == 0 or i == len(y)-1:
            continue
        else:
            if y[i-1] > y[i] and y[i] < y[i+1]:
                m.append(x[i])

    return m

# take a filename fn and return a list of freqencies and a list of corresponding amplitues
def getValues(fn):
    sr, d = wav.read(fn)
    a = []
    for i in range(len(d)):
        a.append(d[i][0])
    print(a)
    return a

# take the list of x and y values and make a plot
# l is a boolean that tells whether to draw lines at the local minima or not
# h is a boolean that tells whether to draw lines at the local maxma or not
def makePlot(plotTitle, xVal, xLabel, yVal, yLabel, l, h, saveLocation):
    plt.plot(xVal, yVal)

    if l:
        minima = findLocalMinima(xVal, yVal)

        # plot vertical lines for local minima
        for i in range(len(minima)):
            plt.axvline(x=minima[i], color='r')

        print("the curve's minima: ", minima)

    elif h:
        maxima = findPeaks(xVal, yVal)

        # plot vertical lines for local minima
        for i in range(len(maxima)):
            plt.axvline(x=maxima[i], color='r')
            plt.text(maxima[i]-80, .8, 'f = ' + str(maxima[i]), rotation=90)

        print("the curve's maxima: ", maxima)

    plt.title(plotTitle)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.savefig(saveLocation + plotTitle[22:] + ".jpg")
    # plt.show()
    plt.close()

# takes a list of amplitudes and divides the whole list by the largest value in the list
# normalizes the highest amplitude to 1
def normalize(a):
    best = a[0]
    for i in range(len(a)):
        if best < a[i]:
            best = a[i]

    return [x / best for x in a]

# opens the audio file given by fn
# and does the fft on it
# returns the list of amplitudes and frequencies for that file
def doFFT(fn, myPath):
    # the audio file is expected to be mono
    sr, dat = wav.read(myPath + fn)
    powOf2(dat)
    L = len(dat) / 2  # you only need half of the fft list (it mirrors to the right)
    p = abs(fft(dat)[:(L - 1)])  # get the list of power values
    a = [math.sqrt(x) for x in p]  # get amplitudes from power spectrum
    a = normalize(a)  # normalize the amplitudes
    f = fftfreq(dat.size, 1 / sr)[:(L - 1)]  # get the list of frequencies

    return f, a

# pad zeroes onto a numpy array called dat to make its length a power of 2
def powOf2(dat):
    n = pow(2, math.ceil(math.log(float(dat.shape[0])) / math.log(float(2))));
    dat.resize((n,), refcheck=False)

# takes a list of amplitudes a and list of frequencies f
# attempts to find the peaks in the list of data
def findPeaks(freqs, amps):
    width = 5000
    cutoff = .3
    maxZeros = 10
    skew = 30
    temp = list(amps)
    peakFreqs = []
    peakAmps = []

    for i in range(len(temp)):
        if temp[i] < cutoff:
            temp[i] = 0

    nextStart = 0
    for i in range(int(len(temp)/width)):
        start = None
        end = None
        zeroCount = 0
        for j in range(width):
            curr = j + i*width
            if curr < nextStart:
                continue
            if temp[curr] != 0:
                zeroCount = 0
                if start == None:
                    start = curr
            elif temp[curr] == 0 and start != None:
                if zeroCount >= maxZeros:
                    end = curr
                    break
                else:
                    zeroCount += 1
        if start != None and end != None:
            mid = int((end-start)/2) + curr
            peakFreqs.append(freqs[mid-skew])
            peakAmps.append(amps[mid-skew])
            nextStart = end

    return peakFreqs, peakAmps

##############################################################################################
##############################################################################################
def getAmpsAndFreqs(files, myPath):
    allAmps = []
    allFreqs = []
    for i in range(len(files)):
        print("printing stuff for:" + files[i])
        freqs, amps = doFFT(files[i], myPath)
        allAmps.append(amps)
        allFreqs.append(freqs)
        # np.savetxt("C:/Users/Brendan/Dropbox/Python projects/dissonance/spectrum_plot_data/" + files[i][:len(files[i])-4] + "_amplitudes.csv", amps, fmt="%10.5f", delimiter=', ')
        # np.savetxt("C:/Users/Brendan/Dropbox/Python projects/dissonance/spectrum_plot_data/" + files[i][:len(files[i])-4] + "_frequencies.csv", freqs, fmt="%10.5f", delimiter=', ')

    # for i in range(len(allAmps)):
    #     makePlot("Frequency Spectrum for " + files[i][:len(wavFiles[i])-4], allFreqs[i],"Frequencies[Hz]", allAmps[i], "Amplitudes", False)

    return allFreqs, allAmps


def findAllPeaks(allFreqs, allAmps):
    allPeakFreqs = []
    allPeakAmps = []
    for i in range(len(allAmps)):
        f, a = findPeaks(allFreqs[i], allAmps[i])
        allPeakFreqs.append(f)
        allPeakAmps.append(a)

    return allPeakFreqs, allPeakAmps

def getAllDissonanceCurves(wavFiles, allPeakFreqs, allPeakAmps, saveLoc):

    for i in range(len(wavFiles)):
        myFreqs = allPeakFreqs[i]
        myAmps = allPeakAmps[i]

        t = Timbre(myFreqs, myAmps)

        xVals, yVals = getCurve(t)

        makePlot("Dissonance Curve for: " + wavFiles[i], xVals, "Frequency Ratio", yVals, "Dissonance", False, False, saveLoc)

def getAllDissonanceCurvesAndMaxima(wavFiles, allPeakFreqs, allPeakAmps, saveLoc):

    for i in range(len(wavFiles)):
        myFreqs = allPeakFreqs[i]
        myAmps = allPeakAmps[i]

        t = Timbre(myFreqs, myAmps)

        xVals, yVals = getCurve(t)

        makePlot("Dissonance Curve for: " + wavFiles[i], xVals, "Frequency Ratio", yVals, "Dissonance", False, True, saveLoc)


def saveSpectra(freqs, amps, fileNames, fPath):
    None


def testFindPeaks():
    myPath = "C:/Users/Brendan/Dropbox/Python projects/dissonance/Instrument_samples/"
    filename = "Accordion_01.wav"
    freqs, amps = doFFT(filename, myPath)

    makePlot("Frequency Spectrum for " + filename, freqs, "Frequencies[Hz]", amps,
             "Amplitudes", False, True)

##########################
#### main program code####
##########################

def mainRoutine():

    myPath = "C:/Users/Brendan/Dropbox/Python projects/dissonance/"
    wavFiles = os.listdir(myPath + "Instrument_samples/")  # get a list of all the filenames of the audio files
    allFrequencies, allAmplitudes = getAmpsAndFreqs(wavFiles, myPath + "Instrument_samples/")

    allPeakFreqs, allPeakAmps = findAllPeaks(allFrequencies, allAmplitudes)

    saveSpectra(allPeakFreqs, allPeakAmps, wavFiles, myPath + "partials/")

    getAllDissonanceCurves(wavFiles, allPeakFreqs, allPeakAmps, myPath + "dissonance_curves/")
    getAllDissonanceCurvesAndMaxima(wavFiles, allPeakFreqs, allPeakAmps, myPath + "dissonance_curves_and_maxima/")


mainRoutine()

# testFindPeaks()

