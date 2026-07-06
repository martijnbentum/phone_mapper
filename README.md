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
mapper.disc_to_ipa['p']         # 'p'
mapper.ipa_to_sampa['tʃ']       # 'tS'
mapper.cgn_to_ipa['A~']         # 'ɑ̃ː'
mapper.arpabet_to_disc['AA']    # 'A'
mapper.celex_to_ipa['w']        # 'ʋ' (w is realised as ʋ in Dutch)
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

All mappings live in JSON files under `phone_mapper/data/`. Bidirectional
files store the forward and inverse dicts under named keys (for example
`disc_to_ipa` and `ipa_to_disc`). Language-specific data (CGN, Baldey,
COOLEST, ARPAbet, example words) lives in `data/dutch/`, `data/english/`,
and `data/german/`.

## Development

```bash
uv venv .venv --python 3.12
uv sync
.venv/bin/python -m pytest
```

## License

MIT — see [LICENSE](LICENSE).
