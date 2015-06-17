from echonest.remix import audio, modify
import random


def screw(input_filename, output_filename):
    """
    Slow down tempo and lower the pitch
    """

    soundtouch = modify.Modify()
    song = audio.LocalAudioFile(input_filename)
    beats = song.analysis.beats
    out_shape = len(song.data)
    out_data = audio.AudioData(shape=out_shape, numChannels=1, sampleRate=44100)

    # Amount to change
    tempo = -20
    pitch = -6

    print 'Slow tempo...'

    beats2 = song.analysis.beats[1:]
    old_data = None

    # Lower the pitch and the tempo.
    # Have the same beat twice; one of them is one beat ahead of the other.
    # There's a 10% chance of switching between them, which gives
    # the song that 'chopping' feel.
    for beat, beat2 in zip(beats, beats2):
        if old_data is not None:
            if random.random() < 0.1:
                new_beat = soundtouch.shiftTempoChange(song[beat], tempo)
            else:
                new_beat = soundtouch.shiftTempoChange(song[beat2], tempo)
        else:
            if random.random() < 0.1:
                new_beat = soundtouch.shiftPitchSemiTones(song[beat], pitch)
            else:
                new_beat = soundtouch.shiftPitchSemiTones(song[beat2], pitch)

        out_data.append(new_beat)
        old_data = song[beat]

    print 'Encoding...'
    out_data.encode(output_filename)


def main():
    import sys

    usage = """
    Usage:
        python screw.py <input_filename> <output_filename>

    Example:
        python screw.py song_input.mp3 song_output.mp3
    """

    try:
        # This gets the filenames to read from and write to.
        input_filename = sys.argv[1]
        output_filename = sys.argv[2]
    except:
        # If things go wrong, exit!
        print usage
        sys.exit(-1)

    screw(input_filename, output_filename)
    

if __name__ == '__main__':
    main()
