'''Phoneme set of the CGN (Corpus Gesproken Nederlands) annotations.

Dataset-linked rather than a general transcription standard.
'''
from .mapper import _load_mapping_pair

name = 'cgn'

cgn_to_ipa, ipa_to_cgn = _load_mapping_pair('cgn/cgn_to_ipa.json')
