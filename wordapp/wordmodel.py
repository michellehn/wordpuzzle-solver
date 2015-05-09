# wordmodel.py
# Walker M. White (wmw2)
# October 1, 2014
"""Model class for Word Puzzle App"""
import urllib2
import hashlib
import traceback

# Webserver to contact for puzzle generation
WEBSERVER = 'http://cs1110.cs.cornell.edu/2014fa/a4/puzzle.php?netid='


def md5encode(s):
    """Returns: md5 hash for a string.
    
    The server provides the solution as a md5 hash so that students (hi, student 
    reading this comment) cannot find the solution by looking at the Python code.
    This function allows us to encode a string, so that we can compare it to the
    unique hash.
    
    Precondition: s is a string."""
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()


class PuzzleModel(object):
    """Instances represent a single puzzle.
    
    Every time the player gets a new puzzle, we create a new puzzle model.  This
    class ensures a classic MVC separation for the puzzle.
    
    Instance Attributes:
        netid:     the generating netid for this puzzle [str]
        progress:  the index of the lowest unscrambled word [int in range 0..6]
        puzzle:    the array of scrambled words [2d list of charcters]
        _solution: the md5 hashes of the puzzle solution [list of str, length 6]
        _original: the original state of the puzzle (for reset) [list of str, length 6]
    """
    
    # All properties are immutable
    @property 
    def netid(self):
        """The netid that generated this particular puzzle
        
        *This attribute may not be (directly) altered*"""
        return self._index
    
    @property 
    def progress(self):
        """The index of the currently active word in the puzzle.
        
        *This attribute may not be (directly) altered*"""
        return self._index
    
    @property 
    def solved(self):
        """Whether or not the puzzle has been solved
        
        *This attribute may not be (directly) altered*"""
        return self._index == 7

    @property 
    def puzzle(self):
        """The current state of this puzzle.
        
        This value is a list of strings, each string of length 7.  The
        list itself is length 6.
        
        For performance reasons, we return the 2D array directly, and 
        do not copy it.  This is unsafe, but considered an acceptable
        trade-off.
        
        *This attribute may not be (directly) altered*"""
        return self._puzzle
    
    def __init__(self):
        """**Constructor**: Create a new, empty word puzzle.
        
        This method does not actually initialize the puzzle.  Use the methods
        load or download to initialize the puzzle."""
        self._netid = None
        self._solution = [[' ']*7]*6
        self._original = [[' ']*7]*6
        self._puzzle = map(list,self._original)
        self._index  = 0
    
    # Initialization Methods
    def download(self,netid):
        """Connect to the webserver and download the puzzle for this netid.
        
        Precondition: netid is a string."""
        self._netid = netid
        
        u = urllib2.urlopen(WEBSERVER+netid)
        data = u.read().split('<br/>')
        
        self._solution  = data[:6]
        self._original = data[6:]
        self._puzzle = map(list,self._original)
        self._index  = 0
    
    def load(self,filename):
        """Return: True if the puzzle state was loaded from filename
        
        This method will actually redownload the game (to get the original)
        state, but then fast forward the game to the saved state.
        
        If filename is not the name of a valid save file, then this method
        leaves the puzzle unaffected.
        
        Precondition: filename is a string"""
        try:
            # Read the data
            f = open(filename,'r')
            data = []
            for x in f:
                data.append(x.strip())
            
            # Redownload
            self.download(data[0])
            
            # Fast forward the state
            self._index  = int(data[7])
            self._puzzle = map(list,data[8:])
            return True
        except:
            return False
    
    def reset(self):
        """Reset the puzzle state back to the beginning."""
        self._index = 0
        self._puzzle = map(list,self._original)
    
    def save(self,filename):
        """Save the given puzzle state to a file
        
        Precondition: filename is a string."""
        try:
            f = open(filename,'w')
            f.write(self._netid+'\n')
            for x in self._solution:
                f.write(x+'\n')
            f.write(str(self._index)+'\n')
            for x in self.puzzle:
                w = ''.join(x)
                f.write(w+'\n')
            f.close()
        except:
            pass
    
    # Interactive Methods
    def locked(self, a):
        """Returns: True if position a in the current word is locked.
        
        The current word is determined by the attribute progress."""
        locked = a < 0 or a >= 7
        if self._index == 1:
            locked = locked or a == 6
        elif self._index == 2:
            locked = locked or a == 0
        elif self._index == 3 or self._index == 5:
            locked = locked or a == 0 or a == 6
        elif self._index == 5:
            locked = locked or a == 0 or a == 6 or a == 3
        return locked
    
    def swap(self, a, b):
        """Returns: True if swapping a and b will solve the current word.
        
        This method swaps the letters at a and b in the current word.
        If this solves this word, it increments the progress attribute
        and removes true.
        
        Precondition: a and b are unlocked position."""
        assert not self.locked(a), 'Position '+str(a)+' is locked'
        assert not self.locked(b), 'Position '+str(b)+' is locked'

        tmp = self._puzzle[self._index][a]
        self._puzzle[self._index][a] = self._puzzle[self._index][b]
        self._puzzle[self._index][b] = tmp
        # Increment if solved
        solved = False
        
        # Check to see if we completed this part of the puzzle
        digest = md5encode(''.join(self.puzzle[self._index]))
        if digest == self._solution[self._index]:
            solved = True
            self.increment()
        return solved
    
    def increment(self):
        """Increments the puzzle state if when a word is solved.
        
        As the solution affects the contents of unsolved words, 
        the results are propagated to the next level."""
        self._index += 1
        if self._index == 1:
            self._puzzle[1][6] = self._puzzle[0][0]
            self._puzzle[5][6] = self._puzzle[0][3]
            self._puzzle[3][6] = self._puzzle[0][6]
        elif self._index == 2:
            self._puzzle[4][0] = self._puzzle[1][3]
            self._puzzle[2][0] = self._puzzle[1][0]
        elif self._index == 3:
            self._puzzle[5][0] = self._puzzle[2][3]
            self._puzzle[3][0] = self._puzzle[2][6]
        elif self._index == 4:
            self._puzzle[4][6] = self._puzzle[3][3]
        elif self._index == 5:
            self._puzzle[5][3] = self._puzzle[4][3]
