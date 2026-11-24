'''Build phone_mapper/data/maus/<iso>.json from the BAS MAUS phoneme tables.

The source tables in data_sources/maus/ are the BAS WebMAUS symbol lists
(MAUS symbol, SAMPA, IPA, ...) per alignment language. Run with:

    .venv/bin/python scripts/build_maus_maps.py

English merges the variant tables (us, gb, au, nz, sc); the build fails if a
MAUS symbol maps to different IPA symbols in different tables.
'''
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'data_sources' / 'maus'
OUT = ROOT / 'phone_mapper' / 'data' / 'maus'

LANGUAGES = {
    'nld': ['dutch'],
    'eng': ['english_us', 'english_gb', 'english_au', 'english_nz',
        'english_sc'],
    'fra': ['french'],
    'deu': ['german'],
    'hun': ['hungarian'],
    'ita': ['italian'],
    'pol': ['polish'],
    'spa': ['spanish'],
}


def read_table(name):
    '''Return (maus, ipa) pairs in table order from one BAS table.'''
    path = SOURCE / f'maus_{name}_phoneme_map.txt'
    pairs = []
    for line in path.read_text(encoding='utf-8').splitlines():
        if line.startswith('%') or line.startswith('MAUS\t'): continue
        columns = line.split('\t')
        if len(columns) < 3 or not columns[0]: continue
        pairs.append((columns[0], columns[2]))
    return pairs


def merge_tables(names):
    '''Merge tables in order; raise on conflicting entries for one symbol.'''
    forward, inverse = {}, {}
    for name in names:
        for maus, ipa in read_table(name):
            known = forward.get(maus)
            if known is not None and known != ipa:
                message = f'{name}: {maus} -> {ipa}, earlier -> {known}'
                raise ValueError(message)
            forward.setdefault(maus, ipa)
            inverse.setdefault(ipa, maus)
    return forward, inverse


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for iso, names in LANGUAGES.items():
        forward, inverse = merge_tables(names)
        data = {'maus_sampa_to_ipa': forward, 'ipa_to_maus_sampa': inverse}
        path = OUT / f'{iso}.json'
        text = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
        path.write_text(text, encoding='utf-8')
        print(f'{iso}: {len(forward)} symbols, {len(inverse)} ipa')


if __name__ == '__main__':
    main()
