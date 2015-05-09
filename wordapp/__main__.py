# __main__.py
# Walker M. White (wmw2)
# October 1, 2014
"""View for the Word Puzzle App"""
from kivy.app               import App
from kivy.lang              import Builder
from kivy.factory           import Factory
from kivy.config            import Config
from kivy.clock             import Clock
from kivy.uix.widget        import Widget
from kivy.uix.label         import Label
from kivy.uix.modalview     import ModalView
from kivy.uix.boxlayout     import BoxLayout
from kivy.uix.anchorlayout  import AnchorLayout
from kivy.properties        import NumericProperty, ReferenceListProperty, ListProperty, ObjectProperty

from lettergui              import LetterBox, LetterGrid
from soundlib               import SoundLibrary
from wordmodel              import PuzzleModel
import math


class InfoPanel(BoxLayout):
    """Instances represent the info box widget for net-id"""
    msgLabel  = ObjectProperty(None)
    infoField = ObjectProperty(None)
    okButton  = ObjectProperty(None)
    noButton  = ObjectProperty(None)
    
    def __init__(self,**kw):
        """Initialize the Info Panel Widgit
        
        Precondition: kw is a Kivy style attribute dictionary."""
        BoxLayout.__init__(self,**kw)
        self._callback = kw['callback'] if 'callback' in kw else None
    
    def on_okay(self):
        """Call back function for when 'OK' is pressed."""
        self.parent.dismiss()
        self._callback(self.infoField.text.strip())
    
    def on_cancel(self):
        """Call back function for when 'Cancel' is pressed."""
        self.parent.dismiss()


