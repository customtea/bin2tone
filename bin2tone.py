### Reference https://news.mynavi.jp/article/zeropython-55/

import pyaudio
import numpy as np
import sys

RATE = 44100
BPM = 100
L1 = (60 / BPM * 4)
L2,L4,L8 = (L1/2,L1/4,L1/8)

C,D,E,F,G,A,B,C2 = (
        261.626, 293.665, 329.628, 
        349.228, 391.995, 440.000,
        493.883, 523.251)


def tone(freq, length, gain):
    slen = int(length * RATE)
    t = float(freq) * np.pi * 2 / RATE
    return np.sin(np.arange(slen) * t) * gain


def play_wave(stream, samples):
    stream.write(samples.astype(np.float32).tobytes())


p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=RATE,
                frames_per_buffer=1024,
                output=True)



print("play")
if len(sys.argv) != 2:
    sys.exit()

f = open(sys.argv[1],'rb')
while(True):
    data = f.read(1)
    if len(data) == 0:
        break
    idata = int(data.hex(), 16)
    print(format(idata, '02b'))
    
    sound_long = L8
    src = []
    
    if (idata >> 7) & 0x01 == 1:
        sound_long = L4
    if (idata >> 6) & 0x01 == 1:
        src.append(tone(B, sound_long, 1.0))
    if (idata >> 5) & 0x01 == 1:
        src.append(tone(A, sound_long, 1.0))
    if (idata >> 4) & 0x01 == 1:
        src.append(tone(G, sound_long, 1.0))
    if (idata >> 3) & 0x01 == 1:
        src.append(tone(F, sound_long, 1.0))
    if (idata >> 2) & 0x01 == 1:
        src.append(tone(E, sound_long, 1.0))
    if (idata >> 1) & 0x01 == 1:
        src.append(tone(D, sound_long, 1.0))
    if idata & 0x01 == 1:
        src.append(tone(C, sound_long, 1.0))
    else:
        src.append(tone(0, sound_long, 1.0))
    
    res = np.array([0] * len(src[0]))
    for s in src:
        res = res + s
    res *= (1/len(src))
    play_wave(stream, res)

stream.close()