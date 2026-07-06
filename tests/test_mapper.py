import pytest
from phone_mapper import Mapper, validate, to_ipa


@pytest.fixture(scope='module')
def mapper():
    return Mapper()


def test_mapper_instantiates(mapper):
    assert mapper is not None


def test_ipa_to_disc_roundtrip(mapper):
    disc = mapper.ipa_to_disc['p']
    assert mapper.disc_to_ipa[disc] == 'p'


def test_ipa_to_sampa_roundtrip(mapper):
    sampa = mapper.ipa_to_sampa['b']
    assert mapper.sampa_to_ipa[sampa] == 'b'


def test_ipa_to_celex_roundtrip(mapper):
    celex = mapper.ipa_to_celex['t']
    assert mapper.celex_to_ipa[celex] == 't'


def test_cgn_to_ipa(mapper):
    assert mapper.cgn_to_ipa['p'] == 'p'


def test_arpabet_to_disc(mapper):
    assert 'AA' in mapper.arpabet_to_disc


def test_baldey_to_ipa(mapper):
    assert 'n' in mapper.baldey_to_ipa
    assert mapper.baldey_to_ipa['n'] == 'n'


def test_coolest_to_ipa(mapper):
    assert 'i' in mapper.coolest_to_ipa
    assert mapper.coolest_to_ipa['i'] == 'iː'


def test_validate_counts(mapper):
    counts = validate(mapper)
    assert 'ipa_set' in counts
    assert counts['ipa_set'] > 0


def test_to_ipa_lookup():
    assert 'p' in to_ipa
    assert to_ipa['p'] == 'p'


def test_non_dutch_fix_w():
    m = Mapper(language='english')
    assert m.celex_to_ipa['w'] == 'ʋ'
