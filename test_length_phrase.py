import pytest


def test_length_phrase():
    phrase = input("Set a phrase: ")
    phrase_length = len(phrase)
    assert phrase_length < 15, "Phrase consists more than 15 symbols"