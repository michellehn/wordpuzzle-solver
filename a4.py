# a4.py
# Michelle Nelson, mhn29
# 11/2/14
""" Functions for Assignment A4"""


# Task 1: Word Lists

def build_word_list(filename):
    """Returns a list of words from the given file
    
    Each word in the file should stored on a separate line. The lines are trimmed 
    to remove trailing spaces and line returns. 
    
    Example: build_word_list('short.txt') returns the 10 element list of words
    ['the','be','to','of','and','a','in','that','have','it'].
    
    Precondition: filename is the name of a text file storing a list of words.
    
    Enforced Precondition: filename is a string"""
    
    assert type(filename) == str, `filename`+' is not a string.'
    
    file = open(filename)
    
    thelist = []
    for line in file:
        if '\n' in line:
            word = line[:-1]
        else:
            word = line
        thelist.append(word)
    file.close()
    
    return thelist


def word_list_by_size(words, size):
    """Returns the elements of words that have length size
    
    The words in the resulting list should be in the same order as the original list.
    
    Example: word_list_by_size(['a', 'at', 'axe', 'by'], 2) returns ['at','by']
    
    Precondition: words is a list of strings. size is a positive int.
    
    Enforced Precondition: words a list. size is a positive int."""
    
    assert type(words) == list, `words`+' is not a list'
    assert type(size) == int and size >= 0, `size`+'is not a positive integer'
    
    thelist = []
    
    for x in words:
        if len(x) == size:
            thelist.append(x)
    
    return thelist


def word_list_extend(words, prefix):
    """Returns the word list that is the result of adding prefix to the start of 
    every word in the list words.
    
    The resulting word list is sorted alphabetically.
    
    Example: word_list_extend(['at', 'rap'], 'c') returns ['cat', 'crap'].
    
    Precondition: words is a list of strings. prefix is a string.
    
    Enforced Precondition: words is a list. prefix is a string."""
    
    assert type(words) == list, `words`+' is not a list'
    assert type(prefix) == str, `prefix`+' is not a string'
    
    thelist = []
    
    for x in words:
        word = prefix + x
        thelist.append(word)
    thelist.sort()
    
    return thelist


# Task 2: Prefix Maps

def pmap_add_word(pmap,word):
    """Adds a single word to a prefix map.
    
    This is a procedure.  It modifies the contents of pmap. It does not return.
    a new prefix map.  
    
    This function will add the word AND all of its prefixes to pmap.  For each
    prefix it will add the next letter to the list of values.  For the complete word, 
    it will add '' to the list of values. 
    
    This function does not add duplicates to the prefix map.  If a letter is already
    in the list for a given prefix map, then it will not add it a second time.
    
    Example: If pmap is the empty map {}, then pmap_add_word(pmap,'at') changes
    pmap to the dictionary { '':['a'], 'a':['t'], 'at':[''] }.

    Example: If pmap is { '':['a'], 'a':['t'], 'at':[''] }, pmap_add_word(pmap,'as') 
    changes pmap to { '':['a'], 'a':['s', 't'], 'at':[''], 'as':[''] }.
    
    Precondition: pmap is a prefix map.  word is a string with only letters.
    
    Enforced Precondition: pmap is a dict. word is a string with only letters."""
    
    assert type(pmap) == dict, `pmap` + ' is not of type dict'
    assert type(word) == str, `word` + ' is not a string'
    assert word.isalpha() == True, `word`+' needs to be only letters'
    
    
    """if not word in pmap:
        for x in word:
            pos = word.find(x)
            beginning = word[:pos]
            end = word[pos]
            if beginning in pmap:
                if not end in pmap[beginning]:
                    pmap[beginning].append(end)
            else:
                pmap[beginning] = list(end)
        pmap[word] = ['']
    if not '' in pmap[word]:
        pmap[word].append('')"""
        
    
    if not word in pmap:
        for index, x in enumerate(word):
            pos = index
            beginning = word[:pos]
            end = word[pos]
            if beginning in pmap:
                if not end in pmap[beginning]:
                    pmap[beginning].append(end)
            else:
                pmap[beginning] = list(end)
        pmap[word] = ['']
    if not '' in pmap[word]:
        pmap[word].append('')

    #what about words w/ double letters like goop, well, larry?

def word_list_to_pmap(words):
    """Returns the prefix map for the given word list.
    
    Hint: pmap_add_word is a useful helper function.
    
    Precondition: words is a list of strings with only letters.
    
    Enforced precondition: words is a list."""
    assert type(words) == list, `words` + ' is not a list'
    
    pmap = {}
    for x in words:
        pmap_add_word(pmap,x)
    return pmap


