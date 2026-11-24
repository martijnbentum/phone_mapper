import unicodedata

import pytest
from phone_mapper import (
    Mapper, counts, ipa_set, ipa_to_definition, show, validate,
    sampa_to_ipa, celex_to_ipa, disc_to_ipa,
)
from phone_mapper import arpabet, baldey, cgn, coolest, diphone, maus

N_IPA = 95


@pytest.fixture(scope='module')
def mapper():
    return Mapper()


# ── basic instantiation ────────────────────────────────────────────────────

def test_mapper_instantiates(mapper):
    assert mapper is not None


def test_ipa_set_length():
    assert len(ipa_set) == N_IPA


# ── roundtrips ─────────────────────────────────────────────────────────────

def test_ipa_to_disc_roundtrip(mapper):
    disc = mapper.ipa_to_disc['p']
    assert mapper.disc_to_ipa[disc] == 'p'


def test_ipa_to_sampa_roundtrip(mapper):
    sampa = mapper.ipa_to_sampa['b']
    assert mapper.sampa_to_ipa[sampa] == 'b'


def test_ipa_to_celex_roundtrip(mapper):
    celex = mapper.ipa_to_celex['t']
    assert mapper.celex_to_ipa[celex] == 't'


# ── data fixes ─────────────────────────────────────────────────────────────

def test_celex_syllabic_lateral(mapper):
    assert mapper.celex_to_ipa['l,'] == 'l̩'
    assert mapper.ipa_to_celex['l̩'] == 'l,'


def test_celex_rhotic(mapper):
    assert mapper.celex_to_ipa['r*'] == '*'
    assert mapper.ipa_to_celex['*'] == 'r*'


def test_disc_nasal_bouillon(mapper):
    '''The CELEX data files use ~ for ɒ̃ː; " is the secondary stress
    marker in DISC pronunciation strings, not a phoneme.'''
    assert mapper.disc_to_ipa['~'] == 'ɒ̃ː'
    assert mapper.ipa_to_disc['ɒ̃ː'] == '~'
    assert '"' not in mapper.disc_to_ipa


def test_celex_nasals_match_data_notation(mapper):
    '''The CELEX columns in the data files mark nasalization with ~.'''
    assert mapper.celex_to_ipa['&~'] == 'æ̃'
    assert mapper.celex_to_ipa['&~:'] == 'æ̃ː'
    assert mapper.celex_to_ipa['A~:'] == 'ɑ̃ː'
    assert mapper.celex_to_ipa['O~:'] == 'ɒ̃ː'
    assert mapper.celex_to_ipa['Q~:'] == 'œ̃ː'
    assert mapper.ipa_to_celex['ɒ̃ː'] == 'O~:'


def test_disc_nasal_parfum(mapper):
    '''German Parfum is transcribed Q~: with two cv slots, so disc ^
    is the long nasal.'''
    assert mapper.disc_to_ipa['^'] == 'œ̃ː'
    assert mapper.ipa_to_disc['œ̃ː'] == '^'


def test_cgn_nasals_vaccin(mapper):
    assert cgn.cgn_to_ipa['E~'] == 'æ̃'


def test_cgn_nasals_croissant(mapper):
    assert cgn.cgn_to_ipa['A~'] == 'ɑ̃ː'


def test_cgn_nasals_bouillon(mapper):
    assert cgn.cgn_to_ipa['O~'] == 'ɒ̃ː'


def test_cgn_nasals_parfum(mapper):
    assert cgn.cgn_to_ipa['Y~'] == 'œ̃'


def test_dataset_modules():
    assert cgn.name == 'cgn'
    assert arpabet.name == 'arpabet'
    assert baldey.name == 'baldey'
    assert coolest.name == 'coolest'
    assert diphone.name == 'diphone'
    assert maus.name == 'maus'
    assert diphone.to_ipa['sh'] == 'ʃ'


# ── definitions ────────────────────────────────────────────────────────────

def test_ipa_to_definition_coverage():
    assert len(ipa_to_definition) == N_IPA


def test_ipa_to_definition_sample():
    assert ipa_to_definition['p'] == 'voiceless bilabial plosive'
    assert ipa_to_definition['ə'] == 'mid central vowel'


# ── language-specific data ─────────────────────────────────────────────────

def test_cgn_to_ipa():
    assert cgn.cgn_to_ipa['p'] == 'p'


def test_baldey_to_ipa():
    assert baldey.baldey_to_ipa['n'] == 'n'
    assert baldey.baldey_to_ipa['i'] == 'iː'


def test_baldey_to_disc():
    assert baldey.baldey_to_disc['i'] == 'i'
    assert baldey.disc_to_baldey['i'] == 'i'


def test_coolest_to_ipa():
    assert coolest.coolest_to_ipa['i'] == 'iː'


def test_maus_languages():
    assert set(maus.maus_sampa_to_ipa) == set(maus.languages)
    assert set(maus.ipa_to_maus_sampa) == set(maus.languages)


def test_maus_sampa_to_ipa():
    assert maus.maus_sampa_to_ipa['eng']['aI'] == 'aɪ'
    assert maus.maus_sampa_to_ipa['eng']['D'] == 'ð'
    assert maus.maus_sampa_to_ipa['nld']['EI'] == 'ɛɪ'


