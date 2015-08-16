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

    chance_of_small_chop = 0.05
    chance_of_large_chop = 0.10

    last_played_index = 0

    print 'Slow tempo...'

    beats2 = song.analysis.beats[1:]
    old_data = None

    # hold all beats of the newly computed song for easy access later
    played_song = {}
    # Lower the pitch and the tempo.
    # Have the same beat twice; one of them is one beat ahead of the other.
    # There's a 10% chance of switching between them, which gives
    # the song that 'chopping' feel.
    for idx, (beat, beat2) in enumerate(zip(beats, beats2)):
        if old_data is not None:
            if random.random() <= chance_of_small_chop:
                new_beat = soundtouch.shiftTempoChange(song[beat], tempo)
            else:
                new_beat = soundtouch.shiftTempoChange(song[beat2], tempo)
        else:
            if random.random() <= chance_of_small_chop:
                new_beat = soundtouch.shiftPitchSemiTones(song[beat], pitch)
            else:
                new_beat = soundtouch.shiftPitchSemiTones(song[beat2], pitch)

        played_song[idx] = new_beat

        if random.random() < chance_of_large_chop:
            # Make it go back either 4 or 8 beats.
            go_back_n_beats = random.randint(1, 2) * 4

            # How many times you're allowed to play this segment.
            n_time_plays = random.randint(1, 2)
            
            # Make sure you aren't going back to any beats that were just played
            # unless you go to the beginning.
            if go_back_n_beats <= idx and idx - last_played_index >= 32:
                temp_beats, temp_plays = go_back_n_beats, n_time_plays
                while n_time_plays > 0:
                    while go_back_n_beats > 0:
                        out_data.append(played_song[idx - go_back_n_beats])
                        go_back_n_beats -= 1
                    go_back_n_beats = temp_beats
                    n_time_plays -= 1
                n_time_plays = temp_plays

                last_played_index = idx
        else:
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
