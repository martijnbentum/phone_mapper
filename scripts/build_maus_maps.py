'''Build phone_mapper/data/maus/<iso>.json from the BAS MAUS phoneme tables.

Run with:

    .venv/bin/python scripts/build_maus_maps.py

Steps per language:

1. Read the BAS WebMAUS tables in data_sources/maus/ (MAUS symbol -> IPA).
   English merges the variant tables (us, gb, au, nz, sc); the build fails
   if a MAUS symbol maps to different IPA symbols in different tables.
   This raw result is kept as bas_maus_sampa_to_ipa.
2. Apply data_sources/maus/corrections_<iso>.tsv: reviewed per-language
   fixes where the BAS generic IPA is not the sound the symbol stands for
   in that language (e.g. Spanish r is a tap). Each row names the BAS IPA
   it expects; the build fails if the BAS table no longer says that. A row
   with an empty bas_ipa adds a symbol that is not in the BAS table (used
   for labels written by corpus fixes, e.g. English @`); the build fails
   if the symbol does exist in BAS.
3. Normalise notation:
   - U+0342 (Greek perispomeni, BAS typo for nasal schwa) -> U+0303
   - Unicode NFC
   - affricates get a tie bar (tʃ -> t͡ʃ, ts -> t͡s); MAUS gemination on
     the stop moves behind the affricate (tːʃ -> t͡ʃː)
   - palatalisation precedes length (tːʲ -> tʲː)
'''
import json
import re
import unicodedata
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

TIE_BAR = '͡'
LONG = 'ː'
PALATALIZED = 'ʲ'
AFFRICATE = re.compile(r'^(t)(ː?)([ʃs])(ʲ?)(ː?)$|^(d)(ː?)([ʒz])(ʲ?)(ː?)$')


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
    merged = {}
    for name in names:
        for maus, ipa in read_table(name):
            known = merged.get(maus)
            if known is not None and known != ipa:
                message = f'{name}: {maus} -> {ipa}, earlier -> {known}'
                raise ValueError(message)
            merged.setdefault(maus, ipa)
    return merged


def read_corrections(iso):
    '''Return {maus: (bas_ipa, ipa)} from corrections_<iso>.tsv, if any.'''
    path = SOURCE / f'corrections_{iso}.tsv'
    if not path.exists(): return {}
    corrections = {}
    for line in path.read_text(encoding='utf-8').splitlines()[1:]:
        maus, bas_ipa, ipa, _reason = line.split('\t')
        corrections[maus] = (bas_ipa, ipa)
    return corrections


def apply_corrections(iso, bas):
    '''Return a copy of the BAS table with the reviewed corrections.'''
    table = dict(bas)
    for maus, (bas_ipa, ipa) in read_corrections(iso).items():
        found = bas.get(maus)
        if not bas_ipa and found is None:
            table[maus] = ipa
            continue
        if found is None or nfc(found) != nfc(bas_ipa):
            message = f'{iso} correction {maus}: expected BAS {bas_ipa!r}, '
            message += f'found {found!r}'
            raise ValueError(message)
        table[maus] = ipa
    return table


def nfc(text):
    return unicodedata.normalize('NFC', text)


def normalize_ipa(label):
    '''Return one IPA label in normalised notation (see module doc).'''
    label = nfc(label.replace('͂', '̃'))
    match = AFFRICATE.match(label)
    if match is not None:
        groups = [g for g in match.groups() if g is not None]
        stop, stop_long, fricative, palatalized, long = groups
        length = LONG if stop_long or long else ''
        label = stop + TIE_BAR + fricative + palatalized + length
    return label.replace(LONG + PALATALIZED, PALATALIZED + LONG)


def invert(table):
    '''Map each IPA symbol to its first MAUS symbol in table order.'''
    inverse = {}
    for maus, ipa in table.items():
        inverse.setdefault(ipa, maus)
    return inverse


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for iso, names in LANGUAGES.items():
        bas = merge_tables(names)
        corrected = apply_corrections(iso, bas)
        forward = {maus: normalize_ipa(ipa) for maus, ipa in corrected.items()}
        data = {'maus_sampa_to_ipa': forward,
            'ipa_to_maus_sampa': invert(forward),
            'bas_maus_sampa_to_ipa': bas}
        path = OUT / f'{iso}.json'
        text = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
        path.write_text(text, encoding='utf-8')
        n_fixed = len(read_corrections(iso))
        print(f'{iso}: {len(forward)} symbols, {n_fixed} corrections')


if __name__ == '__main__':
    main()
