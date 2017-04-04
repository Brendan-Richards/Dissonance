# create a synthetic 'sine wave' wave file with
# set frequency and length
# tested with Python 2.5.4 and Python 3.1.1 by vegaseat
# code taken from: https://www.daniweb.com/programming/software-development/code/263775/create-a-synthetic-sine-wave-wave-file
import math
import wave
import struct
import FileStuff as fs

def make_soundfile(freqs, amps, data_size=10000, fname="test.wav"):
    """
    create a synthetic 'sine wave' wave file with frequency freq
    file fname has a length of about data_size * 2
    """
    frate = 44000.0  # framerate as a float
    amp = 8000.0     # multiplier for amplitude
    # make a sine list ...
    sine_list = []
    for x in range(data_size):
        val = 0.0
        for i in range(len(freqs)):
            val += amps[i]*math.sin(2*math.pi*freqs[i]*(x/frate))
        sine_list.append(val)
    # get ready for the wave file to be saved ...
    wav_file = wave.open(fs.myPath + "synth_recreations/" + fname + ".wav", "w")
    # give required parameters
    nchannels = 1
    sampwidth = 2
    framerate = int(frate)
    nframes = data_size
    comptype = "NONE"
    compname = "not compressed"
    # set all the parameters at once
    wav_file.setparams((nchannels, sampwidth, framerate, nframes,
        comptype, compname))
    # now write out the file ...
    print( "may take a moment ..." )
    for s in sine_list:
        # write the audio frames to file
        wav_file.writeframes(struct.pack('h', int(s*amp/2)))
    wav_file.close()
    print( "%s written" % fname )



def makeAllSynths():
    wavFiles = fs.getWavFiles()
    for i in range(len(wavFiles)):
        freqs, amps = fs.getPartials(wavFiles[i][:-4])
        make_soundfile(freqs, amps, 90000, wavFiles[i][:-4])

# flist = [440, 880, 1320, 1760, 2200, 2640]
# amplist = [1, .21666, .119116, .096164, .085033, .076539]
#
#
# make_soundfile(flist, amplist, 90000, "WaveTest2.wav")