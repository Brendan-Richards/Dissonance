
import numpy as np
import pyaudio
import time
import os

myPath = "C:/Users/Brendan/Dropbox/github/Dissonance/"

def makeSynths():

    wavFiles = getWavFiles()

    for i in range(1,len(wavFiles)):
        partialFreqs, partialAmps = getPartials(wavFiles[i])

        audio = synthesize( partialFreqs, partialAmps)

        saveSynth(audio)

# return a list of all the filenames in the given folder
def getWavFiles():
    return os.listdir(myPath + "Instrument_samples/")  # get a list of all the filenames of the audio files

def synthesize(freqs, amps):


    for i in range(len(freqs)):
        p = pyaudio.PyAudio()
        volume = amps[i]  # range [0.0, 1.0]
        sr = 44100  # sampling rate, Hz, must be integer
        duration = 5.0  # in seconds, may be float
        f = freqs[i]  # sine frequency, Hz, may be float

        # generate samples, note conversion to float32 array
        samples = (np.sin(2 * np.pi * np.arange(sr * duration) * f / sr)).astype(np.float32)

        # for paFloat32 sample values must be in range [-1.0, 1.0]
        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=sr,
                        output=True)

        # play. May repeat with different volume values (if done interactively)
        stream.write(volume * samples)
        stream.read(len(samples))

        stream.stop_stream()
        stream.close()

        p.terminate()

        time.sleep(3)


def saveSynth(audio):
    None

def getPartials(filename):
    freqs = []
    amps = []
    myFile1 = open(myPath + "partials/peak_freqs_" + filename[:len(filename)-4] + ".csv", 'r')
    for x in myFile1:
        freqs.append(float(x[:-3]))
    myFile1.close()

    myFile2 = open(myPath + "partials/peak_amps_" + filename[:len(filename)-4] + ".csv", 'r')
    for x in myFile2:
        amps.append(float(x[:-3]))
    myFile2.close()

    return freqs, amps

makeSynths()