import json
from pathlib import Path

_DATA = Path(__file__).parent / 'data'

class Mapper:
    '''Map phonemes between IPA, SAMPA, CELEX, DISC, CGN, and ARPAbet.
    General mappings are attributes; language-specific mappings live in
    the dutch, english, and german sub-namespaces.
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
        self.dutch = Language('dutch')
        self.english = Language('english')
        self.german = Language('german')


class Language:
    '''Namespace for the language-specific mappings in one data folder.
    Each JSON file becomes attributes named after its stem; a file
    named x_to_y.json provides both the x_to_y and y_to_x dicts.
    '''
    def __init__(self, name):
        self.name = name
        for path in sorted((_DATA / name).glob('*.json')):
            self._add(path)

    def _add(self, path):
        data = json.loads(path.read_text())
        stem = path.stem
        if isinstance(data, dict) and stem in data:
            forward, inverse = _mapping_pair_keys(stem)
            setattr(self, forward, data[forward])
            setattr(self, inverse, data[inverse])
        else:
            setattr(self, stem, data)

    def __repr__(self):
        names = [k for k in vars(self) if k != 'name']
        return f'<Language {self.name}: {", ".join(names)}>'


def _load_json(path):
    return json.loads((_DATA / path).read_text())


def _mapping_pair_keys(stem):
    '''Return the forward and inverse dict names for a mapping file stem.'''
    a, b = stem.split('_to_')
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


def counts(mapper=None):
    '''Return entry counts for the main phoneme sets.'''
    if not mapper: mapper = Mapper()
    return {
        'ipa_set': len(mapper.ipa_set),
        'sampa_set': len(mapper.sampa_set),
        'celex_set': len(mapper.celex_set),
        'disc_set': len(mapper.disc_set),
        'cgn_set': len(mapper.dutch.cgn_to_ipa),
    }


def show(mapper=None):
    '''Print IPA/SAMPA/CELEX/DISC/CGN side by side, one phoneme per row.'''
    if not mapper: mapper = Mapper()
    for ipa in mapper.ipa_set:
        sampa = mapper.ipa_to_sampa.get(ipa, '')
        celex = mapper.ipa_to_celex.get(ipa, '')
        disc  = mapper.ipa_to_disc.get(ipa, '')
        cgn   = mapper.dutch.ipa_to_cgn.get(ipa, '')
        row = [str(x).ljust(6) for x in (ipa, sampa, celex, disc, cgn)]
        print('\t'.join(row))
