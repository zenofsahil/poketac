from pokeapi.utils import remove_nonprintable_chars

def test_remove_nonprintable_chars():
    test_string = 'When several of\nthese POKéMON\ngather, their\x0celectricity could\nbuild and cause\nlightning storms.'
    output_string = 'When several of these POKéMON gather, their electricity could build and cause lightning storms.'

    assert remove_nonprintable_chars(test_string) == output_string

