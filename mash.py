from distutils.log import error
from pydub import AudioSegment
from pydub.playback import play

sound = AudioSegment.from_wav("./audio/src/better.wav")

bpm = 120
slice_length = int(60000/bpm)

print(slice_length)

if len(sound) < slice_length:
    raise ValueError('file too short')

slices = sound[::slice_length]

flippedslices = AudioSegment.empty()

for index, slice in enumerate(slices):

    rev_slice = slice.reverse()

    if index == 0:
        flippedslices += rev_slice
    elif len(slice) >= 100:
        flippedslices = flippedslices.append(rev_slice, crossfade=(100))
    else:
        flippedslices = flippedslices.append(rev_slice, crossfade=len(slice))


play(flippedslices)
