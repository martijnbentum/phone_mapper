'''Integrity checks for the mapping data shipped with phone_mapper.'''

from .mapper import Mapper, ipa_to_definition


def validate(mapper=None):
    '''Check mapping invariants, return a list of problem descriptions.'''
    from . import arpabet, baldey, cgn, coolest
    if not mapper: mapper = Mapper()
    problems = []
    pairs = [
        ('sampa', mapper.sampa_to_ipa, mapper.ipa_to_sampa),
        ('celex', mapper.celex_to_ipa, mapper.ipa_to_celex),
        ('disc', mapper.disc_to_ipa, mapper.ipa_to_disc),
        ('cgn', cgn.cgn_to_ipa, cgn.ipa_to_cgn),
    ]
    for name, forward, inverse in pairs:
        problems += _check_bijection(name, forward, inverse)
    problems += [f'no definition for {ipa}'
        for ipa in mapper.ipa_set if ipa not in ipa_to_definition]
    for namespace in (arpabet, baldey, cgn, coolest):
        problems += _check_namespace(namespace, mapper.disc_to_ipa)
    for language, words in mapper.ipa_to_example_words.items():
        problems += [f'example words {language}: unknown ipa {ipa}'
            for ipa in words if ipa not in ipa_to_definition]
    return problems


def _check_bijection(name, forward, inverse):
    '''The forward and inverse dicts must mirror each other exactly.'''
    problems = []
    for symbol, ipa in forward.items():
        if inverse.get(ipa) != symbol:
            problems.append(f'{name}: {symbol} -> {ipa} -> {inverse.get(ipa)}')
    for ipa, symbol in inverse.items():
        if forward.get(symbol) != ipa:
            problems.append(
                f'{name} inverse: {ipa} -> {symbol} -> {forward.get(symbol)}')
    return problems


def _check_namespace(namespace, disc_to_ipa):
    '''Check mapping pairs and symbol domains for one dataset module.

    Pair check: every value of x_to_y must be a key of y_to_x when that
    inverse exists. This tolerates aliases (two symbols mapping to the
    same target), unlike the strict bijection check; see
    NOTES/baldey_coolest_aliases.md.
    Domain check: symbols of a known transcription system must belong
    to that system's inventory.
    '''
    problems = []
    mappings = {name: value for name, value in vars(namespace).items()
        if isinstance(value, dict) and '_to_' in name}
    for name, mapping in mappings.items():
        parts = name.split('_to_')
        if len(parts) != 2:
            continue
        source, target = parts
        label = f'{namespace.name}.{name}'
        inverse_name = f'{target}_to_{source}'
        inverse = mappings.get(inverse_name)
        if inverse is not None:
            problems += [
                f'{label}: {symbol} -> {value} missing from {inverse_name}'
                for symbol, value in mapping.items() if value not in inverse]
        source_domain = _domain(source, mappings, disc_to_ipa)
        if source_domain is not None:
            problems += [f'{label}: unknown {source} symbol {symbol}'
                for symbol in mapping if symbol not in source_domain]
        target_domain = _domain(target, mappings, disc_to_ipa)
        if target_domain is not None:
            problems += [f'{label}: unknown {target} symbol {value}'
                for value in mapping.values() if value not in target_domain]
    return problems


def _domain(system, mappings, disc_to_ipa):
    '''Return the known symbols of a transcription system, or None.'''
    if system == 'ipa': return ipa_to_definition
    if system == 'disc': return disc_to_ipa
    return mappings.get(f'{system}_to_ipa')
