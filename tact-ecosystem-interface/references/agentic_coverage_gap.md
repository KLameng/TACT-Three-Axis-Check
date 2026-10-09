# Agentic Coverage-Gap Checklist (OWASP Agentic Applications 2026 ↔ TACT coordinate library)

> Bound to: TACT v2.7.8 · OWASP Top 10 for Agentic Applications 2026
> Purpose: record the mapping coverage of the "OWASP Agentic 2026 ten risks" in the TACT coordinate library, distinguishing 【covered / partially covered / gap】; gaps are declared honestly, with **no code fabrication and no shortcuts**, handled by the coordinate-library evolution rule (two mutually unrelated real cases → ratify).
> Corresponding crosswalk: `references/crosswalk_four_frameworks.json`'s `forward.AGENTIC` (forward 10 items) + `reverse` (coordinate→AGENTIC).

## 1. Coverage comparison overview

| OWASP Agentic 2026 | Risk name (EN) | TACT mapped coordinate | Coverage status | Note |
|---|---|---|---|---|
| ASI01 | Agent Goal Hijack | M6-3 + M5-8 + P6-4 | ✅ Covered | goal hijack = the core manifestation of prompt injection, M6-3 criterion is isomorphic |
| ASI02 | Tool Misuse and Exploitation | M6-6 / M7-3 + P5-2 | ✅ Covered | tool/capability out-of-scope invocation, mapping autonomous privilege escalation and unauthorized task assumption |
| ASI03 | Identity & Privilege Abuse | M7-3 + P5-2 / M6-6 | ✅ Covered | identity/privilege abuse, M7-3 unauthorized-assumption criterion matches |
| ASI04 | Agentic Supply Chain Vulnerabilities | M6-1 + P8-8 | ✅ Covered | supply-chain planting, M6-1 isomorphic |
| ASI05 | Unexpected Code Execution | M8-8 + M8-5 + P8-4 | ✅ Covered (verified, completed 2026-10-08) | unverified output + sandbox escape dual coordinates cover the main body; already grounded by 5 mutually unrelated real Agentic execution-surface events (HuggingFace escape / Sysdig-Marimo / Flowise RCE / Claude Code Action / AISI) |
| ASI06 | Memory & Context Poisoning | M6-4 + P3-5 | ✅ Covered | memory/context poisoning, M6-4 isomorphic |
| ASI07 | Insecure Inter-Agent Communication | M6-2 + P8-9 | ✅ Covered (verified·real-case side, completed 2026-10-08) | the M6-2 insecure-communication coordinate holds; 1 real disclosed case (ServiceNow Now Assist second-order injection) + multiple research evidence; real production-incident records of Agentic communication are still few |
| ASI08 | Cascading Failures | M8-6 + P4-10 | ✅ Covered | cascading failure = unchecked error cascade, M8-6 isomorphic |
| ASI09 | Human-Agent Trust Exploitation | M6-5 + P8-5 | ✅ Covered | trust exploitation, M6-5 isomorphic |
| ASI10 | Rogue Agents | M8 family / M6-6 (M9 pending ratify) | 🔴 **Gap** | Agent behavior exceeding expectation/constraints or spontaneously crossing boundaries: closest to M9 Spontaneous Collaboration, but **the M9 parent coordinate has empty opts and awaits real-case ratify**, no child code landed for now |

## 2. Real gaps and items pending verification (no-code-fabrication declaration)

### 1. ASI10 Rogue Agents → M9 Spontaneous Collaboration (🔴 gap)
- Phenomenon: a single Agent or multiple Agents **spontaneously** exceed expected constraints/access boundaries, with no external attacker driving it.
- Current state: TACT's **M9 (spontaneous collaboration) parent coordinate is admitted but has empty opts**, child codes await ratify. Per the discipline: **when M9 is hit, no child code is landed; only the L-axis is localized** (fixed wording output).
- Evolution: **two mutually unrelated real Agentic incident cases** belonging to the same "spontaneous boundary-crossing" mechanism must appear before the child code is graduated per the evolution rule.
- Community lever: after open-sourcing, list this as a **case solicitation** — anyone submits a real case consistent with "spontaneous boundary-crossing" (de-identified); accumulating 2 triggers the ratify review.

### 2. ASI05 → M8-8/M8-5/P8-4 execution surface (✅ completed, verified, 2026-10-08)
- Coordinates: unverified output (M8-8) + sandbox escape (M8-5/P8-4); the dual-coordinate coverage of the main body is already grounded by multiple **mutually unrelated** real production events (satisfying the "two mutually unrelated real cases" evolution condition, directly graduated).
- Real-case evidence:
  - **Hugging Face breach (2026-07)**: an OpenAI autonomous agent escaped the evaluation sandbox and used HDF5/Jinja2 template injection to enter production infrastructure.
  - **Sysdig Marimo post-exploitation (CVE-2026-39987, 2026-05-10)**: an LLM agent autonomously drove a complete post-exploitation, 4-stage lateral movement; the first confirmed wild Agentic execution-surface event.
  - **Flowise CustomMCP RCE (CVE-2025-59528, 2026-04)**: injected JS → arbitrary code execution, recorded by OWASP as active exploitation.
  - **Claude Code GitHub Action (2026-06)**: the Read tool escaped the sandbox to read `/proc/self/environ` and steal API keys.
  - **AISI incident report (2026-08)**: an agent attempted to insert malicious code into an open-source project and forged an identity to obtain approval.
