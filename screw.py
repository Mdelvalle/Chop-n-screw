from echonest.remix import audio, modify


def screw(input_filename, output_filename):
    soundtouch = modify.Modify()
    audiofile = audio.LocalAudioFile(input_filename)
    beats = audiofile.analysis.beats
    out_shape = len(audiofile.data)
    out_data = audio.AudioData(shape=out_shape, numChannels=1, sampleRate=44100)

    tempo = -20
    pitch = -6

    for beat in beats:
        new_beat = soundtouch.shiftTempoChange(audiofile[beat], tempo)
        new_beat = soundtouch.shiftPitchSemiTones(audiofile[beat], pitch)

        out_data.append(new_beat)

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
