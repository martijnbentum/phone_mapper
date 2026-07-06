import pytest
from phone_mapper import (
    Mapper, counts, ipa_set, ipa_to_definition, validate, to_ipa,
    sampa_to_ipa, celex_to_ipa, disc_to_ipa,
)

N_IPA = 81


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
    assert mapper.cgn_to_ipa['E~'] == 'æ̃'


def test_cgn_nasals_croissant(mapper):
    assert mapper.cgn_to_ipa['A~'] == 'ɑ̃ː'


def test_cgn_nasals_bouillon(mapper):
    assert mapper.cgn_to_ipa['O~'] == 'ɒ̃ː'


def test_cgn_nasals_parfum(mapper):
    assert mapper.cgn_to_ipa['Y~'] == 'œ̃'


def test_cgn_set_matches_mapping(mapper):
    assert mapper.cgn_set == list(mapper.cgn_to_ipa.keys())
    assert len(mapper.cgn_set) > 0


# ── definitions ────────────────────────────────────────────────────────────

def test_ipa_to_definition_coverage():
    assert len(ipa_to_definition) == N_IPA


def test_ipa_to_definition_sample():
    assert ipa_to_definition['p'] == 'voiceless bilabial plosive'
    assert ipa_to_definition['ə'] == 'mid central vowel'


# ── language-specific data ─────────────────────────────────────────────────

def test_cgn_to_ipa(mapper):
    assert mapper.cgn_to_ipa['p'] == 'p'


def test_baldey_to_ipa(mapper):
    assert mapper.baldey_to_ipa['n'] == 'n'
    assert mapper.baldey_to_ipa['i'] == 'iː'


def test_coolest_to_ipa(mapper):
    assert mapper.coolest_to_ipa['i'] == 'iː'


def test_arpabet_to_disc(mapper):
    assert mapper.arpabet_to_disc['AA'] == 'A'
    assert mapper.arpabet_to_disc['M'] == 'm'
    assert mapper.arpabet_to_disc['NG'] == 'N'
    assert mapper.arpabet_to_disc['EN'] == 'H'
    assert mapper.disc_to_arpabet['C'] == 'NG'


def test_arpabet_example_words(mapper):
    assert 'AA' in mapper.arpabet_to_example_words


def test_example_words_dutch(mapper):
    assert mapper.ipa_to_example_words_dutch['p'] == 'put'


def test_example_words_english(mapper):
    assert mapper.ipa_to_example_words_english['p'] == 'pat'


def test_example_words_german(mapper):
    assert mapper.ipa_to_example_words_german['p'] == 'Pakt'


# ── module-level lookups ───────────────────────────────────────────────────

def test_counts(mapper):
    result = counts(mapper)
    assert result['ipa_set'] == N_IPA
    assert result['sampa_set'] > 0
    assert result['cgn_set'] > 0


def test_validate_no_problems(mapper):
    assert validate(mapper) == []


def test_validate_non_dutch():
    assert validate(Mapper(language='english')) == []


def test_instances_are_isolated():
    m1, m2 = Mapper(), Mapper()
    m1.arpabet_to_ipa['ZZ'] = 'test'
    m1.ipa_to_example_words_dutch['zz'] = 'test'
    assert 'ZZ' not in m2.arpabet_to_ipa
    assert 'zz' not in m2.ipa_to_example_words_dutch


def test_to_ipa_lookup():
    assert to_ipa['p'] == 'p'


def test_module_level_sampa_to_ipa():
    assert sampa_to_ipa['p'] == 'p'


def test_module_level_celex_to_ipa():
    assert celex_to_ipa['p'] == 'p'


def test_module_level_disc_to_ipa():
    assert disc_to_ipa['p'] == 'p'


# ── non-Dutch language ─────────────────────────────────────────────────────

def test_non_dutch_fix_w():
    m = Mapper(language='english')
    assert m.celex_to_ipa['w'] == 'ʋ'
    assert m.sampa_to_ipa['w'] == 'ʋ'
    assert m.disc_to_ipa['w'] == 'ʋ'
