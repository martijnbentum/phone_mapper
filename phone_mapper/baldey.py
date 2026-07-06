'''Phoneme set of the Baldey dataset's textgrids.

Idiosyncratic to that dataset (a restricted CGN-based set), not a
general transcription standard. See NOTES/baldey_coolest_aliases.md
for the alias entries.
'''
from .mapper import _load_mapping_pair

name = 'baldey'

baldey_to_ipa, ipa_to_baldey = _load_mapping_pair('baldey/baldey_to_ipa.json')
baldey_to_disc, disc_to_baldey = _load_mapping_pair(
    'baldey/baldey_to_disc.json')
