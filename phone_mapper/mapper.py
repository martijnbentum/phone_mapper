import json
from pathlib import Path

_DATA = Path(__file__).parent / 'data'


def _load(path):
    return json.loads((_DATA / path).read_text())


def _load_both(path):
    '''Load a JSON file containing two directional dicts, return as a tuple.'''
    data = _load(path)
    keys = list(data.keys())
    return data[keys[0]], data[keys[1]]


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
        self.ipa_set = ipa_set
        self.sampa_set = sampa_set
        self.celex_set = celex_set
        self.disc_set = disc_set
        self.ipa_to_example_words_dutch = ipa_to_example_words_dutch
        self.ipa_to_example_words_english = ipa_to_example_words_english
        self.ipa_to_example_words_german = ipa_to_example_words_german
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
        self.arpabet_to_ipa = arpabet_to_ipa
        self.ipa_to_arpabet = ipa_to_arpabet
        self.arpabet_to_example_words = arpabet_to_example_words
        self.arpabet_to_disc = {}
        self.disc_to_arpabet = {}
        for ipa, disc in self.ipa_to_disc.items():
            mapped = ipa
            if mapped == '*': mapped = 'r'
            if mapped == 'iː': mapped = 'i'
            if mapped == 'uː': mapped = 'u'
            if mapped == 'ɑɪ': mapped = 'ai'
            if mapped == 'ɑ̃ː': mapped = 'ɑː'
            if mapped == 'ɒ': mapped = 'ɔ'
            if mapped == 'ɔ̃': mapped = 'ɔ'
            if mapped == 'æ̃ː': mapped = 'æ̃'
            if mapped == 'ŋ̩': mapped = 'ŋ'
            if mapped not in self.ipa_to_arpabet:
                continue
            arpabet = self.ipa_to_arpabet[mapped]
            self.arpabet_to_disc[arpabet] = disc
            self.disc_to_arpabet[disc] = arpabet

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


def validate(mapper=None):
    '''Return entry counts for the main phoneme sets.'''
    if not mapper: mapper = Mapper()
    return {
        'ipa_set': len(mapper.ipa_set),
        'sampa_set': len(mapper.sampa_set),
        'celex_set': len(mapper.celex_set),
        'disc_set': len(mapper.disc_set),
        'cgn_set': len(mapper.cgn_set),
    }


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
