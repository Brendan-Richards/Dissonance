import FileStuff as fs
import matplotlib.pyplot as plt
import detect_peaks as dp
import GUI as g


def findSpectra():
    wavFiles = fs.getWavFiles()
    cutoff = .05
    mph = 0
    mpd = 3000
    low = 5000
    high = 240000

    params = [cutoff, mph, mpd, low, high, False]
    """
    params[0]: the amplitude value to ignore below
    params[1]: maximum peak height
    params[2]: minimum distance between peaks
    params[3]: minimum frequency for peak detection
    params[4]: maximum frequency for peak detection
    params[5]: boolean, answers "save the current graph?"
    """

    for i in range(len(wavFiles)):
        freqs, amps = fs.getAmpsAndFreqs(wavFiles[i])
        fs.saveData(freqs, amps, wavFiles[i])

        while True:
            # make spectrum plot
            peakFreqs, peakAmps = plotMaxima(freqs, amps, wavFiles[i], params)
            g.guiInit(params)
            if params[5]:
                params[5] = False
                fs.saveSpectra(peakFreqs, peakAmps, "partials/peak_freqs_" + wavFiles[i][:len(wavFiles[i]) -4], "partials/peak_amps_" + wavFiles[i][:len(wavFiles[i]) - 4])
                break


def plotMaxima(freqs, amps, filename, params):
    # Get current size
    fig_size = plt.rcParams["figure.figsize"]
    # Set figure width to 12 and height to 9
    fig_size[0] = 22
    fig_size[1] = 15
    plt.rcParams["figure.figsize"] = fig_size

    plt.title("Spectrum for: " + filename)
    plt.xlabel("Frequency[HZ]")
    plt.ylabel("Amplitude")
    plt.plot(freqs, amps)
    maxima = dp.detect_peaks(amps, mph=params[1], mpd=params[2], show=False, valley=False, cutoff=params[0], low=params[3], high=params[4])
    # maxima2 = fixPeaks(amps, maxima)
    # print("unadjusted maxima frequencies: ",end="")
    # print(maxima)
    peakAmps = []
    peakFreqs = []
    for x in maxima:
        a = amps[x]
        f = freqs[x]
        peakAmps.append(a)
        peakFreqs.append(f)
    # plot vertical lines for local maxima
    for i in range(len(peakFreqs)):
        plt.axvline(x=peakFreqs[i], color='r')
        plt.text(peakFreqs[i] - 80, .8, 'f = ' + str(peakFreqs[i]), rotation=90)
    plt.axhline(y=params[0], color='g')

    if not(params[5]):
        plt.show()
    else:
        plt.savefig(fs.myPath + "spectrum_plots_with_maxima/" + filename[:len(filename)-4] + ".png")
        params[5] = True
    plt.close()
    return peakFreqs, peakAmps


################################################################################
def fixPeaks(amps, result):
    width = 4800
    keep = []
    for i in range(len(result)):
        maxAmp = max(amps[result[i]-width:result[i]+width])
        keep.append(amps.index(maxAmp))
    return keep


def fixSpectraMaximaPlots():
    wavFiles = fs.getWavFiles()

    for i in range(len(wavFiles)):
        freqs, amps = fs.getAmpsAndFreqs(wavFiles[i])
        peakFreqs, peakAmps = fs.getPartials(wavFiles[i][:-4])

        # Get current size
        fig_size = plt.rcParams["figure.figsize"]
        # Set figure width to 12 and height to 9
        fig_size[0] = 22
        fig_size[1] = 15
        plt.rcParams["figure.figsize"] = fig_size

        plt.title("Spectrum for: " + wavFiles[i])
        plt.xlabel("Frequency[HZ]")
        plt.ylabel("Amplitude")
        plt.plot(freqs, amps)

        for j in range(len(peakFreqs)):
            plt.axvline(x=peakFreqs[j], color='r')
            plt.text(peakFreqs[j] - 80, .8, 'f = ' + str(peakFreqs[j]), rotation=90)

        plt.savefig(fs.myPath + "spectrum_plots_with_maxima2/" + wavFiles[i][:-4] + ".png")
        plt.close()