def pmap_to_word_list(pmap):
    """Returns the word list for the given prefix map.
    
    The word list should contain only those prefixes which have a next character
    of '' (the empty string) in the prefix map.
    
    Precondition: pmap is a prefix map.
    
    Enforced Precondition: pmap is a dict."""
    assert type(pmap) == dict, `pmap` + ' is not a dict'
    
    wordlist = []
    for key in pmap:
        if '' in pmap[key]:
            wordlist.append(key)
    return wordlist


def pmap_has_word(pmap,word):
    """Returns True if word is in the prefix map.
    
    Precondition: pmap is a prefix map.  word is a string.
    
    Enforced Precondition: pmap is a dict. word is a string."""
    assert type(pmap) == dict, `pmap` + ' is not a dict'
    assert type(word) == str, `word` + ' is not a string'
    
    if word in pmap and word != '':
        return True
    else:
        return False


# PART C: Word Completions

def autocomplete(prefix, pmap):
    """Returns the list of all words the complete prefix in pmap
    
    If there are no words completing prefix in pmap, this function returns the
    empty list.
    
    Example: If pmap is the prefix map created from 'short.txt', then 
    autocomplete('th',pmap) returns the list ['the', 'that'].  
    Similarly, autocomplete('x',pmap) returns the empty list []
    
    Precondition: prefix is a string that is either empty or has only letters. 
    pmap is a prefix map.
    
    Enforced Preconditions: We enforce the preconditions for prefix, but only
    enforce that pmap is a dict."""
    # This function will require recursion combined with a for-loop.  The base
    # case is when prefix is not in the prefix map.  Otherwise, you will need
    # to process all of the values in the list pmap[prefix].
    
    # Be careful with pmap[prefix]. If prefix is an actual word then '' is in this
    # list.  If you are not careful with your recursive call, then you will find
    # yourself in an infinite recursion.
    
    # NOTE: This function MUST be recurse, and you are not allowed to add any
    # helper functions to implement this function.
    
    assert type(prefix) == str, `prefix` + ' is not a string'
    assert len(prefix) == 0 or prefix.isalpha() == True,`prefix` + ' is not empty or only letters'
    assert type(pmap) == dict, `pmap` + ' is not a dict'

    if prefix != '' and (not pmap_has_word(pmap, prefix)):
        return []
    else:
        wordlist = []
        thelist = pmap[prefix]
        if thelist == ['']:
            return [prefix] 
        else:
            if '' in thelist:
                wordlist = [prefix]
                listcopy = thelist[:]
                listcopy.remove('')
                newlist = word_list_extend(listcopy, prefix)
            else:
                newlist = word_list_extend(thelist, prefix)
            for x in newlist:
                wordlist = wordlist + autocomplete(x,pmap)
            return wordlist


# PART D: Scrabble Puzzles

def scrabble(rack,size,pmap):
    """Returns the list of all valid words that you can form from the tile rack
    using EXACTLY size letters.
    
    The prefix map pmap is used to determine whether or not a word is valid.
    
    Example: If pmap is the prefix map created from 'short.txt', then 
    scrabble('theob',2,pmap) returns ['be', 'to'].
    
    Precondition: rack is a string that is either empty or has only letters. 
    size is a nonnegative integer. pmap is a prefix map.
   
    Enforced Precondition: We enforce the complete precondition for rack and size.
    We only enforce that pmap is a dict."""
    # We are not going to assert the preconditions here
    # We will let you do that in the helper function.
    return scrabble_helper('',rack,size,pmap)


def scrabble_helper(prefix,rack,size,pmap):
    """"Returns the list of all valid words extending prefix that you can form from
    the tile rack using EXACTLY size ADDITIONAL letters.
    
    The prefix map pmap is used to determine whether or not a word is valid.
    
    Example: If pmap is the prefix map created from 'short.txt', then 
    scrabble_helper('t','heob',1,pmap) returns ['to'], while 
    scrabble_helper('t','heob',2,pmap) returns ['the']

    Precondition: prefix and rack are a strings with only letters, but which may
    be empty. size is a nonnegative integer. pmap is a prefix map.
   
    Enforced Precondition: We enforce the complete precondition for prefix, rack, 
    and size. We only enforce that pmap is a dict."""
    # This function is to be implemented recursively using the process that was
    # described in the assignment overview.  At each recursive call, you will remove 
    # a letter from the rack and add it to the prefix.  Note that,  unlike scramble, 
    # size is not the number of letters in the word. It is the number of letters 
    # REMAINING to pick from the rack. So you must decrease it in the recursive call
    # as well.
    
    # This recursive function will have multiple base cases:
    
    #     1. size is 0 (so no letter left to pick)
    #     2. size > 0, but rack is empty (so there is nothing left to pick from)
    #     3. there are no words that complete prefix
    
    # In the case of 2 and 3, you should return the empty list.
    
    assert type(prefix) == str, `prefix` + ' is not a string'
    assert len(prefix) == 0 or prefix.isalpha() == True,`prefix` + ' is not empty or only letters'
    assert type(rack) == str, `rack` + ' is not a string'
    assert len(rack) == 0 or rack.isalpha() == True,`rack` + ' is not empty or only letters'
    assert type(size) == int and size >= 0, `size` + ' is not a non-negative integer'
    assert type(pmap) == dict, `pmap` + ' is not a dict'
    
    if size==0 or rack == '':
        return []
    else:
        scrabblelist = []
        autolist = autocomplete(prefix,pmap)
        wordlength = len(prefix) + size
        sizelist = word_list_by_size(autolist, wordlength)
        for x in rack:
            print 'pmap[prefix] is '+`pmap[prefix]`
            if x in pmap[prefix]:
                print `x`+' is in pmap[prefix]'
                newprefix = prefix + x
                print newprefix
                
                pos = rack.find(x)
                first = rack[:pos]
                last = rack[pos+1:]
                newrack = first + last
                print 'newrack is '+`newrack`
                
                newsize = size - 1
                if newprefix in sizelist:
                    print 'newprefix is in sizelist'
                    scrabblelist = scrabblelist + [newprefix]
                    print 'scrabblelist is ' + `scrabblelist`
                scrabblelist = scrabblelist + scrabble_helper(newprefix, newrack, newsize, pmap)
                print 'after recursion, scrabblelist is '+`scrabblelist`
        return scrabblelist


