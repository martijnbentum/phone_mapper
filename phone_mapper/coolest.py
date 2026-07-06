'''Phoneme set of the COOLEST dataset's textgrids.

Idiosyncratic to that dataset, not a general transcription standard.
See NOTES/baldey_coolest_aliases.md for the alias entries.
'''
from .mapper import _load_mapping_pair

name = 'coolest'

coolest_to_ipa, ipa_to_coolest = _load_mapping_pair(
    'coolest/coolest_to_ipa.json')
