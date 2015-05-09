# a4test.py
# Michelle Nelson, mhn29
# 11/2/14
""" Unit Test for Assignment A4"""
import cornelltest
import a4

# NEW ASSERT to help with testing

def assert_lists_equal(expected, received):
    """Helper function to verify that expected == received
    
    Because of how lists work, we cannot say
    
       cornelltest.assert_equals(expected, received)
    
    The lists are different folders and the contents may be in a 
    different order. So instead, we break this down into several 
    tests, which we put here.
    
    As always, we put the value that we expect on the  left, and the 
    value being tested on the right (in parameter received).
    
    Precondition: expected is a list"""
    # Check received is a list of the right length
    if list != type(received):
        msg = 'assert_lists_equal: '+`received`+' is not a list'
        cornelltest.quit_with_error(msg)
    
    if len(expected) != len(received):
        msg = ('assert_lists_equal: '+`received`+' does not have expected length'
                +`len(expected)`)
        cornelltest.quit_with_error(msg)
    
    # Check each of the contents of expected
    for item in expected:
        if not item in received:
            msg = 'assert_lists_equal: '+`received`+' is missing element '+`item`
            cornelltest.quit_with_error(msg)


# Test Procedures

def test_build_word_list():
    """Test function build_word_list"""
    print 'Testing build_word_list'
    words = a4.build_word_list('short.txt')
    expected = ['the', 'be','to','of','and','a','in','that','have','it']
    assert_lists_equal(expected, words)


def test_word_list_by_size():
    """Test function word_list_by_size"""
    print 'Testing word_list_by_size'
    # Make the word list
    words = ['the', 'be','to','of','and','a','in','that','have','it']
    
    # Call the function
    other = a4.word_list_by_size(words, 2)
    
    # Compare to what we expect
    expected = ['be','to','of','in','it']
    assert_lists_equal(expected, other)
    
    words = []
    other = a4.word_list_by_size(words,2)
    expected = []
    assert_lists_equal(expected, other)
    
    words = ['the', 'be','to','of','and','a','in','that','have','it']
    other = a4.word_list_by_size(words,0)
    expected = []
    assert_lists_equal(expected, other)
    
    words = ['the', 'be','to','of','and','a','in','that','have','it']
    other = a4.word_list_by_size(words,5)
    expected = []
    assert_lists_equal(expected, other)


def test_word_list_extend():
    """Test function word_list_extend"""
    print 'Testing word_list_extend'
    # Create a short word list
    words = ['o', 'at', 'ong']
    
    # Call the function
    other = a4.word_list_extend(words, 's')
    
    # Compare to what we expect
    expected = ['so','sat','song']
    assert_lists_equal(expected, other)
    
    # Verify that we DID NOT change words
    assert_lists_equal(['o', 'at', 'ong'], words)

    # Do this one more time with a prefix that is more than one letter
    other = a4.word_list_extend(words, 'pr')
    
    # Verify that we loaded the right number of words
    expected = ['pro','prat','prong']
    assert_lists_equal(expected, other)