def match(template,pmap):
    """Returns the list of all valid words that match the given template.
    
    A template is a string combining letters and the '?' character.  A
    word is a match of for a template if it is the same length, and agrees
    with the template on every character that is not '?'. For example,
    'ate' matches the template 'a?e', as does 'axe'.
    
    The prefix map pmap is used to determine whether or not a word is valid.
    
    Example: If pmap is the prefix map created from 'short.txt', then 
    match('i?',pmap) returns ['in', 'it'].
    
    Precondition: template is a string of letters and '?'. pmap is a
    prefix map.
    
    Enforced Precondition: template is a string. pmap is a dict."""
    # We are not going to assert the preconditions here
    # We will let you do that in the helper function.
    return match_helper('',template,pmap)


def match_helper(prefix,template,pmap):
    """Returns the list of all valid words that start with the given prefix, and
    whose remaining letters match the given template.
    
    Unlike match, the template in this case is not supposed to match the whole
    string. It is only supposed to match the remaining part of the string after
    the prefix.
    
    Example: If pmap is the prefix map created from 'short.txt', then 
    match_helper('i','?',pmap) returns ['in', 'it'].
    
    Precondition: prefix is a string of letters or empty. template is either empty or
    string of letters and '?'. pmap is a prefix map.
    
    Enforced Precondition: prefix is a string of letters or empty. template is a string. 
    pmap is a dict."""
    # This function is to be implemented recursively using a process that is similar
    # to, but not the same as scrabble.  At each recursive call, you will remove
    # the first element from template.  If it is a letter, you add it to the prefix.
    # If it is a '?', you must try each valid extension of the prefix.
    
    # There are two base cases: when there are no word that complete the prefix, and 
    # when the template is empty.  In that second case, what you do depends on whether 
    # or not prefix is a word.
    
    assert (type(prefix) == str), `prefix` + ' is not a string'
    assert prefix.isalpha() or prefix == '', `prefix` + ' is not empty or all letters'
    assert type(template) == str, `template` + ' is not a string'
    assert type(pmap) == dict, `pmap` + ' is not a dict'
    
    matchlist = []
    autolist = autocomplete(prefix,pmap)
    wordlength = len(prefix) + len(template)
    #print 'wordlength is '+`wordlength`
    sizelist = word_list_by_size(autolist, wordlength)
    #print 'sizelist is'+`sizelist`
    
    if prefix not in pmap:
        return []
    if template == '':
        #print 'template is empty string'
        if prefix in sizelist:
            return [prefix]
        else:
            return []
        return matchlist
    elif template[0].isalpha():
        #print 'template[0] is letter'
        newprefix = prefix + template[0]
        #print 'newprefix is '+`newprefix`
        newtemplate = template[1:]
        matchlist = matchlist + match_helper(newprefix,newtemplate,pmap)
        return matchlist
    elif template[0] == '?':
        #print 'template[0] is ?'
        nextletterlist = pmap[prefix]
        copynll = nextletterlist[:]
        if '' in copynll:
            copynll.remove('')
        #print 'copynll is '+`copynll`
        for x in copynll:
            #print 'x is '+`x`
            newprefix = prefix + x
            #print 'newprefix is '+`newprefix`
            newtemplate = template[1:]
            matchlist = matchlist + match_helper(newprefix,newtemplate,pmap)
            #print 'matchlist is '+`matchlist`
        return matchlist
    
