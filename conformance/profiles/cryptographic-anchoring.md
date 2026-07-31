# Cryptographic Anchoring Profiles for SMP

_Status: informative research draft; no service, account, key, transaction, or deployment is authorized_
_Version: 0.1.0-draft.1_
_Last updated: 2026-07-31T10:13:54-04:00_
_Related: `../../spec/08-immutability-and-chain-of-custody.md`_

## 1. Decision to support

SMP needs the least complex mechanism that can:

- detect ordinary and privileged history mutation;
- show ordered append relative to a previously observed head;
- verify offline from portable evidence;
- preserve provider exit;
- avoid disclosing subject data or trust-domain structure;
- survive signer rotation and algorithm migration;
- report stale, partial, offline, and unavailable witness coverage;
- add multi-party consensus only when the authority model actually requires it.

Anchoring is evidence of commitment existence and ordering. It is not proof of source truth, legitimate authority, completeness, lawful retention, or erasure.

## 2. Baseline before any external anchor

Every conforming L2-style deployment should first produce a portable signed checkpoint containing:

- stream/profile and algorithm-suite identifiers;
- event count/tree size;
- root and last-event hashes;
- issue time and signer key reference;
- signature and historical key-transition evidence;
- inclusion/consistency proof material or enough retained leaves to reproduce it;
- verifier and export receipts.

An independent copy of that checkpoint is the first witness. If the authority store is rewritten but every witness copy is controlled by the same account, host, or operator, the independence claim is weak and must be stated as such.

## 3. Candidate profiles

| Profile | What it adds | Trust and operational cost | Privacy/erasure posture | Offline/provider-exit posture | SMP disposition |
|---|---|---|---|---|---|
| Signed checkpoint retained independently | Detects divergence from a prior head; no third-party service required | Signer and witness custody; no consensus | Keep roots opaque and domain-separated; witness timing still leaks activity | Strong if checkpoint, keys, proofs, and verifier are exported | **Required foundation** |
| RFC 3161 Time-Stamp Protocol | A TSA signs an assertion that a digest existed before a time | Trust in TSA identity, certificate status, policy, time source, and archival evidence | Submit only an opaque checkpoint digest; TSA still learns timing and client metadata | Portable tokens exist, but long-term verification needs certificate/policy/revocation evidence and algorithm renewal | **Preferred simple external-time profile when one independent TSA is sufficient** |
| OpenTimestamps / Bitcoin calendar | Publicly verifiable proof that a digest existed before a Bitcoin commitment; calendar aggregation can avoid direct transaction fees | Calendar availability for stamping/upgrading; Bitcoin verification and confirmation latency; public-chain dependency | Browser/client can hash locally; opaque roots still permit timing/correlation; never submit private identifiers | Proof files can verify independently with retained chain/header evidence and tooling; provider account not required | **Optional public timestamp profile for non-sensitive opaque roots** |
| Transparency log such as Rekor-style verifiable log | Public append-only inclusion and monitorable consistency; supports independent auditors | Log operation or external service, monitoring, split-view defenses, schema/entry-type fit | Public metadata is durable and difficult to erase; only opaque aggregate checkpoints should be considered | Export signed tree heads, inclusion/consistency proofs, keys, and monitor observations; service availability must not be required after export | **Optional ecosystem/witness profile, not the base custody store** |
| Signed Git tag/release plus independent mirrors | Familiar distribution and immutable-by-convention release receipt | Hosting/account trust; Git history can be rewritten; signature and mirrors are essential | Public repository timing and metadata leak; not suitable for private stream IDs | Good portability, but not strong independent time or consensus by itself | **Supplementary publication receipt only** |
| Hyperledger Fabric permissioned ledger | Deterministic finality and ordered state among governed organizations; endorsement/orderer policies model multi-party control | Highest cost: organizations, identities/MSPs, channels, orderers, peers, policy, upgrades, backup, quorum, incident response | Private-data collections keep data among authorized peers but channel peers retain hashes; membership and transaction metadata persist; erasure is governance-heavy | Provider-neutral software, but operational exit requires complete ledger, MSP, policy, key, and chaincode custody | **Defer unless mutually distrustful custodians need shared ordering** |

For ordinary external time evidence, the preferred candidate profile is RFC
3161/5816. A higher-assurance deployment should use two independently
administered RFC 3161 TSAs or combine RFC 3161 with OpenTimestamps so one PKI or
one witness mechanism is not the sole external dependency. This is a proposed
profile-selection rule, not authorization to procure a TSA or publish a digest.

## 4. Primary-source observations

### RFC 8785 — deterministic JSON

RFC 8785 states that hashing/signing needs an invariant representation. JCS constrains data to I-JSON and deterministic property sorting, forbids duplicate property names, and limits JSON numbers to IEEE 754 values; longer integers are recommended as strings. SMP's draft therefore uses strings for unbounded counters and requires a complete interoperability vector before release.

Source retrieved 2026-07-31: <https://www.rfc-editor.org/rfc/rfc8785.txt>

### RFC 9162 — transparency-log properties

