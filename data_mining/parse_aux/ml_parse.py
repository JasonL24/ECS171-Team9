"""Helper Parsing Functions for ML Team"""
import numpy as np


def random_select_batch(file: list, x_size: int, y_size: int, batch_size: int = 1) -> np.array:
    """ randomly select batch_size number of samples of each x_size + y_size

    :param file: target song to parse
    :param x_size: size of encoder
    :param y_size: size of decoder
    :param batch_size:
    :return: a list of randomly selected batch size input
    """
    pass


def fill_notes(notes: list, target_size: int):
    """ Given a list of notes, fill the list to target list length

    :param notes: list of notes
    :param target_size: target_size to fill
    :return: return list of notes with target size
    """
    pass


def trim_notes(notes: list, target_size: int):
    """ Given a list of notes, trim to target size by dropping the last the notes

    :param notes: list of notes
    :param target_size: target size
    :return: return list of notes with target size
    """
    pass


def build_song(song):
    """ given a list of notes, return the song of these notes.

    :param song:
    :return: a MIDI file of the given song
    """
    pass