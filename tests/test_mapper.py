import pytest
from phone_mapper import (
    Mapper, ipa_set, ipa_to_definition, validate, to_ipa,
    sampa_to_ipa, celex_to_ipa, disc_to_ipa,
)


@pytest.fixture(scope='module')
def mapper():
    return Mapper()


# ── basic instantiation ────────────────────────────────────────────────────

def test_mapper_instantiates(mapper):
    assert mapper is not None


def test_ipa_set_length():
    assert len(ipa_set) == 81


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


def test_cgn_length(mapper):
    assert len(ipa_set) == 81


# ── definitions ────────────────────────────────────────────────────────────

def test_ipa_to_definition_coverage():
    assert len(ipa_to_definition) == 81


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
    assert 'AA' in mapper.arpabet_to_disc


def test_arpabet_example_words(mapper):
    assert 'AA' in mapper.arpabet_to_example_words


def test_example_words_dutch(mapper):
    assert mapper.ipa_to_example_words_dutch['p'] == 'put'


def test_example_words_english(mapper):
    assert mapper.ipa_to_example_words_english['p'] == 'pat'


def test_example_words_german(mapper):
    assert mapper.ipa_to_example_words_german['p'] == 'Pakt'


# ── module-level lookups ───────────────────────────────────────────────────

def test_validate_counts(mapper):
    counts = validate(mapper)
    assert counts['ipa_set'] == 81
    assert counts['sampa_set'] > 0
    assert counts['cgn_set'] > 0


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