class PuzzleWidget(LetterGrid):
    """Instances represent the scramble puzzle.
    
    This class integrates with word puzzle model with the LetterGrid GUI.
    """
    # GUI State Constants
    STATE_COMPLETE = 0
    STATE_ACTIVE   = 1
    STATE_INACTIVE = 2
    
    # Delay the animation
    DELAY_SWAP = 0.25
    DELAY_POP  = 0.25
    
    # Kivy Attributes
    completeForeground = ListProperty([0,0,0,1])
    completeBackground = ListProperty([0,0,1,1])
    completeTextColor  = ListProperty([1,1,1,1])
    activeForeground   = ListProperty([0,0,0,1])
    activeBackground   = ListProperty([1,1,1,1])
    activeTextColor    = ListProperty([1,0,0,1])
    inactiveForeground = ListProperty([0,0,0,0.5])
    inactiveBackground = ListProperty([1,1,1,0.5])
    inactiveTextColor  = ListProperty([1,0,0,0.5])
    
    @property
    def model(self):
        """The model associated with this LetterGrid"""
        return self._model
    
    @model.setter
    def model(self,value):
        assert value is None or type(value) == PuzzleModel, `value`+' is not a PuzzleModel'
        self._model = value
        if self._active:
            words = [[' ']*7]*6 if value is None else value.puzzle
            self.clear()
            self._down  = []
            self._disabled = False
            self._load_words(words)
            self._position = self.model.progress
            self._update_ui()
    
    # Initialization Methods
    def __init__(self, **kw):
        """Initialize the Info Panel Widgit
        
        The widget starts out with no model and no contents.
        
        Precondition: kw is a Kivy style attribute dictionary."""
        LetterGrid.__init__(self,**kw)
        self._active = False
        self._model  = None
        self.position = -1

        self._netid = ''
        self._down  = []
        self._disabled = False
    
        self.sounds = SoundLibrary()
        self.sounds['off']   = 'drop.wav'
        self.sounds['on']    = 'boing.wav'
        self.sounds['swap']  = 'zip2.wav'
        self.sounds['solve'] = 'cha-ching.wav'
        self.sounds['win']   = 'ship-bell.wav'
    
    def register(self):
        """Initialize the view state once the Kivy application enters focus."""
        if self.model is None:
            words = [[' ']*7]*6 
            self._position = 0
        else:
            words = self.model.puzzle
            self._position = self.model.progress
        self.clear()
        self._down  = []
        self._disabled = False
        self._load_words(words)
        self._update_ui()
        self._active = True
    
    def _load_words(self, words):
        """Store the given words into the appropriate LetterBoxes"""
        # Rightmost column
        for x in range(7):
            w = words[0][x].upper()
            self.add_cell(w,6,6-x)
        
        # Upper row
        for x in range(6):
            w = words[1][x].upper()
            self.add_cell(w,x,6)
        
        # Leftmost column
        for x in range(1,7):
            w = words[2][x].upper()
            self.add_cell(w,0,6-x)
        
        # Bottom row
        for x in range(1,6):
            w = words[3][x].upper()
            self.add_cell(w,x,0)
        
        # Middle column
        for x in range(1,6):
            w = words[4][x].upper()
            self.add_cell(w,3,6-x)
        
        # Middle row
        for x in range(1,6):
            if x != 3:
                w = words[5][x].upper()
                self.add_cell(w,x,3)
    
    def _update_ui(self):
        """Update the UI to indicate the current model state.
        
        The active word is given active coloring.  Inactive words
        get inactive coloring and solved words get solved coloring."""
        if self.model is None:
            return
        
        self.position = self.model.progress
        pos = self.position # Simplifies coding
        
        # Rightmost column
        state = 1 if pos == 0 else (0 if pos > 0 else 2)
        for x in range(7):
            self._update_cell_ui(6,6-x,state)
        
        # Upper row
        state = 1 if pos == 1 else (0 if pos > 1 else 2)
        for x in range(6):
            self._update_cell_ui(x,6,state)
        
        # Leftmost column
        state = 1 if pos == 2 else (0 if pos > 2 else 2)
        for x in range(1,7):
            self._update_cell_ui(0,6-x,state)
        
        # Bottom row
        state = 1 if pos == 3 else (0 if pos > 3 else 2)
        for x in range(1,6):
            self._update_cell_ui(x,0,state)
        
        # Middle column
        state = 1 if pos == 4 else (0 if pos > 4 else 2)
        for x in range(1,6):
            self._update_cell_ui(3,6-x,state)
        
        # Middle row
        state = 1 if pos == 5 else (0 if pos > 5 else 2)
        for x in range(1,6):
            if x != 3:
                self._update_cell_ui(x,3,state)
    
    def _update_cell_ui(self,col,row,state):
        """Update the UI of a single cell to indicate the current model state.
        
        The active word is given active coloring.  Inactive words
        get inactive coloring and solved words get solved coloring.
        
        Precondition: row and col are valid indices in the grid.  
        state is one of STATE_COMPLETE, STATE_ACTIVE or STATE_INACTIVE"""
        label = self.get_cell(col,row)
        if state == self.STATE_COMPLETE:
            label.foreground = list(self.completeForeground)
            label.background = list(self.completeBackground)
            label.textcolor  = list(self.completeTextColor)
        elif state == self.STATE_ACTIVE:
            label.foreground = list(self.activeForeground)
            label.background = list(self.activeBackground)
            label.textcolor  = list(self.activeTextColor)
        else:
            label.foreground = list(self.inactiveForeground)
            label.background = list(self.inactiveBackground)
            label.textcolor  = list(self.inactiveTextColor)
    
    # Mouse Handling
    def click_to_cell(self, x, y):
        """Returns: The grid cell for the mouse click at x and y
        
        Precondition: x and y are ints."""
        dx = math.floor((x - self.pos[0])/self.cellsize[0])
        dy = math.floor((y - self.pos[1])/self.cellsize[1])
        return (int(dx),int(dy))
    
    def click_valid(self, x, y):
        """Returns: True if x, y is a valid grid position.
        
        A grid position is valid if (1) there is a LetterBox there, (2)
        it is part of an unsolved word and (3) it is not locked.
        
        Precondition: x and y are ints."""
        if self.model is None:
            return False
        elif not (x,y) in self._labels:
            return False
        
        if self.model.progress == 0:
            return x == 6
        elif self.model.progress == 1:
            return y == 6 and x != 6
        elif self.model.progress == 2:
            return x == 0 and y != 6
        elif self.model.progress == 3:
            return y == 0 and x % 6 != 0
        elif self.model.progress == 4:
            return x == 3 and y % 6 != 0
        elif self.model.progress == 5:
            return y == 3 and x % 3 != 0
        return False
    
    def view_to_model(self,x,y):
        """Returns: The index in the model for the (valid) click position.
        
        If there is not model, or the click position is invalid, return -1
        
        Precondition: x and y are ints."""
        if self.model is None:
            return -1
        elif not (x,y) in self._labels:
            return -1
        
        if self.model.progress % 2== 0:
            return 6-y
        
        return x
    
    def on_touch_down(self, touch):
        """Process a mouse touch
        
        Precondition: touch is a Touch Event."""
        if self._disabled:
            return
        
        # Compute where the touch is on the grid.
        cell = self.click_to_cell(touch.x,touch.y)
        if self.click_valid(cell[0],cell[1]):
            if self.toggle_cell(cell[0],cell[1]):
                self.sounds['on'].play()
                self._down.append(tuple(cell))
            else:
                self.sounds['off'].play()
                self._down.remove(tuple(cell))
        if len(self._down) == 2:
            self._disabled = True
            Clock.schedule_once(self._delay_swap,0.35) # Magic number determined by tuning
    
    def reset(self):
        """Reset the game state."""
        if self.model is None:
            return
        
        self.model.reset()
        words = self.model.puzzle
        self._position = self.model.progress
        print self.clear
        self.clear()
        self._down  = []
        self._disabled = False
        self._load_words(words)
        self._update_ui()
        self._active = True
    
    # Animation Methods
    # We have built-in delays to make the animation look smooth
    def _delay_swap(self,dt):
        """Swap the letters in two LetterBoxes.
        
        Precondition: dt is a float"""
        pos1 = self._down[0]
        pos2 = self._down[1]
        label1 = self._labels[pos1]
        label2 = self._labels[pos2]
        tmp = label1.text
        label1.text = label2.text
        label2.text = tmp
        
        mpos1 = self.view_to_model(pos1[0],pos1[1])
        mpos2 = self.view_to_model(pos2[0],pos2[1])
        
        self.model.swap(mpos1,mpos2)
        self.sounds['swap'].play()
        Clock.schedule_once(self._delay_popup,self.DELAY_SWAP)
    
    def _delay_popup(self,dt):
        """Pop the letters back up after a swap.
        
        Precondition: dt is a float"""
        cell = self._down[0]
        self.toggle_cell(cell[0],cell[1])
        cell = self._down[1]
        self.toggle_cell(cell[0],cell[1])
        self._down = []
        if self.position != self.model.progress:
            Clock.schedule_once(self._delay_progress,self.DELAY_POP)
        else:
            self._disabled = False
    
    def _delay_progress(self,dt):
        """Shift to a new word when one is solved.
        
        Precondition: dt is a float"""
        self.position = self.model.progress
        self._update_ui()
        if self.position == 6:
            self.parent.parent.top.statusLabel.text = 'SOLVED!'
            self.sounds['win'].play()
        else:
            self.sounds['solve'].play()
        self._disabled = False


