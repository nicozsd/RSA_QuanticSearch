# NOTICE — QuanticTest.py: license scope, provenance and attribution

## Applicable license and recorded version

**SPDX license identifier:** MIT, **only for the original copyrightable
contributions** identified below.

**Copyright/author attribution:** Copyright (c) 2025 Nicolas Santos
(GitHub: [@nicozsd](https://github.com/nicozsd)).

**Source file:** [QuanticTest.py](QuanticTest.py).

**Recorded Git blob (file-content SHA-1):**
`3bc0665713f491ae9f9c27d43aca04fdc0bb9eb6`.

The rights holder grants the permissions in [LICENSE](LICENSE) for original
source code and explanatory comments in **this recorded version of
QuanticTest.py** to the extent that those contributions are owned or licensable
by the rights holder. This is a grant published now that expressly includes
the identified earlier file contents; it does **not** assert that an MIT
license notice was already present when the file was recorded.

The file itself is left unchanged so the recorded Git blob remains
identifiable. The grant is restricted to material within the rights holder's
authority and should not be read as a blanket license for the repository.

## Attribution to preserve

When reproducing or distributing copies or substantial portions of the
licensed original material, include the MIT copyright and permission notice
from [LICENSE](LICENSE).

Suggested source-record attribution:

> Nicolas Santos (@nicozsd), RSA_QuanticSearch, `QuanticTest.py`,
> original code and comments, 2025. License: MIT (file-scoped; see
> `LICENSE` and `NOTICE.md`). Recorded Git blob:
> `3bc0665713f491ae9f9c27d43aca04fdc0bb9eb6`.

This suggested bibliographic/source record does not add a separate
license condition beyond MIT.

## Original expression versus examples and dependencies

The author-written experimental glue, RSA key-generation orchestration,
CPU/GPU simulator invocation, timing, Excel result reporting, and original
Portuguese explanatory comments are covered **only insofar as** the
rights holder owns the copyright in their expression. General scientific
ideas, mathematical algorithms, the Bell-state circuit pattern (Hadamard
plus controlled-NOT), and ordinary API usage are not claimed as exclusive
original inventions or as independently copyrightable expression.

The file imports `qiskit`, `qiskit_aer`, `openpyxl`, `sympy`, and
`matplotlib`; their software and documentation remain under the relevant
upstream licenses. An `import` statement does not make that dependency
part of the present MIT grant. This repository notice does not reproduce
or relicense those packages.

The local `breakCode.py` module supplies the **separate classical
factoring routine**, is outside the scope of this file-specific grant,
and must not be recorded as licensed by this notice. Other repository
files (including `.gitignore`, tests, data, and generated output) are
likewise outside the scope of this notice.

No particular copied or adapted third-party source snippet, original
source URL, revision or version is established by the repository history
reviewed for this notice. This is **not** a certification that no such
adaptations exist. If any adapted third-party code or comments are
identified, record the original author, source URL, relevant
revision/version, applicable license and required notice separately.
Preserve those original notices and obtain authorization where needed;
**do not treat this MIT grant as relicensing third-party material**.

## Technical scope

`QuanticTest.py` samples a Bell-state circuit using CPU/GPU simulators
and supplies a derived sampled value to a separate classical factoring
routine. Neither this notice nor the license asserts any quantum
factoring speedup or validates research or dataset acceptance.