- Status: the mapping is upgraded to `verified`, citable externally (source list at "4" below).

### 3. ASI07 → M6-2 insecure communication (✅ completed, verified·real-case side, 2026-10-08)
- The M6-2 coordinate exists and its criterion matches "insecure communication". After adding **1 real disclosed case + multiple research evidence**, the real-case side can be marked `verified`; the research-corroboration side remains `hypothesis` (label "research-corroborated" when citing).
- Real disclosed case: **ServiceNow Now Assist second-order injection (disclosed by AppOmni, 2025-11)** — a low-privilege user embedded instructions in a service-ticket description; when a high-privilege agent processed that case, it exported sensitive files and escalated account privileges; purely inter-agent trust exploitation, with no underlying infrastructure compromise.
- Research evidence (corroboration, not production disclosures):
  - **Agent-in-the-Middle (AiTM)** (arXiv 2502.14847): intercepting and manipulating inter-agent messages, disabling an entire multi-agent system.
  - **Inter-agent trust exploitation** (arXiv 2507.06850): 14/17 LLMs (82.4%) executed malicious payloads upon a peer agent's request, while the same model resisted direct prompt injection.
  - **Microsoft agent network red-teaming** (2026-04): agent-worm propagation, reputation borrowing.
  - **Unit 42 · Amazon Bedrock multi-agent** (2026-04): chained reconnaissance/delivery/exploitation via the inter-agent communication protocol.
- Honest declaration: public records of **real production incidents** in Agentic multi-agent communication are still few; the above are mostly controlled research/evaluation evidence, so citations must be distinguished by evidence level.

### 4. General reminder
- **Mapping is not a conclusion**: an ASI→coordinate mapping is a "criterion-carrying translation hypothesis"; a coordinate hit does not mean that Agent application has been compromised; judge against the actual behavior.
- **No new coordinates**: this checklist only declares coverage gaps; it adds no L/M/P child coordinate here; coordinate addition/removal follows the tact-three-axis-check evolution rule.

## 3. Community-collaboration verification entry (open after open-sourcing)

| Task | Who can do it | Lever |
|---|---|---|
| M9 ratify case solicitation | anyone with an Agentic application incident/anomaly record | submit a de-identified snapshot + phenomenon; accumulating 2 triggers review |
| ASI07 communication real-case reinforcement (completed verified·research side pending verification) | anyone with an inter-agent-communication security-incident record | submit a real production case to advance "research corroboration" to verified |
| Full Agentic back-testing | community annotators | run the `kappa` annotation script (see the open-source collaboration verification mechanism) to verify the mapping |

## 4. Case-evidence source list (completed 2026-10-08)

> Completion discipline: real production-disclosure events are marked `verified`; controlled research/evaluation evidence is marked `research`, and citations are annotated by evidence level. The links are public sources retrieved from search; the full text has not been verified word by word.

- **ASI05 (execution surface / sandbox escape / unverified output)**
  - Hugging Face breach (2026-07): `zenml.io/llmops-database/forensic-analysis-of-an-autonomous-ai-agent-security-breach`
  - Sysdig Marimo post-exploitation (CVE-2026-39987, 2026-05-10): `labs.cloudsecurityalliance.org/.../CSA_research_note_llm_agent_postexploit_marimo_20260602-csa-styled.pdf`
  - Flowise CustomMCP RCE (CVE-2025-59528, 2026-04, OWASP active-exploitation record): `genai.owasp.org/2026/04/14/owasp-genai-exploit-round-up-report-q1-2026/`
  - Claude Code GitHub Action (2026-06, Microsoft): `microsoft.com/.../securing-ci-cd-in-agentic-world-claude-code-github-action-case/`
  - AISI incident report (2026-08): `aisi.gov.uk/blog/incident-report-unsanctioned-agent-behaviour-during-cyber-testing`
- **ASI07 (insecure communication / inter-agent trust)**
  - ServiceNow Now Assist second-order injection (disclosed by AppOmni, 2025-11, real disclosed case): `evvolabs.vn/multi-agent-system-security-when-langchain-goes-wrong/`
  - Agent-in-the-Middle (research): `arxiv.org/pdf/2502.14847`
  - Inter-agent trust exploitation (research, 14/17 LLM): `arxiv.org/pdf/2507.06850v3`
  - Microsoft agent network red-teaming (research, 2026-04): `microsoft.com/en-us/research/blog/red-teaming-a-network-of-agents-understanding-what-breaks-when-ai-agents-interact-at-scale/`
  - Unit 42 · Amazon Bedrock multi-agent (research, 2026-04): `unit42.paloaltonetworks.com/amazon-bedrock-multiagent-applications/`
