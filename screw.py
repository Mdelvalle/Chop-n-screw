from echonest.remix import audio, modify
import random


class ChopnScrew:
    def __init__(self, input_filename, output_filename):
        print 'INITIALIZIN...'
        self.soundtouch = modify.Modify()
        self.song = audio.LocalAudioFile(input_filename)
        self.beats = self.song.analysis.beats
        self.out_shape = len(self.song.data)
        self.out_data = audio.AudioData(shape=self.out_shape, numChannels=1, sampleRate=44100)
        self.output_filename = output_filename

        # Amount to change
        self.tempo = -20
        self.pitch = -6

        self.chance_of_small_chop = 0.05
        self.chance_of_large_chop = 0.10

        self.last_played_index = 0

        self.beats2 = self.song.analysis.beats[1:]

        # hold all beats of the newly computed song for easy access later
        self.played_song = {}

        self.screw()

    def screw(self):
        """
        Slow down tempo and lower the pitch.
        """
        print 'SCREWIN...'

        old_data = None

        # Lower the pitch and the tempo.
        # Have the same beat twice; one of them is one beat ahead of the other.
        # There's a 5% chance of switching between them, which gives
        # the song that 'chopping' feel.
        for idx, (beat, beat2) in enumerate(zip(self.beats, self.beats2)):
            if old_data is not None:
                if random.random() <= self.chance_of_small_chop:
                    new_beat = self.soundtouch.shiftTempoChange(self.song[beat], self.tempo)
                else:
                    new_beat = self.soundtouch.shiftTempoChange(self.song[beat2], self.tempo)
            else:
                if random.random() <= self.chance_of_small_chop:
                    new_beat = self.soundtouch.shiftPitchSemiTones(self.song[beat], self.pitch)
                else:
                    new_beat = self.soundtouch.shiftPitchSemiTones(self.song[beat2], self.pitch)

            self.played_song[idx] = new_beat

            if random.random() < self.chance_of_large_chop:
                self.chop(idx)

            self.out_data.append(new_beat)
            old_data = self.song[beat]

        print 'WRITIN...'
        self.out_data.encode(self.output_filename)

    def chop(self, idx):
        """
        Either repeat a beat or repeat a long segment.
        """
        print 'CHOPPIN...'

        # Make it go back either 4 or 8 beats.
        go_back_n_beats = random.randint(1, 2) * 8

        # How many times you're allowed to play this segment.
        n_time_plays = random.randint(1, 2)
        
        # Make sure you aren't going back to any beats that were just played
        # unless you go to the beginning.
        if go_back_n_beats <= idx and idx - self.last_played_index >= 40:
            temp_beats, temp_plays = go_back_n_beats, n_time_plays
            while n_time_plays > 0:
                while go_back_n_beats > 0:
                    self.out_data.append(self.played_song[idx - go_back_n_beats])
                    go_back_n_beats -= 1
                go_back_n_beats = temp_beats
                n_time_plays -= 1

            self.last_played_index = idx


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

    chopped_n_screwed = ChopnScrew(input_filename, output_filename)
    

if __name__ == '__main__':
    main()
