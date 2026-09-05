# Repository documentation refresh

## Frozen contract

Baseline: `5c147579bd5870b65dc8fc4e54ed65ea89962085`; branch
`codex/refresh-project-documentation`. User requested current GitHub README and
related documentation, with projects before the repository introduction.

DOC-01: Root README starts with the three actual projects, their purposes,
current checked-in baselines, and useful relative links, then the repo intro.
DOC-02: Correct demonstrably stale current-facing documentation and commands
using checked-in authority and verified GitHub delivery records.
DOC-03: Preserve historical contracts, source, tests, generated artifacts,
dependencies, release bytes, and separate acceptance states. No new design,
release, preview, or physical validation is implied.
DOC-04: Validate changed links and documentation claims independently; preserve
the existing required local validation command contract. Deliver through a PR.

Input path/content hashes are frozen in `INPUTS.sha256`; candidate manifest
will include changed decision-bearing docs plus unchanged relevant inputs and
this frozen contract. Mutable DAG/status and evidence records are excluded
from gate fingerprints. Changed README hashes do not rewrite historical verdicts.

## Mutable delegated execution plan

| ID | Owner / role | Dependencies | Exclusive writes | Done gate |
|---|---|---|---|---|
| DOC-I | /root/docs_editor, implementation | frozen baseline/inputs | current-facing README/docs and necessary project continuity addenda; DESIGN | accurate project-first candidate |
| DOC-C | /root/docs_critic, critic | frozen candidate | none | claims/scope critique receipt |
| DOC-V | /root/docs_validator, validator | frozen candidate | VALIDATION | links, focused structure checks, preservation receipt |
| DOC-R | /root/docs_reviewer, formal review | DOC-C + DOC-V | REVIEW | independent join verdict |
| DOC-D | /root, coordinator/delivery | DOC-R | concise indexes, HANDOFF, git/PR | commit, push, PR |

All roles may read relevant repository records. Implementation reads each touched
project's state, NEXT_AGENT, requirements, experience, decision index and active
iteration before editing. Forbidden: source/tests/artifact/lock changes, historical
contract rewrites, policy redesign, other worktrees, publishing releases, merge.
One writer per namespace; at most three workers. Editor uses balanced/medium;
critic/reviewer strong/high; deterministic validator fast/low. Qualitative ceilings:
editor 10 minutes/8k tokens, checks 5 minutes/4k each, receipts under 700 words,
one attempt plus at most two focused repairs. Stop for input drift, authority
conflict or a change requiring design/manifest scope expansion; report smallest
resolution. Each return identifies status, owner, verified fingerprint, changed
paths, commands/results, findings with severity, requirement coverage, risks and
next action. No self-approval.
