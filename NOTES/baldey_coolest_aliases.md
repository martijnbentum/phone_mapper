# Baldey and COOLEST alias entries

Baldey and COOLEST are not general transcription standards: they are
idiosyncratic phoneme sets tied to specific datasets (the Baldey
dataset's textgrids, a restricted CGN-based set, and the COOLEST
dataset's textgrids). Their symbol choices follow those datasets'
internal conventions rather than standard phonetic notation, so the
aliases documented below may simply be how the datasets are annotated.

Data quirks found during the 2026-07-06 repo review. To be confirmed
against the source textgrids before `validate()` is tightened for
these mappings.

## Background: forward and inverse dicts

Every bidirectional mapping file stores two dicts, e.g.
`baldey_to_ipa.json` holds:

- the forward dict `baldey_to_ipa`: Baldey symbol → IPA
- the inverse dict `ipa_to_baldey`: IPA → Baldey symbol

When two Baldey symbols map to the same IPA symbol (an alias), the
forward dict can hold both, but the inverse dict can only name one of
them — a dict has exactly one value per key. The symbol that the
inverse names is currently an accident of JSON file order, not a
deliberate choice.

## Baldey

`dutch/baldey_to_ipa.json` contains two symbols for each of two
diphthongs:

| Baldey symbol | IPA | named by inverse? |
|---------------|-----|-------------------|
| `Au`          | ɑu  | no                |
| `A+`          | ɑu  | yes (`ipa_to_baldey['ɑu'] == 'A+'`) |
| `Ei`          | ɛi  | no                |
| `E+`          | ɛi  | yes (`ipa_to_baldey['ɛi'] == 'E+'`) |

Consequence: `Au` and `Ei` do not survive a roundtrip. Converting
`Au` → IPA (`ɑu`) → Baldey returns `A+`, not `Au`. The same aliases
propagate into `baldey_to_disc.json` (`Au` and `A+` both → DISC `M`;
`disc_to_baldey['M'] == 'A+'`).

Open questions:
- Do the Baldey textgrids actually contain both notations? If only
  one occurs, delete the other from the data.
- If both occur, pick the canonical symbol for the inverse
  deliberately and document it, instead of relying on file order.

## COOLEST

`dutch/coolest_to_ipa.json` maps both `Y` and `u` to `uː`; the inverse
names `u` (`ipa_to_coolest['uː'] == 'u'`), so `Y` does not roundtrip.

`Y` → `uː` is phonetically surprising: Y-like symbols normally denote
a front rounded vowel (ʏ or y), not a long back vowel. Check whether
the COOLEST textgrids really use `Y` for `uː`, or whether this entry
should map to `ʏ`/`yː` instead.

## Impact on validate()

`validate()` currently skips the Baldey and COOLEST pairs. When it is
generalized to cover them, it must either tolerate confirmed aliases
(check "every forward value is an inverse key" rather than a strict
bijection) or the alias entries above must first be resolved in the
data.
