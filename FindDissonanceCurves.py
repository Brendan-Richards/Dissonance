import math
import FileStuff as fs
import csv
import matplotlib.pyplot as plt

# each Timbre object has a list of frequencies and a corresponding list of amplitudes
class Timbre:
    def __init__(self, c, d):
        self.freq = c
        self.amp = d

    # shifts all the frequencies in this Timbre by a
    def shift(self, a):
        l = []
        for i in range(len(self.freq)):
            l.append(self.freq[i]*a)

        return Timbre(l, self.amp)



# implementation of equation 2 from Sethares
# calculates the dissonance between two frequencies f1 and f2 with amplitudes v1 and v2
def d(f1, f2, v1, v2):
    a = 3.5
    b = 5.75
    s1 = 0.021
    s2 = 19
    dMax = 0.24
    v12 = v1*v2
    s = dMax/(s1*f1+s2) # equation 3 from Sethares
    diff = math.fabs(f2-f1)

    return v12*(math.exp(-1*a*s*diff) - math.exp(-1*b*s*diff))

# implementation of equation 5 from Sethares
# calculates the dissonance of one timbre t with its own overtones
def Dt(t):
    total = 0
    for i in range(len(t.freq)):
        for j in range(len(t.freq)):
            total += d(t.freq[i], t.freq[j], t.amp[i], t.amp[j])

    return .5 * total

# implementation of equation 6 from Sethares
# returns the total dissonance between two timbres t and a*t
def D(t, a):
    t2 = t.shift(a)
    total = 0
    for i in range(len(t.freq)):
        for j in range(len(t.freq)):
            total += d(t.freq[i], t2.freq[j], t.amp[i], t2.amp[j])

    return Dt(t) + Dt(t2) + total

# takes args freqs and amps which are the frequencies and amplitudes of a set of partials
# returns a list of x values and a list of y values for a dissonance curve
def getDissonanceCurve(freqs, amps):
    t = Timbre(freqs, amps)
    x = []
    y = []
    dx = .001
    xMax = 2.2
    a = 1 # the frequency ratio

    for i in range(int((xMax-a)/dx)):
        x.append(a)
        y.append(D(t, a))
        a += dx

    return x, y


def findCurves():
    wavFiles = fs.getWavFiles()

    for i in range(len(wavFiles)):
        amps = []
        freqs = []
        print("making dissonance curve for: " + wavFiles[i])

        name = fs.myPath + "partials/peak_freqs_" + wavFiles[i][:len(wavFiles[i])-4] + ".csv"
        file = open(name, 'r')
        reader = csv.reader(file)
        for row in reader:
            freqs.append(float(row[0]))

        name = fs.myPath + "partials/peak_amps_" + wavFiles[i][:len(wavFiles[i]) - 4] + ".csv"
        file = open(name, 'r')
        reader = csv.reader(file)
        for row in reader:
            amps.append(float(row[0]))

        xVals, yVals = getDissonanceCurve(freqs, amps)

        plt.plot(xVals, yVals)
        plt.title("Dissonance Curve for: " + wavFiles[i])
        plt.xlabel("Frequency Ratio")
        plt.ylabel("Dissonance")

        # Get current size
        fig_size = plt.rcParams["figure.figsize"]
        # Set figure width to 22 and height to 15
        fig_size[0] = 22
        fig_size[1] = 15
        plt.rcParams["figure.figsize"] = fig_size

        plt.savefig(fs.myPath + "dissonance_curves/" + wavFiles[i][:len(wavFiles[i])-4] + ".png")
        # plt.show()
        plt.close()


def findOneCurve(freqs, amps, fileName):
    freqs, amps = getDissonanceCurve(freqs, amps)

    plt.plot(freqs, amps)
    plt.title("Dissonance Curve for: " + fileName)
    plt.xlabel("Frequency Ratio")
    plt.ylabel("Dissonance")
    # plt.savefig(fs.myPath + "all_dissonance_curves/" + fileName + ".png")
    plt.show()
    plt.close()