RFC 9162 describes append-only logs built with Merkle trees, inclusion proofs, consistency proofs, and signatures. It also warns by construction that logs make misbehavior detectable; they do not themselves prevent misissuance. SMP applies that limited claim to custody checkpoints and does not import Certificate Transparency's certificate-specific policy.

Source retrieved 2026-07-31: <https://www.rfc-editor.org/rfc/rfc9162.txt>

### RFC 3161 — independent time assertion

RFC 3161 specifies requests to and responses from a Time Stamping Authority and describes proof that a datum existed before a particular time. It adds TSA trust and certificate-policy dependencies; it does not prove who created the datum, its semantic truth, or that the submitted digest represents a complete stream.

RFC 5816 updates RFC 3161 so the timestamp-signing certificate identifier can use a hash other than SHA-1. A released SMP timestamp profile must therefore pin the modern certificate-identifier and digest suites rather than treating the original 2001 defaults as sufficient.

Sources retrieved 2026-07-31:

- <https://www.rfc-editor.org/rfc/rfc3161.txt>
- <https://www.rfc-editor.org/rfc/rfc5816.txt>

### OpenTimestamps

The official site describes a proof format for independently verifiable timestamps, currently using Bitcoin, and says calendar servers aggregate submissions without registration or API keys. Its browser stamper calculates a hash locally. The official client distinguishes an initially incomplete calendar proof from the upgraded proof that reaches Bitcoin. Creation does not require a local Bitcoin node, while independent verification with the official client requires Bitcoin Core; a pruned node is sufficient. The profile is still tied to Bitcoin proof semantics and calendar/upgrade behavior, and public timing can correlate activity. Preserve the completed `.ots` proof and report pending upgrade state rather than presenting a calendar response as final Bitcoin evidence.

Sources retrieved 2026-07-31:

- <https://opentimestamps.org/>
- <https://github.com/opentimestamps/opentimestamps-client/blob/master/README.md>

### Sigstore Rekor

Sigstore documentation describes Rekor as an immutable, tamper-resistant public ledger of software-supply-chain metadata. It states that auditors can monitor consistency and entries are not mutated or removed; Sigstore's security model also makes third-party monitoring material to detecting log/Fulcio misbehavior. That public non-removal posture conflicts with private subject metadata and erasure needs unless SMP submits only opaque aggregate checkpoint material. Rekor's public service and entry schemas are supply-chain infrastructure, not a general SMP authority store. Offline retention must include the exact bundle/evidence version, historical signed heads and consistency material, and the applicable historical TUF-distributed trust roots rather than silently fetching current online state.

Sigstore's timestamp documentation makes an important separation: Rekor v1's `integratedTime` came from Rekor's internal clock, was not externally verifiable, and was not part of the append-only node, so that timestamp could change without log detection. Rekor v2 obtains a signed timestamp from a separate timestamp authority. SMP must likewise report log inclusion and independent time evidence as separate outcomes.

Sources retrieved 2026-07-31:

- <https://docs.sigstore.dev/logging/overview/>
- <https://docs.sigstore.dev/cosign/verifying/timestamps/>
- <https://docs.sigstore.dev/about/bundle/>
- <https://docs.sigstore.dev/about/security/>

### Hyperledger Fabric

Fabric documentation describes a permissioned ordering service with deterministic consensus and final blocks rather than probabilistic forks. Fabric 3.x documents a BFT orderer for a threat model with fewer than one third of orderer operators malicious or compromised. Private-data documentation says actual private data is gossiped only to authorized organizations while a hash is endorsed, ordered, and written to every peer's ledger for validation/audit. Fabric can therefore support real multi-organization ordering but does not eliminate hash privacy, metadata, identity, governance, or erasure concerns. If one administrator controls all peers, orderers, CAs, and membership policy, the machinery does not create an independent witness.

Sources retrieved 2026-07-31:

- <https://hyperledger-fabric.readthedocs.io/en/latest/orderer/ordering_service.html>
- <https://hyperledger-fabric.readthedocs.io/en/latest/private-data/private-data.html>

### Public Git publication limits

Git object addressing and signatures are useful integrity and distribution
receipts, but ordinary author/committer dates are caller-supplied, remote refs
can be force-updated or deleted, and SHA-1 repositories retain known collision
risk. A Git publication becomes independent evidence only when another party
clones, archives, mirrors, or separately timestamps the exact object. SMP must
therefore treat a public Git ref as a convenience witness, not trusted civil
time or an immutable ledger.

Sources retrieved 2026-07-31:

- <https://git-scm.com/docs/hash-function-transition>
- <https://git-scm.com/docs/gitformat-signature>
- <https://git-scm.com/docs/git-commit-tree>
- <https://git-scm.com/docs/git-push>

## 5. Threat-model fit

