import pytest
from phone_mapper import (
    Mapper, counts, ipa_set, ipa_to_definition, show, validate,
    sampa_to_ipa, celex_to_ipa, disc_to_ipa,
)
from phone_mapper import arpabet, baldey, cgn, coolest, diphone

N_IPA = 94


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