class BotPanel(AnchorLayout):
    """Instances implement the top panel (text boxes and buttons)"""
    puzzlePanel = ObjectProperty(None)
    
    def register(self):
        self.puzzlePanel.register()


class TopPanel(BoxLayout):
    """Instances implement the top panel (text boxes and buttons)"""
    startButton = ObjectProperty(None)
    resetButton = ObjectProperty(None)
    saveButton  = ObjectProperty(None)
    loadButton  = ObjectProperty(None)
    statusLabel = ObjectProperty(None)


class WordPuzzleWidget(BoxLayout):
    """Instances represent the top level widget"""
    top = ObjectProperty(None)
    bot = ObjectProperty(None)
    
    def on_new_game(self):
        """Handle the new game button"""
        view = ModalView(size_hint=(None, None), size=(300, 300))
        view.add_widget(InfoPanel(callback=self._start_download))
        view.open()
    
    def _start_download(self,netid):
        """Initiate the download.
        
        Downloading is delayed by one clock cycle, so we can update the view."""
        self.top.statusLabel.text = 'Loading...'
        self._netid = netid
        Clock.schedule_once(self._do_download,0)
    
    def _do_download(self,dt):
        """Complete the download.
        
        Downloading is delayed by one clock cycle, so we can update the view."""
        model = PuzzleModel()
        model.download(self._netid)
        self.bot.puzzlePanel.model = model
        self.top.statusLabel.text = ''
    
    def on_reset(self):
        """Handle the reset game button"""
        self.top.statusLabel.text = 'Reseting...'
        Clock.schedule_once(self._do_reset,0)
    
    def _do_reset(self,dt):
        """Complete the reset.
        
        Reset is delayed by one clock cycle, so we can update the view."""
        self.bot.puzzlePanel.reset()
        self.top.statusLabel.text = ''
    
    def on_save(self):
        """Handle the save game button"""
        self.top.statusLabel.text = 'Saving...'
        Clock.schedule_once(self._do_save,0)
    
    def _do_save(self,dt):
        """Complete the save.
        
        Sace is delayed by one clock cycle, so we can update the view."""
        if not self.bot.puzzlePanel.model is None:
            self.bot.puzzlePanel.model.save('data.save')
        self.top.statusLabel.text = ''
    
    def on_load(self):
        """Handle the load game button"""
        self.top.statusLabel.text = 'Loading...'
        Clock.schedule_once(self._do_load,0)
    
    def _do_load(self,dt):
        """Complete the load.
        
        Load is delayed by one clock cycle, so we can update the view."""
        model = PuzzleModel()
        if model.load('data.save'):
            self.bot.puzzlePanel.model = model
            self.top.statusLabel.text = ''
        else:
            self.top.statusLabel.text = 'ERROR: No Save'
    
    def register(self):
        """Initialize the view state once the Kivy application enters focus."""
        self.bot.register()


class WordPuzzleApp(App):
    """Instances represnet the word puzzle application"""
    def build(self):
        """Read kivy file and perform layout"""
        Config.set('graphics', 'width', '600')
        Config.set('graphics', 'height', '600')
        return WordPuzzleWidget()
    
    def on_start(self):
        """Start up the app and initialize values"""
        super(WordPuzzleApp,self).on_start()
        self.root.register()


# Link classes to the KV file
Factory.register('PuzzleWidget', PuzzleWidget)
Factory.register('InfoPanel', InfoPanel)
Factory.register('TopPanel', TopPanel)
Factory.register('BotPanel', BotPanel)


# Application Code
if __name__ in ('__android__', '__main__'):
    WordPuzzleApp().run()