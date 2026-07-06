# phone_mapper

Phoneme mapping between IPA, SAMPA, CELEX, DISC, CGN, ARPAbet, Baldey,
and COOLEST transcription systems.

Ported from `phoneme_mapper.py` in
[diphone_perception](https://github.com/martijnbentum/diphone_perception).

## Installation

```bash
pip install git+https://github.com/martijnbentum/phone_mapper
```

Requires Python 3.12+. No runtime dependencies.

## Usage

```python
from phone_mapper import Mapper

mapper = Mapper()

# General mappings are attributes:
mapper.disc_to_ipa['p']         # 'p'
mapper.ipa_to_sampa['tʃ']       # 'tS'
mapper.celex_to_ipa['w']        # 'ʋ' (w is realised as ʋ in Dutch)

# Language-specific mappings live in per-language namespaces:
mapper.dutch.cgn_to_ipa['A~']                  # 'ɑ̃ː'
mapper.dutch.ipa_to_example_words['p']         # 'put'
mapper.english.arpabet_to_disc['AA']           # 'A'
mapper.english.arpabet_to_example_words['IY']  # 'b(ea)t'
```

Module-level helpers:

```python
from phone_mapper import ipa_to_definition, counts, validate, show

ipa_to_definition['p']   # 'voiceless bilabial plosive'
counts()                 # entry counts per phoneme set
validate()               # list of mapping inconsistencies (empty if OK)
show()                   # print IPA/SAMPA/CELEX/DISC/CGN side by side
```

## Data

All mappings live in JSON files under `phone_mapper/data/`, one mapping
per file. A bidirectional file named `x_to_y.json` stores exactly two
dicts under the keys `x_to_y` and `y_to_x` (for example `disc_to_ipa.json`
holds `disc_to_ipa` and `ipa_to_disc`); the loader derives the key names
from the filename. Language-specific data (CGN, Baldey, COOLEST, ARPAbet,
example words) lives in `data/dutch/`, `data/english/`, and
`data/german/`.

## Development

```bash
uv venv .venv --python 3.12
uv sync
.venv/bin/python -m pytest
```

## License

MIT — see [LICENSE](LICENSE).
