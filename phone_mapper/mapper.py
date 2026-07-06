import json
from pathlib import Path

_DATA = Path(__file__).parent / 'data'

class Mapper:
    '''Map phonemes between IPA, SAMPA, CELEX, DISC, CGN, and ARPAbet.'''
    def __init__(self):
        self.ipa_set = list(ipa_set)
        self.sampa_set = list(sampa_set)
        self.celex_set = list(celex_set)
        self.disc_set = list(disc_set)
        self.ipa_to_example_words_dutch = dict(ipa_to_example_words_dutch)
        self.ipa_to_example_words_english = dict(ipa_to_example_words_english)
        self.ipa_to_example_words_german = dict(ipa_to_example_words_german)
        self.ipa_to_sampa = dict(ipa_to_sampa)
        self.sampa_to_ipa = dict(sampa_to_ipa)
        self.ipa_to_celex = dict(ipa_to_celex)
        self.celex_to_ipa = dict(celex_to_ipa)
        self.ipa_to_disc = dict(ipa_to_disc)
        self.disc_to_ipa = dict(disc_to_ipa)
        self._load_cgn()
        self._add_arpabet()
        self._add_baldey()
        self._add_coolest()

    def _load_cgn(self):
        cgn_fwd, cgn_inv = _load_mapping_pair('dutch/cgn_to_ipa.json')
        self.cgn_to_ipa = cgn_fwd
        self.ipa_to_cgn = cgn_inv
        self.cgn_set = list(cgn_fwd.keys())

    def _add_arpabet(self):
        self.arpabet_to_ipa = dict(arpabet_to_ipa)
        self.ipa_to_arpabet = dict(ipa_to_arpabet)
        self.arpabet_to_example_words = dict(arpabet_to_example_words)
        arpabet_fwd, arpabet_inv = _load_mapping_pair(
            'english/arpabet_to_disc.json')
        self.arpabet_to_disc = arpabet_fwd
        self.disc_to_arpabet = arpabet_inv

    def _add_baldey(self):
        '''Add Baldey textgrid phoneme set (restricted CGN-based set).'''
        baldey_fwd, baldey_inv = _load_mapping_pair('dutch/baldey_to_ipa.json')
        self.baldey_to_ipa = baldey_fwd
        self.ipa_to_baldey = baldey_inv
        self.baldey_to_disc = {b: self.ipa_to_disc[i]
            for b, i in baldey_fwd.items() if i in self.ipa_to_disc}
        self.disc_to_baldey = {v: k for k, v in self.baldey_to_disc.items()}
        self.baldey_textgrid_phoneme_set = list(baldey_fwd.keys())

    def _add_coolest(self):
        '''Add COOLEST textgrid phoneme set.'''
        coolest_fwd, _ = _load_mapping_pair('dutch/coolest_to_ipa.json')
        self.coolest_to_ipa = coolest_fwd
        self.coolest_textgrid_phoneme_set = list(coolest_fwd.keys())


def _load_json(path):
    return json.loads((_DATA / path).read_text())


def _load_mapping_pair(path):
    '''Load a JSON file with named forward and inverse mapping dicts.'''
    data = _load_json(path)
    forward = Path(path).stem
    a, b = forward.split('_to_')
    inverse = f'{b}_to_{a}'
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

celex_dutch_phoneme_set = _load_json('dutch/celex_phone_set.json')

ipa_to_example_words_dutch = _load_json('dutch/ipa_to_example_words.json')
ipa_to_example_words_english = _load_json('english/ipa_to_example_words.json')
ipa_to_example_words_german = _load_json('german/ipa_to_example_words.json')

_arpabet = _load_json('english/arpabet_to_ipa.json')
arpabet_to_ipa = _arpabet['arpabet_to_ipa']
ipa_to_arpabet = _arpabet['ipa_to_arpabet']
arpabet_to_example_words = _arpabet['arpabet_to_example_words']





def counts(mapper=None):
    '''Return entry counts for the main phoneme sets.'''
    if not mapper: mapper = Mapper()
    return {
        'ipa_set': len(mapper.ipa_set),
        'sampa_set': len(mapper.sampa_set),
        'celex_set': len(mapper.celex_set),
        'disc_set': len(mapper.disc_set),
        'cgn_set': len(mapper.cgn_set),
    }


def validate(mapper=None):
    '''Check mapping invariants, return a list of problem descriptions.'''
    if not mapper: mapper = Mapper()
    problems = []
    pairs = [
        ('sampa', mapper.sampa_to_ipa, mapper.ipa_to_sampa),
        ('celex', mapper.celex_to_ipa, mapper.ipa_to_celex),
        ('disc', mapper.disc_to_ipa, mapper.ipa_to_disc),
        ('cgn', mapper.cgn_to_ipa, mapper.ipa_to_cgn),
    ]
    for name, fwd, inv in pairs:
        for symbol, ipa in fwd.items():
            if inv.get(ipa) != symbol:
                problems.append(
                    f'{name}: {symbol} -> {ipa} -> {inv.get(ipa)}')
        for ipa, symbol in inv.items():
            if fwd.get(symbol) != ipa:
                problems.append(
                    f'{name} inverse: {ipa} -> {symbol} -> {fwd.get(symbol)}')
    for ipa in mapper.ipa_set:
        if ipa not in ipa_to_definition:
            problems.append(f'no definition for {ipa}')
    for ipa, arpabet in mapper.ipa_to_arpabet.items():
        if arpabet not in mapper.arpabet_to_ipa:
            problems.append(f'unknown arpabet code {arpabet} for {ipa}')
    for arpabet, disc in mapper.arpabet_to_disc.items():
        if arpabet not in mapper.arpabet_to_ipa:
            problems.append(f'arpabet_to_disc: unknown code {arpabet}')
        if disc not in mapper.disc_to_ipa:
            problems.append(f'arpabet_to_disc: unknown disc {disc}')
    for disc, arpabet in mapper.disc_to_arpabet.items():
        if disc not in mapper.disc_to_ipa:
            problems.append(f'disc_to_arpabet: unknown disc {disc}')
        if arpabet not in mapper.arpabet_to_ipa:
            problems.append(f'disc_to_arpabet: unknown code {arpabet}')
    return problems


def show(mapper=None):
    '''Print IPA/SAMPA/CELEX/DISC/CGN side by side, one phoneme per row.'''
    if not mapper: mapper = Mapper()
    for ipa in mapper.ipa_set:
        sampa = mapper.ipa_to_sampa.get(ipa, '')
        celex = mapper.ipa_to_celex.get(ipa, '')
        disc  = mapper.ipa_to_disc.get(ipa, '')
        cgn   = mapper.ipa_to_cgn.get(ipa, '')
        row = [str(x).ljust(6) for x in (ipa, sampa, celex, disc, cgn)]
        print('\t'.join(row))
