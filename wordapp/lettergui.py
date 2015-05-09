# lettergui.py
# Walker M. White (wmw2)
# October 1, 2014
"""Kivy-Compatible GUI classes for the word puzzle.

These classes support an arbitrary word puzzle, not just the seven-cross puzzle.
They are designed so that they can be used in a kv layout file."""
from kivy.uix.widget        import Widget
from kivy.uix.label         import Label
from kivy.graphics          import Color, Rectangle, Line, Ellipse
from kivy.graphics.instructions import InstructionGroup
from kivy.properties        import NumericProperty, ReferenceListProperty, ListProperty, ObjectProperty, BooleanProperty

class LetterBox(Widget):
    """Instances represent a box with a single letter in it.
    
    Instance Attributes:
        foreground: the foreground color [4 element list of floats]
        background: the background color [4 element list of floats]
        textcolor: the text color [4 element list of floats]
        fontsize: the size of the font [int > 0]
        bold: whether the font is bolded [boolean]
        italic: whether the font is in italics [boolean]
        border: the border size in pixels [odd, positive integer]
        text: the character in this box [single element string]
        state: whether or not the box is pressed [boolean]
    """
    
    @property
    def foreground(self):
        """The foreground color, which is used to color the box border
        
        Defaults to black: [0,0,0,1]
        
        **Invariant**: A 4-element list of floats in the range 0..1"""
        return self._foreground.rgba
    
    @foreground.setter
    def foreground(self,value):
        assert type(value) == list, `value`+' is not a list'
        assert len(value) == 4 or len(value) == 3, `value`+' has the wrong length'
        if len(value) == 4:
            self._foreground.rgba = value
        else:
            self._foreground.rgb = value
    
    @property
    def background(self):
        """The background color, which is used to color the box interior
        
        Defaults to white: [1,1,1,1]
        
        **Invariant**: A 4-element list of floats in the range 0..1"""
        return self._background.rgba
    
    @background.setter
    def background(self,value):
        assert type(value) == list, `value`+' is not a list'
        assert len(value) == 4 or len(value) == 3, `value`+' has the wrong length'
        if len(value) == 4:
            self._background.rgba = value
        else:
            self._background.rgb = value
    
    @property
    def textcolor(self):
        """The color of the letter text
        
        Defaults to red: [1,0,0,1]
        
        **Invariant**: A 4-element list of floats in the range 0..1"""
        return list(self._label.color)
    
    @textcolor.setter
    def textcolor(self,value):
        assert type(value) == list, `value`+' is not a list'
        assert len(value) == 4 or len(value) == 3, `value`+' has the wrong length'
        self._label.color = value
    
    @property
    def border(self):
        """The size of the box border in pixels
        
        Defaults to 3
        
        **Invariant**: An odd, positive int"""
        return self._border
    
    @border.setter
    def border(self,value):
        assert type(value) == int, `value`+' is not an int'
        assert value >= 0, `value`+' is negative'
        self._border = 2* (value / 2)+1
    
    @property
    def fontsize(self):
        """The size of the letter font.
        
        Defaults to 24
        
        **Invariant**: An int > 0"""
        return self._label.font_size
    
    @fontsize.setter
    def fontsize(self,value):
        self._label.font_size = value
    
    @property
    def bold(self):
        """Whether the font is bold
        
        Defaults to False
        
        **Invariant**: A boolean"""
        return self._label.bold
    
    @bold.setter
    def bold(self,value):
        self._label.bold = value
        
    @property
    def italic(self):
        """Whether the font is in italics
        
        Defaults to False
        
        **Invariant**: A boolean"""
        return self._label.italic
    
    @italic.setter
    def italic(self,value):
        self._label.italic = value
    
    @property
    def text(self):
        """Whether the text in this box
        
        Defaults to ' '
        
        **Invariant**: A single element string"""
        return self._label.text
    
    @text.setter
    def text(self,value):
        assert type(value) == str and len(value) < 2, `value`+' is not a valid character'
        self._label.text = value
    
    @property
    def state(self):
        """A button state for the box (whether or not it is pressed)
        
        Defaults to False
        
        **Invariant**: A single element string"""
        return self._state
    
    @state.setter
    def state(self,value):
        assert type(value) == bool, `value`+' is not a boolean'
        self._state = value

    def __init__(self, **kw):
        """**Constructor**: Create a new letter box
        
            :param keywords: dictionary of keyword arguments 
            **Precondition**: See below.
        
        To use the constructor for this class, you should provide
        it with a list of keyword arguments that initialize various
        attributes.  For example, to initialize the text and the 
        foreground color, use the constructor call
        
            GObject(text='A',foreground=[1,0,0,1])
        
        You do not need to provide the keywords as a dictionary.
        The ** in the parameter `keywords` does that automatically.
        
        Any attribute of this class may be used as a keyword.  The
        argument must satisfy the invariants of that attribute.  See
        the list of attributes of this class for more information."""
        Widget.__init__(self,**kw)
        self._label = Label(**kw)
        self._state = False
        self._set_properties(kw)
        self._configure()
        self.bind(pos=self._reposition,size=self._resize)
    
    def _set_properties(self,kw):
        """Sets the letter box attributes according to kw
        
        If an attribute is not in kw, the attribute is set to a default.
        
            :param keywords: dictionary of keyword arguments 
            **Precondition**: Same as __init__"""
        if 'background' in kw:
            self._background = Color(kw['background'])
        else:
            self._background = Color(1,1,1,1)
        
        if 'foreground' in kw:
            self._foreground = Color(kw['foreground'])
        else:
            self._foreground = Color(0,0,0,1)
        
        if 'textcolor' in kw:
            self.textcolor = kw['textcolor']
        else:
            self.textcolor = [1,0,0,1]
        
        if 'border' in kw:
            self.border =kw['border']
        else:
            self.border = 3
        
        if 'fontsize' in kw:
            self.fontsize =kw['fontsize']
        else:
            self.fontsize = 24
        
        if 'bold' in kw:
            self.bold =kw['bold']
        else:
            self.bold = False
        
        if 'italic' in kw:
            self.italic =kw['italic']
        else:
            self.italic = False
        
        if 'state' in kw:
            self.state =kw['state']
        else:
            self.state = False
        
        if 'text' in kw:
            self.text =kw['text']
        else:
            self.text = ' '
    
    def _configure(self):
        """Initializes the canvas for this widget."""
        self._interior = Rectangle(pos=self.pos,size=self.size)
        self._exterior = Line(points=[0]*8, width=self.border, close = True, cap='square', joint='miter')
        self.canvas.add(self._background)
        self.canvas.add(self._interior)
        self.canvas.add(self._label.canvas)
        self.canvas.add(self._foreground)
        self.canvas.add(self._exterior)
        self._reposition(self,self.pos)
    
    def _reposition(self,obj,pos):
        """Repositions the graphics object.
        
        This function is called by Kivy services, so it passes the
        object and new position as an argument."""
        self._label.pos = pos
        self._interior.pos = pos
        
        self._exterior.points[0] = pos[0]
        self._exterior.points[1] = pos[1]
        self._exterior.points[2] = pos[0]+self.size[0]
        self._exterior.points[3] = pos[1]
        self._exterior.points[4] = pos[0]+self.size[0]
        self._exterior.points[5] = pos[1]+self.size[1]
        self._exterior.points[6] = pos[0]
        self._exterior.points[7] = pos[1]+self.size[1]
    
    def _resize(self,obj,size):
        """Resizes the graphics object.
        
        This function is called by Kivy services, so it passes the
        object and new size as an argument."""
        self._label.size = size
        self._interior.size = size
        self._exterior.points[2] = self.pos[0]+size[0]
        self._exterior.points[4] = self.pos[0]+size[0]
        self._exterior.points[5] = self.pos[1]+size[1]
        self._exterior.points[7] = self.pos[1]+size[1]
    
    def update():
        """Redraws the letter box after an update"""
        self._label.texture_update()


