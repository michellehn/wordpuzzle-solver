# soundlib.py
# Walker M. White (wmw2)
# October 1, 2014
"""Sound Library for Word Puzzle App"""
import kivy.resources
import pygame.mixer
import os
import sys

# User-defined resources
SOUND_PATH = str(os.path.join(os.path.dirname(__file__), 'Sounds'))
kivy.resources.resource_add_path(SOUND_PATH)


# Only initialize the sound engine once.
_INITIALIZED = False


def init():
    """Initialize the Sound Engine.
    
    Because of how the Pygame API works, we have to make this a stand-alone function.
    Essentially, the Pygame sound engine is a singleton."""
    FREQUENCY = 44100
    BITSIZE   = -16
    CHANNELS  = 2
    BUFFER    = 1024
    pygame.mixer.init(FREQUENCY,BITSIZE,CHANNELS,BUFFER)
    _INITIALIZED = True


def is_sound_file(name):
    """Return: True if name is the name of an font file"""
    if type(name) != str:
        return False
    
    return os.path.exists(SOUND_PATH+'/'+name)


def Sound(filename):
    """Creates a new Sound object for the given file.
    
    This function is a proxy for the pygame.mixer.Sound class.  That class requires
    some finicky initialization in order to work properly.  In order to hide that from
    you, we have given you this function to use instead.  Treat this function just
    like a constructor (except that the object type is pygame.mixer.Sound, not Sound).
    
        :param filename: string providing the name of a sound file
    
    See the online documentation for more information."""
    assert is_sound_file(filename), `filename`+' is not a sound file'
    absname = filename if os.path.isabs(filename) else str(os.path.join(SOUND_PATH, filename))
    return pygame.mixer.Sound(absname)


class SoundLibrary(object):
    """A sound library is like a dictionary that maps sounds to Sound objects.
    
    This class implements to the dictionary interface to make it easier to load
    sounds and manage them.  To load a sound, simply assign it to the library
    object, as follows:
    
        soundlib['soundname'] = 'soundfile.wav'
    
    The sound library will load the sound and map it to 'soundname' as the key.
    To play the sound, we access it as follows:
    
        soundlib['soundname'].play()
    
    Instance Attributes (Hidden):
        data: Dictionary mapping sound names to sound files
    """
    
    def __init__(self):
        """**Constructor**: Create a new, empty sound library."""
        if not _INITIALIZED:
            init()
        self._data = {}
    
    def __len__(self):
        """Returns: The number of sounds in this library."""
        return len(self._data)
    
    def __getitem__(self, key):
        """Returns: The Sound object for the given sound name.
        
        Precondition: key is a string."""
        return self._data[key]
    
    def __setitem__(self, name, filename):
        """Creates a sound object from the file filename and assigns it the given name.
        
        Precondition: filename is the name of a valid sound file. name is a string."""
        assert is_sound_file(filename), `filename`+' is not a sound file'
        self._data[name] = Sound(filename)
    
    def __delitem__(self, key):
        """Deletes the Sound object for the given sound name.
        
        Precondition: key is a string."""
        del self._data[key]
    
    def __iter__(self):
        """Returns: The iterator for this sound dictionary."""
        return self._data.iterkeys()
    
    def iterkeys(self):
        """Returns: The key iterator for this sound dictionary."""
        return self._data.iterkeys()

