from echonest.remix import audio, modify
import random
import sys
import errno


class ChopnScrew:
    def __init__(self, input_filename, output_filename):
        print 'INITIALIZIN...'
        sys.stdout.flush()
        self.soundtouch = modify.Modify()
        self.song = audio.LocalAudioFile(input_filename)
        self.beats = self.song.analysis.beats
        self.beats2 = self.song.analysis.beats[1:]
        self.out_shape = len(self.song.data)
        self.out_data = audio.AudioData(shape=self.out_shape, numChannels=1, sampleRate=44100)
        self.output_filename = output_filename

        # Amount to change
        self.tempo = -20
        self.pitch = -6

        self.chance_of_small_chop = 0.25
        self.chance_of_large_chop = 0.10
        self.beats_between_repeats = 40

        self.last_played_index = 0

        # hold all beats of the newly computed song for easy access later
        self.played_song = {}

        self.screw()

    def screw(self):
        """
        Slow down tempo and lower the pitch.
        """
        print 'SCREWIN...'
        sys.stdout.flush()

        old_data = None

        # Lower the pitch and the tempo.
        # Have the same beat twice; one of them is one beat ahead of the other.
        # There's a 5% chance of switching between them, which gives
        # the song that 'chopping' feel.
        upbeat = 0
        can_chop = True
        can_start = False
        l = len(self.beats)
	for idx, beat in enumerate(self.beats):
            if idx >= 14 and (idx <= (l - 14)):
                can_start = True

            if upbeat > 3:
                upbeat = 0
            else:
                upbeat += 1

            # Only chop if current beat is the downbeat and the last beat wasn't chopped
            if old_data is not None:
                if can_start and can_chop and upbeat == 1 and random.random() < self.chance_of_small_chop:
		    new_beat = self.soundtouch.shiftTempoChange(self.song[self.beats[idx+1]], self.tempo)
                    can_chop = False
                else:
                    new_beat = self.soundtouch.shiftTempoChange(self.song[beat], self.tempo)
                    can_chop = True
            else:
                if can_start and can_chop and upbeat == 1 and random.random() < self.chance_of_small_chop:
                    new_beat = self.soundtouch.shiftPitchSemiTones(self.song[self.beats[idx+1]], self.pitch)
                    can_chop = False
                else:
                    new_beat = self.soundtouch.shiftPitchSemiTones(self.song[beat], self.pitch)
                    can_chop = True

            self.played_song[idx] = new_beat

            if can_chop and upbeat == 0 and random.random() < self.chance_of_large_chop:
                self.chop(idx)

            self.out_data.append(new_beat)
            old_data = self.song[beat]

        print 'WRITIN...'
        sys.stdout.flush()
        self.out_data.encode(self.output_filename)

    def chop(self, idx):
        """
        Either repeat a beat or repeat a long segment.
        """
        print 'CHOPPIN...'
        sys.stdout.flush()

        # Make it go back either 8 or 16 beats.
        go_back_n_beats = random.randint(1, 2) * 8

        # How many times you're allowed to play this segment.
        n_time_plays = 1

        # Make sure you aren't going back to any beats that were just played
        # unless you go to the beginning.
        if go_back_n_beats <= idx and idx - self.last_played_index >= self.beats_between_repeats:
            temp_beats, temp_plays = go_back_n_beats, n_time_plays
            while n_time_plays > 0:
                while go_back_n_beats > 0:
                    self.out_data.append(self.played_song[idx - go_back_n_beats])
                    go_back_n_beats -= 1
                go_back_n_beats = temp_beats
                n_time_plays -= 1

            self.last_played_index = idx


def main():
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
        sys.stdout.flush()
        sys.exit(-1)
    try:
        chopped_n_screwed = ChopnScrew(input_filename, output_filename)
    except:
        e = sys.exc_info()
        print e
        sys.stdout.flush()
        sys.exit(-1)


if __name__ == '__main__':
    main()
