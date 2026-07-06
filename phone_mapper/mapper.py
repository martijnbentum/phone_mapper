import json
from pathlib import Path

_DATA = Path(__file__).parent / 'data'


def _load(path):
    return json.loads((_DATA / path).read_text())


def _load_both(path):
    '''Load a JSON file with named forward and inverse mapping dicts.'''
    data = _load(path)
    forward = Path(path).stem
    a, b = forward.split('_to_')
    inverse = f'{b}_to_{a}'
    return data[forward], data[inverse]


# ── public data ────────────────────────────────────────────────────────────
ipa_to_definition = _load('ipa_to_definition.json')
ipa_set = list(ipa_to_definition.keys())

sampa_to_ipa, ipa_to_sampa = _load_both('sampa_to_ipa.json')
sampa_set = list(sampa_to_ipa.keys())

celex_to_ipa, ipa_to_celex = _load_both('celex_to_ipa.json')
celex_set = list(celex_to_ipa.keys())

disc_to_ipa, ipa_to_disc = _load_both('disc_to_ipa.json')
disc_set = list(disc_to_ipa.keys())

celex_dutch_phoneme_set = _load('dutch/celex_phone_set.json')

ipa_to_example_words_dutch = _load('dutch/ipa_to_example_words.json')
ipa_to_example_words_english = _load('english/ipa_to_example_words.json')
ipa_to_example_words_german = _load('german/ipa_to_example_words.json')

_arpabet = _load('english/arpabet_to_ipa.json')
arpabet_to_ipa = _arpabet['arpabet_to_ipa']
ipa_to_arpabet = _arpabet['ipa_to_arpabet']
arpabet_to_example_words = _arpabet['arpabet_to_example_words']

# ── diphone/recode helpers (used by external tooling) ─────────────────────
phonemes = 'I E A O } @ i a u y e | o K L M'
phonemes += ' p b t d k g N m n l r f v s z S Z j x h w _'
phonemes = phonemes.split()

rewrite_dict = {'|': 'eu', '_': 'J', '@': 'V', '}': 'U'}

recode_dict = {
    'I': 'ih', 'E': 'eh', 'A': 'ah', 'O': 'oh', 'U': 'uh', 'V': 'vh',
    'K': 'ei', 'L': 'ui', 'M': 'au', 'N': 'ng', 'S': 'sh', 'Z': 'zh',
    'G': 'gx', 'J': 'dj',
}


class Mapper:
    '''Map phonemes between IPA, SAMPA, CELEX, DISC, CGN, and ARPAbet.
    language:    target language for _fix_w correction ('dutch' default)
    '''
    def __init__(self, language='dutch'):
        self.language = language
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
        if self.language != 'dutch':
            self._fix_w()
        self._add_baldey()
        self._add_coolest()

    def _load_cgn(self):
        cgn_fwd, cgn_inv = _load_both('dutch/cgn_to_ipa.json')
        self.cgn_to_ipa = cgn_fwd
        self.ipa_to_cgn = cgn_inv
        self.cgn_set = list(cgn_fwd.keys())

    def _add_arpabet(self):
        self.arpabet_to_ipa = dict(arpabet_to_ipa)
        self.ipa_to_arpabet = dict(ipa_to_arpabet)
        self.arpabet_to_example_words = dict(arpabet_to_example_words)
        arpabet_fwd, arpabet_inv = _load_both('english/arpabet_to_disc.json')
        self.arpabet_to_disc = arpabet_fwd
        self.disc_to_arpabet = arpabet_inv

    def _fix_w(self):
        '''Remap /w/ to /ʋ/ for non-Dutch languages.'''
        self.celex_to_ipa['w'] = 'ʋ'
        self.sampa_to_ipa['w'] = 'ʋ'
        self.disc_to_ipa['w'] = 'ʋ'

    def _add_baldey(self):
        '''Add Baldey textgrid phoneme set (restricted CGN-based set).'''
        baldey_fwd, baldey_inv = _load_both('dutch/baldey_to_ipa.json')
        self.baldey_to_ipa = baldey_fwd
        self.ipa_to_baldey = baldey_inv
        self.baldey_to_disc = {b: self.ipa_to_disc[i]
            for b, i in baldey_fwd.items() if i in self.ipa_to_disc}
        self.disc_to_baldey = {v: k for k, v in self.baldey_to_disc.items()}
        self.baldey_textgrid_phoneme_set = list(baldey_fwd.keys())

    def _add_coolest(self):
        '''Add COOLEST textgrid phoneme set.'''
        coolest_fwd, _ = _load_both('dutch/coolest_to_ipa.json')
        self.coolest_to_ipa = coolest_fwd
        self.coolest_textgrid_phoneme_set = list(coolest_fwd.keys())


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


# Convenience lookups
_default_mapper = Mapper()
disc_to_ipa = _default_mapper.disc_to_ipa

to_ipa_org = {disc: disc_to_ipa[disc] for disc in phonemes}
to_ipa_org['-'] = to_ipa_org['_']
to_ipa_rew = {rewrite_dict.get(k, k): v for k, v in to_ipa_org.items()}
to_ipa = {recode_dict.get(k, k): v for k, v in to_ipa_rew.items()}
to_ipa['gx'] = 'ɣ'
