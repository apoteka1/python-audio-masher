from pydub import AudioSegment
from pydub.playback import play
from pydub.effects import low_pass_filter, high_pass_filter, speedup


sound = AudioSegment.from_wav("./audio/src/better.wav")

slices = sound[::120]

mashed = AudioSegment.empty()

for slice in slices:

    new_slice = slice

    last_echo = slice

    for i in range(1, 8):
        locut = 20000 - (i*2500)
        hicut = i*120
        echo = high_pass_filter(low_pass_filter(
            last_echo, locut).reverse(), hicut)
        new_slice = new_slice.append(echo[:(len(echo)-15)], 5)
        last_echo = echo[:(len(echo)-15)]

    if len(mashed) == 0:
        mashed = new_slice
    elif len(new_slice) >= 100:
        mashed = mashed.append(new_slice)

play(mashed)