| Threat | Signed local checkpoint | Independent copy | RFC 3161 | Public timestamp/log | Fabric |
|---|---:|---:|---:|---:|---:|
| Routine application rewrite | detects/prevents with local enforcement | detects | detects relative to token | detects relative to public receipt | detects under ledger policy |
| Privileged database rewrite | detects if signer evidence survives | detects if witness is independent | detects anchored checkpoint divergence | detects anchored checkpoint divergence | detects unless colluding policy/quorum can rewrite/rebuild evidence |
| Silent truncation after last anchor | not detected | detected only if witness has later head | detected only through latest token | detected only through latest public head | depends on peers/orderers and retained state |
| Fork/equivocation | local chain identifies fork but cannot select truth | witnesses can expose disagreement | tokens prove existence, not select branch | consistency monitors/gossip can expose split views | consensus/policy selects final order |
| False or unauthorized semantic claim | not solved | not solved | not solved | not solved | endorsement may express policy but does not prove external truth |
| Erased payload recovery | not solved by anchoring | not solved | not solved | public receipts can worsen metadata permanence | private collections/purge policy help operations but hashes/metadata persist |
| Multi-party distrust | one signer insufficient | multiple witnesses can detect but not order writes | multiple TSAs witness time but do not arbitrate writes | log orders accepted submissions but does not supply principal governance | strongest candidate when governed organizations must agree |

## 6. Recommended staged architecture

### Stage A — base protocol

1. Canonical event bytes and per-stream predecessor hashes.
2. Strict append serialization and field immutability enforcement.
3. Signed Merkle checkpoint over a declared stream prefix.
4. Portable verifier, key-transition history, inclusion/consistency proof material, and export/restore receipt.
5. Structured coverage that never upgrades “internally valid” to “globally complete.”

### Stage B — independent witness

Retain the signed checkpoint outside the primary authority store under a separately recoverable custody path. Test loss, stale witness, fork, and restore behavior. This can be local/offline and does not require a vendor.

### Stage C — optional external time/transparency profile

For deployments needing independent public time, prefer an opaque aggregate checkpoint digest submitted to one or more RFC 3161 TSAs or OpenTimestamps. A transparency log is reasonable only when public permanence and monitor operations are acceptable. Export every receipt needed for offline/provider-exit verification.

### Stage D — permissioned consensus

Evaluate Fabric or another consensus ledger only when all are true:

- two or more organizations or principals are mutually distrustful writers/custodians;
- they require a shared final ordering decision, not merely tamper detection;
- governance defines membership, endorsement, quorum, onboarding/offboarding, incident response, and dispute handling;
- metadata persistence and private-data hash retention are acceptable;
- erasure and provider-exit drills pass;
- operating cost is lower than the risk reduced.

Single-administrator deployments ordinarily do not meet this threshold.

## 7. External-disclosure minimization

An external anchor payload should contain only a domain-separated aggregate digest and profile identifier needed for verification. It should not contain:

- principal, person, account, project, deployment, or record identifiers;
- stream names or raw event counts when they reveal sensitive activity;
- payload, plaintext digest, source locator, reason, or classification;
- key or credential locators beyond a deliberately public verification key reference.

Batching, cadence, and separate domain keys can reduce but not eliminate timing and correlation leakage. Separately governed custody domains must not share an aggregate checkpoint absent explicit leakage analysis and authorization.

## 8. Offline and algorithm-lifecycle requirements

A portable anchor package must retain, as applicable:

- signed checkpoint bytes and signatures;
- signer public keys, introductions, rotations, revocations, and compromise statements;
- TSA token, certificates, policy identifiers, and long-term validation evidence;
- transparency-log signed heads, inclusion and consistency proofs, log keys, and monitor observations;
- OpenTimestamps proof and required chain/header verification evidence or a documented reproducible retrieval path;
- Fabric channel configuration, MSP/policy history, blocks, private-data coverage statement, chaincode/config versions, and verification tooling;
- algorithm-suite identifiers and a renewal/migration event linking old and new commitments.

Checkpoint-signing key operations should use an isolated signer or HSM-class
boundary where the deployment threat model warrants it, short explicit key
epochs, immutable public-key/validity history, authenticated old-to-new rotation
where possible, and separately witnessed final-old/first-new checkpoints. A
compromise declaration must preserve the last trusted checkpoint and suspect
interval rather than rewriting prior evidence.

A verifier must report expired algorithms, missing revocation evidence, unavailable network dependencies, stale witnesses, and unverified intervals. It must not silently fetch mutable online state and call the result offline verification.

## 9. Recommendation

Adopt the signed hash-chain/Merkle checkpoint contract as the proposed base design. Make external anchoring pluggable and opaque. Use an independent retained copy first; add RFC 3161 or OpenTimestamps only when independent time materially improves the threat model. Do not adopt Hyperledger now. Preserve it as a future multi-party ordering profile with a concrete trigger and conformance gate.

## 10. Coverage limits

The configured `web_search` backend was unavailable on 2026-07-31, so broad discovery coverage is incomplete. The observations above were retrieved directly from named primary-source URLs and do not include a comprehensive product/version survey, legal analysis, cost quote, service-SLA verification, or hands-on interoperability test. Peer research and skeptical review should be reconciled before this note is promoted.