def test_pmap_add_word():
    """Test function pmap_add_word"""
    print 'Testing pmap_add_word'
    
    # Start with an empty prefix map
    pmap = {}
    a4.pmap_add_word(pmap,'a')
    
    # Verify that pmap now has two keys (space and 'a')
    # Note use of helper to make this test easier to read
    cornelltest.assert_equals(2, len(pmap))
    cornelltest.assert_true('' in pmap)
    assert_lists_equal(['a'], pmap[''])
    cornelltest.assert_true('a' in pmap)
    assert_lists_equal([''], pmap['a'])
    
    # Add something with two letters
    a4.pmap_add_word(pmap,'by')
    
    # Verify the keys again
    cornelltest.assert_equals(4, len(pmap))
    cornelltest.assert_true('' in pmap)
    assert_lists_equal(['a','b'], pmap[''])
    cornelltest.assert_true('a' in pmap)
    assert_lists_equal([''], pmap['a'])
    cornelltest.assert_true('b' in pmap)
    assert_lists_equal(['y'], pmap['b'])
    cornelltest.assert_true('by' in pmap)
    assert_lists_equal([''], pmap['by'])
    
    # One last time with overlap
    a4.pmap_add_word(pmap,'at')
    
    # Verify the keys again
    cornelltest.assert_equals(5, len(pmap))
    cornelltest.assert_true('' in pmap)
    assert_lists_equal(['a','b'], pmap[''])
    cornelltest.assert_true('a' in pmap)
    assert_lists_equal(['','t'], pmap['a'])
    cornelltest.assert_true('at' in pmap)
    assert_lists_equal([''], pmap['at'])
    cornelltest.assert_true('b' in pmap)
    assert_lists_equal(['y'], pmap['b'])
    cornelltest.assert_true('by' in pmap)
    assert_lists_equal([''], pmap['by'])
    
    a4.pmap_add_word(pmap,'that')
    cornelltest.assert_true('that' in pmap)
    cornelltest.assert_true('' in pmap['that'])
    
    a4.pmap_add_word(pmap,'goop')
    cornelltest.assert_true('goop' in pmap)
    cornelltest.assert_true('o' in pmap['go'])
    cornelltest.assert_true('p' in pmap['goo'])


def test_word_list_to_pmap():
    """Test function word_list_to_pmap"""
    print 'Testing function word_list_to_pmap'
    
    # Start with an empty word list
    words = []
    pmap = a4.word_list_to_pmap(words)
    
    # Should be empty dictionary
    cornelltest.assert_equals(dict, type(pmap))
    cornelltest.assert_equals(0, len(pmap))
    
    # One word, two letters
    words = ['at']
    pmap = a4.word_list_to_pmap(words)
    
    # Similar test format to pmap_add_word
    cornelltest.assert_equals(3, len(pmap))
    assert_lists_equal(['a'], pmap[''])
    cornelltest.assert_true('a' in pmap)
    assert_lists_equal(['t'], pmap['a'])
    cornelltest.assert_true('at' in pmap)
    assert_lists_equal([''], pmap['at'])
    
    # Several words
    words = ['at', 'by', 'a']
    pmap = a4.word_list_to_pmap(words)
    
    # Similar test format to pmap_add_word
    cornelltest.assert_equals(5, len(pmap))
    cornelltest.assert_true('' in pmap)
    assert_lists_equal(['a','b'], pmap[''])
    cornelltest.assert_true('a' in pmap)
    assert_lists_equal(['','t'], pmap['a'])
    cornelltest.assert_true('at' in pmap)
    assert_lists_equal([''], pmap['at'])
    cornelltest.assert_true('b' in pmap)
    assert_lists_equal(['y'], pmap['b'])
    cornelltest.assert_true('by' in pmap)
    assert_lists_equal([''], pmap['by'])


def test_pmap_to_word_list():
    """Test function pmap_to_word_list"""
    print 'Testing function pmap_to_word_list'
    
    # Start with an empty prefix map
    pmap = {}
    words = a4.pmap_to_word_list(pmap)
    
    # Should be empty list
    cornelltest.assert_equals(list, type(words))
    cornelltest.assert_equals(0, len(words))
    
    # Build a pmap manually
    pmap = { '':['a'], 'a':['','t'], 'at':[''] }
    words =  a4.pmap_to_word_list(pmap)
    assert_lists_equal(['a', 'at'], words)
    
    # See if we can go back and forth
    expected = ['the', 'be','to','of','and','a','in','that','have','it']
    pmap  = a4.word_list_to_pmap(expected)
    words = a4.pmap_to_word_list(pmap)
    assert_lists_equal(expected, words)


def test_pmap_has_word():
    """Test function pmap_has_word"""
    print 'Testing function pmap_has_word'
    
    # Start with an empty prefix map
    pmap = {}
    cornelltest.assert_false(a4.pmap_has_word(pmap, 'a'))
    
    # Build a pmap manually
    pmap = { '':['a'], 'a':['','t'], 'at':[''] }
    cornelltest.assert_false(a4.pmap_has_word(pmap, '')) # NOT A WORD
    cornelltest.assert_false(a4.pmap_has_word(pmap, 'by'))
    cornelltest.assert_true(a4.pmap_has_word(pmap, 'a'))
    cornelltest.assert_true(a4.pmap_has_word(pmap, 'at'))


