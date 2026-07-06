import pytest
from phone_mapper import (
    Mapper, counts, ipa_set, ipa_to_definition, validate,
    sampa_to_ipa, celex_to_ipa, disc_to_ipa,
)

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
    assert mapper.dutch.cgn_to_ipa['E~'] == 'æ̃'


def test_cgn_nasals_croissant(mapper):
    assert mapper.dutch.cgn_to_ipa['A~'] == 'ɑ̃ː'


def test_cgn_nasals_bouillon(mapper):
    assert mapper.dutch.cgn_to_ipa['O~'] == 'ɒ̃ː'


def test_cgn_nasals_parfum(mapper):
    assert mapper.dutch.cgn_to_ipa['Y~'] == 'œ̃'


def test_language_namespaces(mapper):
    assert mapper.dutch.name == 'dutch'
    assert 'cgn_to_ipa' in vars(mapper.dutch)
    assert 'arpabet_to_ipa' in vars(mapper.english)
    assert 'ipa_to_example_words' in vars(mapper.german)


# ── definitions ────────────────────────────────────────────────────────────

def test_ipa_to_definition_coverage():
    assert len(ipa_to_definition) == N_IPA


def test_ipa_to_definition_sample():
    assert ipa_to_definition['p'] == 'voiceless bilabial plosive'
    assert ipa_to_definition['ə'] == 'mid central vowel'


# ── language-specific data ─────────────────────────────────────────────────

def test_cgn_to_ipa(mapper):
    assert mapper.dutch.cgn_to_ipa['p'] == 'p'


def test_baldey_to_ipa(mapper):
    assert mapper.dutch.baldey_to_ipa['n'] == 'n'
    assert mapper.dutch.baldey_to_ipa['i'] == 'iː'


def test_baldey_to_disc(mapper):
    assert mapper.dutch.baldey_to_disc['i'] == 'i'
    assert mapper.dutch.disc_to_baldey['i'] == 'i'


def test_coolest_to_ipa(mapper):
    assert mapper.dutch.coolest_to_ipa['i'] == 'iː'


def test_arpabet_to_disc(mapper):
    assert mapper.english.arpabet_to_disc['AA'] == 'A'
    assert mapper.english.arpabet_to_disc['M'] == 'm'
    assert mapper.english.arpabet_to_disc['NG'] == 'N'
    assert mapper.english.arpabet_to_disc['EN'] == 'H'
    assert mapper.english.disc_to_arpabet['C'] == 'NG'


def test_arpabet_example_words(mapper):
    assert 'AA' in mapper.english.arpabet_to_example_words


def test_example_words_dutch(mapper):
    assert mapper.dutch.ipa_to_example_words['p'] == 'put'


def test_example_words_english(mapper):
    assert mapper.english.ipa_to_example_words['p'] == 'pat'


def test_example_words_german(mapper):
    assert mapper.german.ipa_to_example_words['p'] == 'Pakt'


# ── module-level lookups ───────────────────────────────────────────────────

def test_counts(mapper):
    result = counts(mapper)
    assert result['ipa_set'] == N_IPA
    assert result['sampa_set'] > 0
    assert result['cgn_set'] > 0


def test_validate_no_problems(mapper):
    assert validate(mapper) == []


def test_instances_are_isolated():
    m1, m2 = Mapper(), Mapper()
    m1.english.arpabet_to_ipa['ZZ'] = 'test'
    m1.dutch.ipa_to_example_words['zz'] = 'test'
    assert 'ZZ' not in m2.english.arpabet_to_ipa
    assert 'zz' not in m2.dutch.ipa_to_example_words


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
    assert mapper.dutch.cgn_to_ipa['w'] == 'ʋ'
