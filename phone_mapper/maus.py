'''Phoneme sets of BAS WebMAUS alignments, one table per language.

Keys are the symbols MAUS writes in its SAMPA output (TextGrid tiers MAU,
MAS, KAN-MAU). They are not always strict SAMPA: palatalised consonants are
written d_j, ts_j where SAMPA uses d', ts'.

Three tables per language, keyed by ISO 639-3 code (nld, eng, fra, deu,
hun, ita, pol, spa):

- bas_maus_sampa_to_ipa: the BAS tables as published. Their IPA is the
  generic meaning of each symbol across languages, e.g. R is always the
  uvular trill and r the alveolar trill.
- maus_sampa_to_ipa: the table to use. BAS IPA with reviewed corrections
  for what a symbol stands for in that language (English R and r -> ɹ,
  Spanish r -> ɾ, Polish s_j -> ɕ, ...; see
  data_sources/maus/corrections_<iso>.tsv for each fix and its evidence),
  then normalised notation: NFC, tie bars on affricates (t͡ʃ, t͡s),
  palatalisation before length (tʲː). It also holds a few symbols that
  are not in BAS but are written by corpus fixes (English @` = ɚ, see
  the corrections file; German 6_^ = ɐ̯). Non-speech labels: (...) pause,
  (..) human noise, (.) non-human noise.
- ipa_to_maus_sampa: inverse of maus_sampa_to_ipa. Not a strict inverse:
  several MAUS symbols can share one IPA symbol (<p:>, <p> and < all map
  to (...); English R, r and r\\ all map to ɹ). It names the first symbol
  in BAS table order (English: us, gb, au, nz, sc).

English is the union of the us, gb, au, nz and sc variant tables, which
agree on every shared symbol.

Built from data_sources/maus/ by scripts/build_maus_maps.py.
'''
from .mapper import _load_json

name = 'maus'

languages = ('nld', 'eng', 'fra', 'deu', 'hun', 'ita', 'pol', 'spa')


def _load_tables():
    '''Load the three tables for every language.'''
    forward, inverse, bas = {}, {}, {}
    for language in languages:
        data = _load_json(f'maus/{language}.json')
        forward[language] = data['maus_sampa_to_ipa']
        inverse[language] = data['ipa_to_maus_sampa']
        bas[language] = data['bas_maus_sampa_to_ipa']
    return forward, inverse, bas


maus_sampa_to_ipa, ipa_to_maus_sampa, bas_maus_sampa_to_ipa = _load_tables()