def test_maus_corrections():
    assert maus.bas_maus_sampa_to_ipa['eng']['R'] == 'ʀ'
    assert maus.maus_sampa_to_ipa['eng']['R'] == 'ɹ'
    assert maus.maus_sampa_to_ipa['spa']['r'] == 'ɾ'
    assert maus.maus_sampa_to_ipa['spa']['rr'] == 'r'
    assert maus.bas_maus_sampa_to_ipa['hun']['d_j'] == 'dʲ'
    assert maus.maus_sampa_to_ipa['hun']['d_j'] == 'ɟ'
    assert maus.maus_sampa_to_ipa['pol']['ts_j'] == 't͡ɕ'


def test_maus_additions():
    assert '@`' not in maus.bas_maus_sampa_to_ipa['eng']
    assert maus.maus_sampa_to_ipa['eng']['@`'] == 'ɚ'
    assert '6_^' not in maus.bas_maus_sampa_to_ipa['deu']
    assert maus.maus_sampa_to_ipa['deu']['6_^'] == 'ɐ\u032f'


def test_maus_normalised_notation():
    assert maus.maus_sampa_to_ipa['eng']['tS'] == 't͡ʃ'
    assert maus.maus_sampa_to_ipa['deu']['ts'] == 't͡s'
    assert maus.maus_sampa_to_ipa['eng']['@~'] == 'ə\u0303'
    assert maus.maus_sampa_to_ipa['fra']['a~'] == 'ɑ\u0303'


def test_maus_dutch_matches_bas():
    # Dutch must match the WebMAUS IPA used for CGN: no corrections
    bas = maus.bas_maus_sampa_to_ipa['nld']
    for symbol, ipa in maus.maus_sampa_to_ipa['nld'].items():
        assert unicodedata.normalize('NFC', bas[symbol]) == ipa


def test_maus_is_language_specific():
    # the generic sampa table maps w to the Dutch labiodental
    assert sampa_to_ipa['w'] == 'ʋ'
    assert maus.maus_sampa_to_ipa['eng']['w'] == 'w'


def test_maus_non_speech_labels():
    for language in maus.languages:
        table = maus.maus_sampa_to_ipa[language]
        assert table['<p:>'] == '(...)'
        assert maus.ipa_to_maus_sampa[language]['(...)'] == '<p:>'


def test_arpabet_to_disc():
    assert arpabet.arpabet_to_disc['AA'] == 'A'
    assert arpabet.arpabet_to_disc['M'] == 'm'
    assert arpabet.arpabet_to_disc['NG'] == 'N'
    assert arpabet.arpabet_to_disc['EN'] == 'H'
    assert arpabet.disc_to_arpabet['C'] == 'NG'


def test_arpabet_example_words():
    assert 'AA' in arpabet.arpabet_to_example_words


def test_example_words(mapper):
    assert mapper.ipa_to_example_words['dutch']['p'] == 'put'
    assert mapper.ipa_to_example_words['english']['p'] == 'pat'
    assert mapper.ipa_to_example_words['german']['p'] == 'Pakt'


# ── module-level lookups ───────────────────────────────────────────────────

def test_counts(mapper):
    result = counts(mapper)
    assert result['ipa_set'] == N_IPA
    assert result['sampa_set'] > 0
    assert result['arpabet_set'] > 0
    assert result['baldey_set'] > 0
    assert result['cgn_set'] > 0
    assert result['coolest_set'] > 0
    assert result['maus_sets']['eng'] > 0


def test_show(mapper, capsys):
    show(mapper)
    lines = capsys.readouterr().out.splitlines()
    assert len(lines) == N_IPA
    assert all(len(line.split('\t')) == 6 for line in lines)


def test_validate_no_problems(mapper):
    assert validate(mapper) == []


def test_validate_reports_problems():
    m = Mapper()
    m.sampa_to_ipa['zz'] = 'not-ipa'
    m.ipa_to_example_words['dutch']['qq'] = 'word'
    problems = validate(m)
    assert any('zz' in p for p in problems)
    assert any('qq' in p for p in problems)


def test_instances_are_isolated():
    m1, m2 = Mapper(), Mapper()
    m1.sampa_to_ipa['ZZ'] = 'test'
    m1.ipa_to_example_words['dutch']['zz'] = 'test'
    assert 'ZZ' not in m2.sampa_to_ipa
    assert 'zz' not in m2.ipa_to_example_words['dutch']


def test_module_level_sampa_to_ipa():
    assert sampa_to_ipa['p'] == 'p'


def test_module_level_celex_to_ipa():
    assert celex_to_ipa['p'] == 'p'


def test_module_level_disc_to_ipa():
    assert disc_to_ipa['p'] == 'p'


# ── w is encoded as ʋ in the mapping data ──────────────────────────────────

def test_w_maps_to_labiodental_approximant(mapper):
    assert mapper.celex_to_ipa['w'] == 'ʋ'
    assert mapper.sampa_to_ipa['w'] == 'ʋ'
    assert mapper.disc_to_ipa['w'] == 'ʋ'
    assert cgn.cgn_to_ipa['w'] == 'ʋ'