class LetterGrid(Widget):
    """An instance is a grid of letter boxes. 
    
    While letter boxes are arranged in a grid, not all grids must have a
    letter box.  This allows us to represent a seven-cross.
    
    Instance Attributes:
        cols: number of columns in the grid [int > 0]
        rows: number of rows in the grid [int > 0]
        foreground: the foreground color [4 element list of floats]
        background: the background color [4 element list of floats]
        textcolor: the text color [4 element list of floats]
        font_size: the size of the font [int > 0]
        bold: whether the font is bolded [boolean]
        italic: whether the font is in italics [boolean]
        border: the border size in pixels [odd, positive integer]
        
        _labels: the collection of all letter boxes [map of tuples to LetterBox]
        _back: drawing layer for unpressed boxes
        _front: drawing layer for pressed boxes
    """
    # Computed propery
    @property
    def cellsize(self):
        """A 2-element tuple with the cellsize in pixels."""
        if self._resized:
            width  = self.size[0]/float(self.cols)
            height = self.size[1]/float(self.rows)
            self._cellsize = (width, height)
            self._resized = False
        return self._cellsize
    
    # Kivy style properties for KV sheets
    cols = NumericProperty(1)
    rows = NumericProperty(1)
    border    = NumericProperty(3)
    font_size = NumericProperty(36)
    bold   = BooleanProperty(True)
    italic = BooleanProperty(False)
    foreground = ListProperty([0,0,0,1])
    background = ListProperty([1,1,1,1])
    textcolor  = ListProperty([1,0,0,1])
    
    def __init__(self, **kw):
        """**Constructor**: Create a new letter box
        
            :param keywords: dictionary of keyword arguments 
            **Precondition**: See below.
        
        To use the constructor for this class, you should provide
        it with a list of keyword arguments that initialize various
        attributes.  For example, to initialize a 2x3 grid, use
        the constructor call
        
            GObject(rows=2,cols=3)
        
        You do not need to provide the keywords as a dictionary.
        The ** in the parameter `keywords` does that automatically.
        
        Any attribute of this class may be used as a keyword.  The
        argument must satisfy the invariants of that attribute.  See
        the list of attributes of this class for more information."""
        Widget.__init__(self,**kw)
        self._resized = True
        self._labels = dict()
        self._set_properties(kw)
        self.bind(pos=self._reposition)
        
        # Create a layer for proper state control.
        self._back  = InstructionGroup()
        self._front = InstructionGroup()
        self.canvas.add(self._back)
        self.canvas.add(self._front)
        
        # Bind kivy attributes to methods
        self.bind(size=self._resize)
        self.bind(cols=self._resize)
        self.bind(rows=self._resize)
        self.bind(border=self._set_border)
        self.bind(font_size=self._set_font_size)
        self.bind(bold=self._set_bold)
        self.bind(italic=self._set_italic)
        self.bind(foreground=self._set_foreground)
        self.bind(background=self._set_background)
        self.bind(textcolor=self._set_textcolor)
    
    def clear(self):
        """Reset the entire letter grid, eliminating all letter boxes."""
        self._labels = dict()
       
        self.canvas.clear()
        self.canvas.add(Color(0,0,0,1))
        self.canvas.add(Rectangle(pos=self.pos,size=self.size))
        
        self._back  = InstructionGroup()
        self._front = InstructionGroup()
        self.canvas.add(self._back)
        self.canvas.add(self._front)
    
    def _set_properties(self,kw):
        """Sets the letter box attributes according to kw
        
        If an attribute is not in kw, the attribute is set to a default.
        
            :param keywords: dictionary of keyword arguments 
            **Precondition**: Same as __init__"""
        if 'cols' in kw:
            self.cols = kw['cols']
        
        if 'rows' in kw:
            self.rows = kw['rows']
        
        if 'background' in kw:
            self.background = kw['background']
        
        if 'foreground' in kw:
            self.foreground = kw['foreground']
        
        if 'textcolor' in kw:
            self.textcolor = kw['textcolor']
        
        if 'border' in kw:
            self.border =kw['border']
    
        if 'font_size' in kw:
            self.fontsize =kw['font_size']
        
        if 'bold' in kw:
            self.bold =kw['bold']
        
        if 'italic' in kw:
            self.italic =kw['italic']
    
    # Methods to update the letter grid
    def add_cell(self, s, col, row):
        """Adds a new cell to the letter grid.
        
        The letter grid has s as its initial text.
        
        If the cell already exists, it replaces the text with s.
        
        Precondition: row and col are valid indices in the grid.  s is a string."""
        assert row >= 0 and row < self.rows, 'Row '+`row`+' is out of range [0,'+`self.rows`+']'
        assert col >= 0 and col < self.cols, 'Row '+`col`+' is out of range [0,'+`self.cols`+']'
        if (col,row) in self._labels:
            self._labels[(col,row)].text = s
            return
        
        label = LetterBox(text=s, fontsize=self.font_size, color=self.textcolor)
        label.bold   = self.bold
        label.italic = self.italic
        label.size   = self.cellsize
        x = self.pos[0] + col*self.cellsize[0]
        y = self.pos[1] + row*self.cellsize[1]
        label.pos = [x,y]
        self._labels[(col,row)] = label
        self._back.add(label.canvas)
    
    def delete_cell(self, col, row):
        """Deletes the LetterBox at col and row.
        
        If there is no LetterBox at that position, this method does nothing.
        
        Precondition: row and col are valid indices in the grid."""
        if not (col, row) in self._labels:
            return
        
        label = self._labels[(col,row)]
        self._back.remove(label.canvas)
        del self._labels[(col,row)]
    
    def get_cell(self, col, row):
        """Returns the LetterBox at col and row.
        
        If there is no LetterBox at that position, it returns None.
        
        Precondition: row and col are valid indices in the grid."""
        assert row >= 0 and row < self.rows, 'Row '+`row`+' is out of range [0,'+`self.rows`+']'
        assert col >= 0 and col < self.cols, 'Row '+`col`+' is out of range [0,'+`self.cols`+']'

        if not (col, row) in self._labels:
            return None
            
        return self._labels[(col,row)]
    
    def toggle_cell(self, col, row):
        """Toggles the state of the LetterBox at col and row.
        
        If there is no LetterBox at that position, it does nothing.
        
        Precondition: row and col are valid indices in the grid."""
        if not (col, row) in self._labels:
            return
        
        label = self._labels[(col,row)]
        label.state = not label.state
        tmp = label.foreground
        label.foreground = label.background
        label.background = tmp
        tmp = label.textcolor
        tmp = map(lambda x: 1-x, tmp[:-1])+tmp[-1:]
        label.textcolor = tmp
        if label.state:
            self._front.add(label.canvas)
            return True
        
        self._front.remove(label.canvas)
        return False

    # Call Back Methods
    def _reposition(self,obj,value):
        """Repositions the graphics object.
        
        This function is called by Kivy services, so it passes the
        object and new position as an argument."""
        for pos in self._labels:
            self._labels[pos].pos[0] = self.pos[0]+self.cellsize[0]*pos[0]
            self._labels[pos].pos[1] = self.pos[1]+self.cellsize[1]*pos[1]
    
    def _resize(self,obj,value):
        """Resizes the graphics object.
        
        This function is called by Kivy services, so it passes the
        object and new size as an argument."""
        self._resized = True
        for pos in self._labels:
            self._labels[pos].size = self.cellsize
            self._labels[pos].pos[0] = self.pos[0]+self.cellsize[0]*pos[0]
            self._labels[pos].pos[1] = self.pos[1]+self.cellsize[1]*pos[1]
    
    def _set_border(self,obj,value):
        """Updates the border attribute.
        
        This method propagates its value across all LetterBoxes in the grid.
        
        This function is called by Kivy services, so it passes the object and
        new attribute value as an argument."""
        for pos in self._labels:
            self._labels[pos].border = value
    
    def _set_font_size(self,obj,value):
        """Updates the font size attribute.
        
        This method propagates its value across all LetterBoxes in the grid.
        
        This function is called by Kivy services, so it passes the object and
        new attribute value as an argument."""
        for pos in self._labels:
            self._labels[pos].fontsize = value
    
    def _set_bold(self,obj,value):
        """Updates the bold attribute.
        
        This method propagates its value across all LetterBoxes in the grid.
        
        This function is called by Kivy services, so it passes the object and
        new attribute value as an argument."""
        for pos in self._labels:
            self._labels[pos].bold = value
    
    def _set_italic(self,obj,value):
        """Updates the italic attribute.
        
        This method propagates its value across all LetterBoxes in the grid.
        
        This function is called by Kivy services, so it passes the object and
        new attribute value as an argument."""
        for pos in self._labels:
            self._labels[pos].italic = value
    
    def _set_foreground(self,obj,value):
        """Updates the foreground attribute.
        
        This method propagates its value across all LetterBoxes in the grid.
        
        This function is called by Kivy services, so it passes the object and
        new attribute value as an argument."""
        for pos in self._labels:
            self._labels[pos].foreground = list(value)
    
    def _set_background(self,obj,value):
        """Updates the background attribute.
        
        This method propagates its value across all LetterBoxes in the grid.
        
        This function is called by Kivy services, so it passes the object and
        new attribute value as an argument."""
        for pos in self._labels:
            self._labels[pos].background = list(value)
    
    def _set_textcolor(self,obj,value):
        """Updates the text color attribute.
        
        This method propagates its value across all LetterBoxes in the grid.
        
        This function is called by Kivy services, so it passes the object and
        new attribute value as an argument."""
        for pos in self._labels:
            self._labels[pos].textcolor = list(value)