from pydub import AudioSegment
from pydub.playback import play
from pydub.effects import high_pass_filter, low_pass_filter, compress_dynamic_range, speedup

sound = AudioSegment.from_wav("./audio/src/speech.wav")

bpm = 200
slice_length = int(60000/bpm)

if len(sound) < slice_length:
    raise ValueError('file too short')
 
slices = sound[::slice_length]

flippedslices = AudioSegment.empty()

for index, slice in enumerate(slices):

    rev_slice = slice.reverse()

    if index == 0:
        flippedslices += rev_slice
    elif len(slice) >= 100:
        if index % 5 == 0:
            stutter = slice.append(high_pass_filter(slice, 1000))
            flippedslices = flippedslices.append(
                stutter, crossfade=50)
        elif index % 2 == 0:
            flippedslices = flippedslices.append(
                rev_slice, crossfade=50)
        elif index % 3 == 0:
            stutter = slice.append(low_pass_filter(slice.reverse(), 400))
            flippedslices = flippedslices.append(
                stutter, crossfade=50)
        else:
            flippedslices = flippedslices.append(
                slice, crossfade=50)
    else:
        if index % 2 == 0:
            slow = speedup(rev_slice)
            flippedslices = flippedslices.append(
                slow, crossfade=len(slice))
        else:
            flippedslices = flippedslices.append(
                slice, crossfade=len(slice))

comp = compress_dynamic_range(flippedslices, -3, 10,  1, 10)

play(comp)
