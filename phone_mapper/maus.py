'''Phoneme sets of BAS WebMAUS alignments, one table per language.

Keys of maus_sampa_to_ipa are the symbols MAUS writes in its SAMPA output
(TextGrid tiers MAU, MAS, KAN-MAU). They are not always strict SAMPA:
palatalised consonants are written d_j, ts_j where SAMPA uses d', ts'.
Values are the IPA symbols WebMAUS gives for OUTSYMBOL=ipa, including the
non-speech labels (...) for pauses, (..) for human noise and (.) for
non-human noise.

Tables are keyed by ISO 639-3 code: nld, eng, fra, deu, hun, ita, pol, spa.
English is the union of the us, gb, au, nz and sc variant tables, which
agree on every shared symbol.

ipa_to_maus_sampa is not a strict inverse: several MAUS symbols can share
one IPA symbol (<p:>, <p> and < all map to (...)). It names the first symbol
in BAS table order (English: us, gb, au, nz, sc).

Built from the BAS tables in data_sources/maus/ by
scripts/build_maus_maps.py.
'''
from .mapper import _load_json

name = 'maus'

languages = ('nld', 'eng', 'fra', 'deu', 'hun', 'ita', 'pol', 'spa')


def _load_tables():
    '''Load forward and inverse tables for every language.'''
    forward, inverse = {}, {}
    for language in languages:
        data = _load_json(f'maus/{language}.json')
        forward[language] = data['maus_sampa_to_ipa']
        inverse[language] = data['ipa_to_maus_sampa']
    return forward, inverse


maus_sampa_to_ipa, ipa_to_maus_sampa = _load_tables()
