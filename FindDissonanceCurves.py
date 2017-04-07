import math
import FileStuff as fs
import csv
import matplotlib.pyplot as plt
import os

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
def D(t1, t2, a):
    t3 = t2.shift(a)
    total = 0
    for i in range(len(t1.freq)):
        for j in range(len(t2.freq)):
            total += d(t1.freq[i], t3.freq[j], t1.amp[i], t3.amp[j])

    return Dt(t1) + Dt(t3) + total

# takes args freqs and amps which are the frequencies and amplitudes of a set of partials
# returns a list of x values and a list of y values for a dissonance curve
def getDissonanceCurve(freqs, amps, freqs2, amps2):
    t1 = Timbre(freqs, amps)
    t2 = Timbre(freqs2, amps2)
    x = []
    y = []
    dx = .001
    xMax = 2.2
    a = 1 # the frequency ratio

    for i in range(int((xMax-a)/dx)):
        x.append(a)
        y.append(D(t1, t2, a))
        a += dx

    return x, y


def findCurves():
    wavFiles = fs.getWavFiles()

    for i in range(len(wavFiles)):
        for j in range(len(wavFiles)):
            amps1 = []
            freqs1 = []
            amps2 = []
            freqs2 = []
            print("making dissonance curve for: " + wavFiles[i] + " and " + wavFiles[j])

            name = fs.myPath + "partials/peak_freqs_" + wavFiles[i][:-4] + ".csv"
            file = open(name, 'r')
            reader = csv.reader(file)
            for row in reader:
                freqs1.append(float(row[0]))

            name = fs.myPath + "partials/peak_amps_" + wavFiles[i][:-4] + ".csv"
            file = open(name, 'r')
            reader = csv.reader(file)
            for row in reader:
                amps1.append(float(row[0]))

            name = fs.myPath + "partials/peak_freqs_" + wavFiles[j][:-4] + ".csv"
            file = open(name, 'r')
            reader = csv.reader(file)
            for row in reader:
                freqs2.append(float(row[0]))

            name = fs.myPath + "partials/peak_amps_" + wavFiles[j][:-4] + ".csv"
            file = open(name, 'r')
            reader = csv.reader(file)
            for row in reader:
                amps2.append(float(row[0]))

            xVals, yVals = getDissonanceCurve(freqs1, amps1, freqs2, amps2)

            # fs.saveDissonanceVals(yVals, wavFiles[i][:-4])

            yVals = fs.normalize(yVals)

            plt.plot(xVals, yVals)
            plt.title("Dissonance Curve for: " + wavFiles[i] + " and " + wavFiles[j])
            plt.xlabel("Frequency Ratio")
            plt.ylabel("Dissonance")

            # Get current size
            fig_size = plt.rcParams["figure.figsize"]
            # Set figure width to 22 and height to 15
            fig_size[0] = 22
            fig_size[1] = 15
            plt.rcParams["figure.figsize"] = fig_size

            if not os.path.exists(fs.myPath + "dissonance_curves_normalized/" + wavFiles[i][:-4]):
                os.makedirs(fs.myPath + "dissonance_curves_normalized/" + wavFiles[i][:-4])

            plt.savefig(fs.myPath + "dissonance_curves_normalized/" + wavFiles[i][:-4] + "/" + wavFiles[j][:-4] + ".png")
            # plt.show()
            plt.close()

