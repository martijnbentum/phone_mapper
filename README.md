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

# Example words per language:
mapper.ipa_to_example_words['dutch']['p']    # 'put'
mapper.ipa_to_example_words['german']['p']   # 'Pakt'
```

Phoneme sets tied to a particular language, corpus, or experiment
rather than a cross-language system (ARPAbet, CGN, Baldey, COOLEST,
diphone) each live in their own module:

```python
from phone_mapper import arpabet, baldey, cgn, coolest, diphone

arpabet.arpabet_to_disc['AA']   # 'A'
arpabet.arpabet_to_example_words['IY']  # 'b(ea)t'
cgn.cgn_to_ipa['A~']            # 'ɑ̃ː'
baldey.baldey_to_disc['A+']     # 'M'
coolest.coolest_to_ipa['i']     # 'iː'
diphone.to_ipa['sh']            # 'ʃ'
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

The `celex` and `disc` mappings both come from the CELEX lexical
database: `celex` is CELEX's SAM-PA variant (close to SAMPA, with nine
vowel symbols of its own), while DISC is CELEX's compact alphabet that
encodes every phoneme as a single character. DISC is shared by the
Dutch, English, and German CELEX lexicons, so it lives at the top
level, not in a language folder.

All mappings live in JSON files under `phone_mapper/data/`, one mapping
per file. A bidirectional file named `x_to_y.json` stores exactly two
dicts under the keys `x_to_y` and `y_to_x` (for example `disc_to_ipa.json`
holds `disc_to_ipa` and `ipa_to_disc`); the loader derives the key names
from the filename.

Files directly in `data/` are the general mappings loaded by the
`Mapper`, including `ipa_to_example_words.json`, which holds the
example words for all languages under one key per language — adding a
language means adding a key to that file. Each remaining subfolder
(`data/arpabet/`, `data/cgn/`, `data/baldey/`, `data/coolest/`) belongs
to the module of the same name, not to the `Mapper`.

## Development

```bash
uv venv .venv --python 3.12
uv sync
.venv/bin/python -m pytest
```

## License

MIT — see [LICENSE](LICENSE).
