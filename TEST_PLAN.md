# Test plan - Concord

## Executed on 2026-10-09

10/10 groups in sim/check.py passed with mocked model outputs. Live Studio
compatible, direct-conflict and higher-order-cycle cases passed and finalized.
See evidence.json. Other cases below are additional test ideas, not claims of
executed live tests. Delimiters alone do not prove injection resistance.

## Offline

1. Compatible statements
- expected `get_outcome` -> `R_CONSISTENT`.

2. Directly contradictory pair
- expected `R_INCONSISTENT` and that pair appears in `get_conflicts`.

3. Multiple statements with one clash
- direct pair is exposed; conflict members contain the full inconsistent set.

4. Injection in a statement
- judged by content, not prompt instruction capture.

5. Whole-set inconsistency without a conflicting pair
- joint INCONSISTENT with all pair bits zero remains INCONSISTENT.

6. Mere difference (not contradiction)
- no conflict reported.

7. Re-evaluate after settlement
- re-calling `evaluate` must revert.

8. UNKNOWN joint verdict or CONSISTENT with a conflicting pair
- expected UNDETERMINED.

All simulator runs prohibit constructing DynArray, matching the SDK restriction.
LLM outputs are mocked; these tests check handling, not model reasoning.

## Studio checks

1. open_case duplicate id -> revert.
2. domain empty -> revert.
3. evaluate before submit -> `no statements` path.
4. 3+ statements with one clash and one evaluator run.
5. A before B, B before C, C before A under strict temporal ordering:
   require INCONSISTENT even if all direct pair bits are zero.
