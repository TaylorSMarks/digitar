from musical.theory import Note as InnerNote
from musical.audio  import playback, source

frameRate = 44100

class Note:
    def __init__(self, name = 'C3', length = 1.0, delay = 0.0, volume = 0.25):
        self.name = name
        self.length = length
        self.delay = delay
        self.volume = volume

    def render(self):
        k = (self.name, self.length, self.volume)
        if k not in Note.renderCache:
            Note.renderCache[k] = source.pluck(InnerNote(self.name), self.length) * self.volume
        return Note.renderCache[k]

Note.renderCache = {}

def playnotes(namesOrNotes = ['C3', 'E3', 'G3', 'C4'], length = 2.0, delay = 0.05, volume = 0.25):
    if isinstance(length, str):
        raise Exception("If you want to play multiple notes, wrap them in [] like playnotes(['C3', 'E3'])")
    elif isinstance(length, Note):
        raise Exception("If you want to play multiple notes, wrap them in [] like playnotes([note1, note2])")

    if isinstance(namesOrNotes, str):
        namesOrNotes = [Note(namesOrNotes, length, delay, volume)]
    elif isinstance(namesOrNotes, Note):
        namesOrNotes = [namesOrNotes]
    elif isinstance(namesOrNotes[0], str):
        namesOrNotes = [Note(name, length, delay * index, volume) for index, name in enumerate(namesOrNotes)]

    # Render all the notes.
    fullLength = 0.0

    for note in namesOrNotes:
        fullLength = max(fullLength, note.length + note.delay)

    out = source.silence(fullLength + 0.1)  # Pad it a bit so I stop getting errors...
    #print('fullLength: {} silence frames: {}'.format(fullLength, len(out)))

    for note in namesOrNotes:
        firstFrame = int(note.delay * frameRate)
        #print('delay: {} first frame: {}'.format(note.delay, firstFrame))
        data = note.render()
        #print('delay: {} first frame: {} data size: {}'.format(note.delay, firstFrame, len(data)))
        out[firstFrame:firstFrame + len(data)] += data

    playback.play(out)