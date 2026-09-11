# TODO

- Make all possible places take DataTarget without keywords (e.g., str means 'storage')

- In 24w12a (https://www.minecraft.net/en-us/article/minecraft-snapshot-24w21a) it says that the attribute command has
  changed, but it doesn't clearly say how.
  Look into this when the doc catches up with this.

- Most generated values have no docstrings.
  A value emitted into `_values.py` reaches `info.py` automatically through `from ._values import *`, so it is usable
  with no further work, but Sphinx cannot attach prose to a variable whose assignment lives in another module.
  Documenting one requires a bare re-declaration in `info.py` — `wolves: list[str]` followed by a docstring, the pattern
  at info.py:20-25.
  Only a handful of the 625 generated names have it.
  The `missing-docstrings` skill audits this.

- Investigate whether `info.py` can be generated from an `info.yaml` that has the docstrings and source of the data, so
  the list of values to generate doesn't require updating both `build_data.py` and `info.py`.
  Note that `info.py` also holds things no generator can produce — `patterns_standard_order`, the
  `_missing_from_standard_order` warning, the Enums and NamedTuples — so the question is whether the generated
  declarations can be separated from that hand-written part, not whether the whole file can be generated.
