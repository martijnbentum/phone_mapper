'''ARPAbet phoneme set for American English.

Tied to the American-English tradition (ARPA, CMUdict), not a
cross-language transcription system.
'''
from .mapper import _load_json, _load_mapping_pair

name = 'arpabet'

arpabet_to_ipa, ipa_to_arpabet = _load_mapping_pair(
    'arpabet/arpabet_to_ipa.json')
arpabet_to_disc, disc_to_arpabet = _load_mapping_pair(
    'arpabet/arpabet_to_disc.json')
arpabet_to_example_words = _load_json('arpabet/arpabet_to_example_words.json')