def makeMultiPlots():
    wavFiles = fs.getWavFiles()

    for i in range(1,len(wavFiles)):
        for j in range(1, len(wavFiles)):
            amps1 = []
            freqs1 = []
            amps2 = []
            freqs2 = []
            print("making dissonance curve for: " + wavFiles[i] + " and " + wavFiles[j])

            name = fs.myPath + "partials/peak_freqs_" + wavFiles[i][:-4] + ".csv"
            file = open(name, 'r')
            reader = csv.reader(file)
            for row in reader:
                freqs1.append(float(row[0]))

            name = fs.myPath + "partials/peak_amps_" + wavFiles[i][:-4] + ".csv"
            file = open(name, 'r')
            reader = csv.reader(file)
            for row in reader:
                amps1.append(float(row[0]))

            name = fs.myPath + "partials/peak_freqs_" + wavFiles[j][:-4] + ".csv"
            file = open(name, 'r')
            reader = csv.reader(file)
            for row in reader:
                freqs2.append(float(row[0]))

            name = fs.myPath + "partials/peak_amps_" + wavFiles[j][:-4] + ".csv"
            file = open(name, 'r')
            reader = csv.reader(file)
            for row in reader:
                amps2.append(float(row[0]))

            xVals, yVals = getDissonanceCurve(freqs1, amps1, freqs2, amps2)

            # fs.saveDissonanceVals(yVals, wavFiles[i][:-4])

            yVals = fs.normalize(yVals)

            plt.plot(xVals, yVals)

        plt.title("Dissonance Curve for: " + wavFiles[i] + " vs all other instruments")
        plt.xlabel("Frequency Ratio")
        plt.ylabel("Dissonance")

        # Get current size
        fig_size = plt.rcParams["figure.figsize"]
        # Set figure width to 22 and height to 15
        fig_size[0] = 22
        fig_size[1] = 15
        plt.rcParams["figure.figsize"] = fig_size

        # plt.savefig(fs.myPath + "multiplot_dissonance_curves/" + wavFiles[i][:-4] + ".png")
        plt.show()
        plt.close()

def findOneCurve(fileName1, fileName2):
    amps1 = []
    freqs1 = []
    amps2 = []
    freqs2 = []
    print("making dissonance curve for: " + fileName1 + " and " + fileName2)

    name = fs.myPath + "partials/peak_freqs_" + fileName1[:-4] + ".csv"
    file = open(name, 'r')
    reader = csv.reader(file)
    for row in reader:
        freqs1.append(float(row[0]))

    name = fs.myPath + "partials/peak_amps_" + fileName1[:-4] + ".csv"
    file = open(name, 'r')
    reader = csv.reader(file)
    for row in reader:
        amps1.append(float(row[0]))

    name = fs.myPath + "partials/peak_freqs_" + fileName2[:-4] + ".csv"
    file = open(name, 'r')
    reader = csv.reader(file)
    for row in reader:
        freqs2.append(float(row[0]))

    name = fs.myPath + "partials/peak_amps_" + fileName2[:-4] + ".csv"
    file = open(name, 'r')
    reader = csv.reader(file)
    for row in reader:
        amps2.append(float(row[0]))

    xVals, yVals = getDissonanceCurve(freqs1, amps1, freqs2, amps2)

    plt.plot(xVals, yVals)
    plt.title("Dissonance Curve for: " + fileName1 + " and " + fileName2)
    plt.xlabel("Frequency Ratio")
    plt.ylabel("Dissonance")

    plt.show()

# Get current size
fig_size = plt.rcParams["figure.figsize"]
# Set figure width to 22 and height to 15
fig_size[0] = 22
fig_size[1] = 15
plt.rcParams["figure.figsize"] = fig_size


def test():
    f = 440
    g= 440
    freqs1 = [f, 1.7*f, 2.84*f]
    freqs2 = [g, 1.67*g, 3.14*g]
    amps1 = [1,5,5]
    amps2 = [1,5,5]

    xVals, yVals = getDissonanceCurve(freqs1, amps1, freqs2, amps2)

    # fs.saveDissonanceVals(yVals, wavFiles[i][:-4])

    plt.plot(xVals, yVals)
    plt.xlabel("Frequency Ratio")
    plt.ylabel("Dissonance")

    # Get current size
    fig_size = plt.rcParams["figure.figsize"]
    # Set figure width to 22 and height to 15
    fig_size[0] = 22
    fig_size[1] = 15
    plt.rcParams["figure.figsize"] = fig_size

    plt.show()
    plt.close()
