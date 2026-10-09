# Concord portal submission

## Category

Builder > Intelligent Contracts

## Title

Concord

## Contribution date

October 9, 2026 (publication and live verification).

## Description and notes

Concord judges whether 2-10 separate statements can all hold within a committed domain. It calls gl.nondet.exec_prompt inside gl.eq_principle.prompt_comparative: validators independently assess the same set and compare the joint verdict and every pairwise conflict bit. This contract's own non-deterministic judgment determines the stored outcome, rather than reading settled upstream flags. It handles higher-order contradictions even when every pair is compatible. Inputs are creator-only and one-time, commitments are rechecked, result types are validated, and settlement is terminal. Three Studio cases finalized with successful execution and majority agreement: compatible claims, a direct conflict, and a three-event cycle with no pairwise conflict. Ten local regression groups and SDK validation pass. This is consensus-backed LLM judgment, not a formal proof; conflict members are the full inconsistent set, not a minimal core.

## Primary evidence links

- Source repository: https://github.com/Zhekinmaksim/genlayer-concord
- Deployed Studio contract: https://explorer-studio.genlayer.com/address/0x40E19BFfbBd0FD45BBE30B8643C8dB9CdF96A3bA

## Additional evidence

- Exact deployed source: https://github.com/Zhekinmaksim/genlayer-concord/blob/5c72b2cef3bbd8f347e826d9b1c7ea5dfad37efb/contract.py
- Deployment: https://explorer-studio.genlayer.com/tx/0x9329892e40caf6eaee24af69c691973322c862733ef10990865e5cdc83223185
- concord-compatible-001: https://explorer-studio.genlayer.com/tx/0x762c0761d55cfd9ec7d75b8881c52881ca388902c2f20ed4de7705afc9064b41
- concord-conflict-001: https://explorer-studio.genlayer.com/tx/0x8a73bf1627b20182eb0705bad2ea354e6bce109aa2365be66ed7e6265b258640
- concord-cycle-001: https://explorer-studio.genlayer.com/tx/0x43366a4a583c1111e0ff8cbdde27531d0dabe2c35fb247dcf5cc8f4b507f5ed4
- Inputs, expected and observed results: https://github.com/Zhekinmaksim/genlayer-concord/blob/main/evidence.json

## Verification

10/10 local regression groups; SDK semantic validation and ABI extraction passed.
All three live evaluations and the deployment are FINALIZED, execution SUCCESS,
consensus MAJORITY_AGREE, with leader_only=false. Stored results match expectations.
Local tests mock the SDK and models; they are separate from the live Studio checks.

## Submission status

Ready for manual entry. No portal submission has been created or sent.
Studio is a test environment, not mainnet. Portal acceptance is not guaranteed.
