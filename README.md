# Concord - consensus on mutual consistency of a set

A GenLayer Intelligent Contract that decides whether a set of statements can all
be true at once, and if not, which statements clash.

## Publication and verification

Published on 2026-10-09 and deployed to
[Studio](https://explorer-studio.genlayer.com/address/0x40E19BFfbBd0FD45BBE30B8643C8dB9CdF96A3bA).
10 local regression groups and SDK semantic validation passed. Three live cases
(compatible claims, a direct conflict, and a higher-order cycle) matched their
expected results. Deployment and evaluations are FINALIZED with SUCCESS and
MAJORITY_AGREE in normal consensus mode, not leader-only.
See [evidence.json](evidence.json) for inputs, hashes, transactions and readbacks,
and [SUBMISSION.md](SUBMISSION.md) for manual portal entry. No submission was sent.

## Consensus mechanism

Not pairwise equivalence of two texts, and not self-consistency within one
document: joint consistency over N separate claims. The judge returns a joint
verdict (CONSISTENT, INCONSISTENT, UNKNOWN) and a per-pair conflict vector.
Validators compare both outputs and the statements hash. The joint verdict
determines settlement; direct conflict pairs provide additional diagnostics.

## Documented limit

The whole-set judgment includes higher-order contradictions, such as A before B,
B before C, and C before A under strict temporal ordering. This is an LLM
judgment validated by consensus, not a formal satisfiability proof. The exposed
conflict members are the full inconsistent set, not a minimal unsatisfiable core.
UNKNOWN and malformed or internally contradictory judgments settle UNDETERMINED.

## Outcomes

- CONSISTENT: consensus says all statements can hold together.
- INCONSISTENT: conflict pairs plus the set of involved statements.
- UNDETERMINED: judgment did not converge or statements changed after submit.

## API

- `open_case(id, domain_text)` -> domain hash
- `submit_statements(id, statements)` - 2 to 10
- `evaluate(id)` - permissionless
- `get_outcome(id)` -> 0 pending, 1 consistent, 2 inconsistent, 3 undetermined
- `get_conflicts(id)` -> readable clashing pairs
- `get_conflict_members(id)` -> all indices in the inconsistent set
- `get_result(id)` -> JSON outcome, reason, pairs, members and commitments

## Test plan (hosted Studio)

1. Compatible statements -> CONSISTENT.
2. Two directly contradictory statements -> INCONSISTENT, the pair flagged.
3. Several statements, one pair clashes -> INCONSISTENT, only that pair and its
   full inconsistent set surfaced as members.
4. Injection in a statement -> judged on merit or consensus fails.
5. Stored domain or statements changed -> input-changed UNDETERMINED (local simulation).
6. Mere difference (not contradiction) -> CONSISTENT, not a false conflict.
7. Re-evaluate after settlement -> revert.

## Notes

Consistency aggregation is deterministic; the joint verdict and pairwise conflict
judgment are non-deterministic. Validators independently run the judgment through
`gl.eq_principle.prompt_comparative`, which uses an LLM comparator, not a strict
byte-equality check. The accepted judgment determines the stored outcome.

Run `python3 sim/check.py` for local regressions. Models and SDK storage are
mocked; the hash stub uses SHA3-256, not actual Keccak256. SDK validation checks
types and ABI; the separate live cases exercised real GenVM and consensus.
Creator-only one-time inputs, input integrity checks, strict integer result bits,
terminal settlement and a result hash binding domain, statements, decision and
reason are enforced. Prompt delimiters do not guarantee injection resistance.
Models can agree incorrectly. Network consensus failure may leave a transaction
unaccepted rather than store UNDETERMINED. No external security audit is claimed.
