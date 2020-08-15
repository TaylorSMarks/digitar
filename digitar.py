'''
The primary use of the digitar module is the playnotes() function.
If it's desired to assign a unique length or volume of, or delay between the notes, it's also possible to pass in a list of Note instances instead.
'''

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

from musical.theory import Note as InnerNote
from musical.audio  import playback, source

class Note:
    '''
    Used for customizing the length, delay, or volume of individual notes passed into the playnotes function.
    '''
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
    '''
    Plays the notes passed in on the digitar (digital-guitar).
    
    Parameters:
            namesOrNotes: Represents the notes to be played in one of these -
                    1 - a string naming a note, like 'C3', 'D#4', or 'Bb2',
                    2 - a list of strings naming the notes as above,
                    3 - a Note instance, or
                    4 - a list of Note instances.
                Defaults to ['C3', 'E3', 'G3', 'C4'] - it's a nice sounding chord.
            length: If not using Note instance(s), defines how long each note will be held for, in seconds.
                Defaults to 2.0 seconds.
            delay: If a list of strings is passed in, defines how many seconds to wait before each additional note is started.
                Defaults to 0.05 seconds.
            volume: If not using Note instance(s), defines how loudly the notes will be played.
                Defaults to 0.25.
    '''
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
    sampleRate = 44100

    for note in namesOrNotes:
        fullLength = max(fullLength, note.length + note.delay)

    out = source.silence(fullLength + 0.1)  # Pad it a bit so I stop getting errors...
    #print('fullLength: {} silence samples: {}'.format(fullLength, len(out)))

    for note in namesOrNotes:
        firstSample = int(note.delay * sampleRate)
        #print('delay: {} first sample: {}'.format(note.delay, firstSample))
        data = note.render()
        #print('delay: {} first sample: {} data size: {}'.format(note.delay, firstSample, len(data)))
        out[firstSample:firstSample + len(data)] += data

    playback.play(out)