def test_autocomplete():
    """Test search function autocomplete"""
    print 'Testing function autocomplete'
    
    pmap = {}
    
    words = a4.autocomplete('a',pmap)
    assert_lists_equal([], words)
    
    pmap = { '':['a'], 'a':['']}
    
    words = a4.autocomplete('a',pmap)
    assert_lists_equal(['a'], words)
    words = a4.autocomplete('',pmap)
    assert_lists_equal(['a'], words)
    words = a4.autocomplete('m',pmap)
    assert_lists_equal([], words)
    
    pmap = { '':['a'], 'a':['','t'], 'at':[''] }
    
    words = a4.autocomplete('a',pmap)
    assert_lists_equal(['a','at'], words)
    words = a4.autocomplete('at',pmap)
    assert_lists_equal(['at'], words)
    
    pmap = { '':['a'], 'a':['','t','r'], 'at':[''], 'ar':['e'], 'are':[''] }
    words = a4.autocomplete('ar',pmap)
    assert_lists_equal(['are'], words)
    words = a4.autocomplete('a',pmap)
    assert_lists_equal(['a','at','are'], words)
    words = a4.autocomplete('aren',pmap)
    assert_lists_equal([], words)
    
    pmap = { '':['a'], 'a':['','t','r'], 'at':['','e'], 'ate':[''], 'ar':['e'], 'are':[''] }
    words = a4.autocomplete('at',pmap)
    assert_lists_equal(['at','ate'], words)

def test_scrabble():
    """Test search function scrabble"""
    print 'Testing function scrabble'
    
    wordlist = ['the','be','to','of','a','and','in','that','have','it']
    pmap = a4.word_list_to_pmap(wordlist)
    
    words = a4.scrabble('eavhi',4,pmap)
    assert_lists_equal(['have'], words)
    
    words = a4.scrabble('',4,pmap)
    assert_lists_equal([], words)
    
    words = a4.scrabble('eavhi',0,pmap)
    assert_lists_equal([], words)
    
    words = a4.scrabble('ebht',3,pmap)
    assert_lists_equal(['the'], words)
    
    words = a4.scrabble('tinfoeb',2,pmap)
    assert_lists_equal(['be','to','of','in','it'], words)
    
    words = a4.scrabble('eavhi',5,pmap)
    assert_lists_equal([], words)
    
    words = a4.scrabble('abcde',1,pmap)
    assert_lists_equal(['a'], words)
    
    words = a4.scrabble('veha',4,pmap)
    assert_lists_equal(['have'], words)
    

def test_match():
    """Test search function match"""
    print 'Testing function match'
    
    wordlist = ['the','be','to','of','a','and','in','that','have','it']
    pmap = a4.word_list_to_pmap(wordlist)
    
    words = a4.match('?',pmap)
    assert_lists_equal(['a'], words)
    
    words = a4.match('???',pmap)
    assert_lists_equal(['the','and'], words)
    
    words = a4.match('???t',pmap)
    assert_lists_equal(['that'], words)
    
    words = a4.match('b???',pmap)
    assert_lists_equal([], words)
    
    words = a4.match('a?d',pmap)
    assert_lists_equal(['and'], words)
    
    words = a4.match('that',pmap)
    assert_lists_equal(['that'], words)
    
    words = a4.match('a??',pmap)
    assert_lists_equal(['and'], words)
    
    wordlist = ['ate','are','ale','axe','axes']
    pmap = a4.word_list_to_pmap(wordlist)
    
    words = a4.match('a?e',pmap)
    assert_lists_equal(['ate','are','ale','axe'], words)


# Application Code
if __name__ == "__main__":
    # Part A
    test_build_word_list()
    test_word_list_by_size()
    test_word_list_extend()

    # Part B
    test_pmap_add_word()
    test_word_list_to_pmap()
    test_pmap_to_word_list()
    test_pmap_has_word()
    
    # Part C
    test_autocomplete()
    
    # Part D
    test_scrabble()
    test_match()
    print "Module a4 is working correctly"
