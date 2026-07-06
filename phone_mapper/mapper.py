import json
from pathlib import Path

_DATA = Path(__file__).parent / 'data'


class Mapper:
    '''Map phonemes between the IPA, SAMPA, CELEX, and DISC
    transcription systems, with example words per language.
    Language- and dataset-specific phoneme sets (ARPAbet, CGN, Baldey,
    COOLEST, diphone) live in their own modules.
    '''
    def __init__(self):
        self.ipa_set = list(ipa_set)
        self.sampa_set = list(sampa_set)
        self.celex_set = list(celex_set)
        self.disc_set = list(disc_set)
        self.ipa_to_sampa = dict(ipa_to_sampa)
        self.sampa_to_ipa = dict(sampa_to_ipa)
        self.ipa_to_celex = dict(ipa_to_celex)
        self.celex_to_ipa = dict(celex_to_ipa)
        self.ipa_to_disc = dict(ipa_to_disc)
        self.disc_to_ipa = dict(disc_to_ipa)
        self.ipa_to_example_words = {language: dict(words)
            for language, words in ipa_to_example_words.items()}


def _load_json(path):
    return json.loads((_DATA / path).read_text())


def _mapping_pair_keys(stem):
    '''Return the forward and inverse dict names for a mapping file stem.'''
    parts = stem.split('_to_')
    if len(parts) != 2:
        raise ValueError(f'cannot derive an inverse name from {stem!r}')
    a, b = parts
    return stem, f'{b}_to_{a}'


def _load_mapping_pair(path):
    '''Load a JSON file with named forward and inverse mapping dicts.'''
    data = _load_json(path)
    forward, inverse = _mapping_pair_keys(Path(path).stem)
    return data[forward], data[inverse]


# ── public data ────────────────────────────────────────────────────────────
ipa_to_definition = _load_json('ipa_to_definition.json')
ipa_set = list(ipa_to_definition.keys())

sampa_to_ipa, ipa_to_sampa = _load_mapping_pair('sampa_to_ipa.json')
sampa_set = list(sampa_to_ipa.keys())

celex_to_ipa, ipa_to_celex = _load_mapping_pair('celex_to_ipa.json')
celex_set = list(celex_to_ipa.keys())

disc_to_ipa, ipa_to_disc = _load_mapping_pair('disc_to_ipa.json')
disc_set = list(disc_to_ipa.keys())

ipa_to_example_words = _load_json('ipa_to_example_words.json')


def counts(mapper=None):
    '''Return entry counts for the phoneme sets.'''
    from . import arpabet, baldey, cgn, coolest
    if not mapper: mapper = Mapper()
    return {
        'ipa_set': len(mapper.ipa_set),
        'sampa_set': len(mapper.sampa_set),
        'celex_set': len(mapper.celex_set),
        'disc_set': len(mapper.disc_set),
        'arpabet_set': len(arpabet.arpabet_to_ipa),
        'baldey_set': len(baldey.baldey_to_ipa),
        'cgn_set': len(cgn.cgn_to_ipa),
        'coolest_set': len(coolest.coolest_to_ipa),
    }


def show(mapper=None):
    '''Print IPA/SAMPA/CELEX/DISC/CGN/ARPAbet side by side, one phoneme
    per row.
    '''
    from .arpabet import ipa_to_arpabet
    from .cgn import ipa_to_cgn
    if not mapper: mapper = Mapper()
    for ipa in mapper.ipa_set:
        sampa = mapper.ipa_to_sampa.get(ipa, '')
        celex = mapper.ipa_to_celex.get(ipa, '')
        disc  = mapper.ipa_to_disc.get(ipa, '')
        cgn   = ipa_to_cgn.get(ipa, '')
        arpabet = ipa_to_arpabet.get(ipa, '')
        row = [str(x).ljust(6)
            for x in (ipa, sampa, celex, disc, cgn, arpabet)]
        print('\t'.join(row))
