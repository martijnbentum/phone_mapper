# Option: freeze module-level dicts with MappingProxyType

Decision 2026-07-06: leave as is. The module-level mapping dicts
(`sampa_to_ipa` etc. in `mapper.py` and the dicts in the `arpabet`,
`cgn`, `baldey`, and `coolest` modules) are shared mutable state:
mutating one in place affects the whole process, and for the
`mapper.py` dicts it poisons every `Mapper()` created afterwards,
since instances copy from them at construction. Per-instance `Mapper`
attributes are already isolated; this only concerns the shared
module-level objects.

If accidental in-place mutation ever becomes a real problem, the fix
is wrapping the loaded dicts in `types.MappingProxyType` — a read-only
view: writes raise `TypeError`, while reads, iteration, and
`dict(proxy)` (used by `Mapper.__init__` for its copies) work
unchanged. Cleanest place: have `_load_json` and `_load_mapping_pair`
return proxies, which covers `mapper.py` and all dataset modules at
once (~15 lines total).

Ripple effects to handle when implementing:

1. `validate._check_namespace` filters attributes with
   `isinstance(value, dict)`. A proxy is not a `dict` subclass, so the
   filter would silently skip everything and validate would check
   nothing while staying green. It must become
   `isinstance(value, Mapping)` (`collections.abc.Mapping`).
   `test_validate_reports_problems` guards against this failure mode.
2. The `*_set` lists are not covered; full immutability means tuples,
   which changes the type callers see.
3. Nested dicts stay mutable: freezing `ipa_to_example_words` at the
   top level does not freeze the per-language inner dicts — wrap each
   inner dict as well.

A determined caller can still reach the underlying dict, so this is
hardening against accidents, not a security boundary.
