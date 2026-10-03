# Implementation Self-Report v0.1

_Status: Informative_
_Date: 2026-10-03_

This note describes a machine-readable declaration a deployment could emit from inside itself. The declaration names the protocol version the deployment claims, the capabilities it classifies as required or optional, the extensions and representation mappings it declares, the surfaces that declaration covers, and an explicit declaration-versus-verified status.

Issue #8 asks for several distinct pieces of work. This note is the self-report piece. A conformance definition, a requirement-level split, an extension mechanism, and a conformance test remain open. This note assigns no conformance result and certifies nothing.

## Where this note sits

Informative notes live in `notes/`. This document describes a declaration a deployment could publish. Encoding, signature, and assurance profiles live in `conformance/profiles/`, where each profile declares algorithms and verifier dependencies. Expectation matrices live in `conformance/expectations/`. This declaration has neither of those contents, so it stays here.

The shape identifier below is a label for this informative note. A later protocol document may adopt another identifier.

## A self-report is a declaration

A self-report is a declaration until an independent check verifies it. `evaluation_status` makes that distinction explicit.

| Status | Meaning |
|---|---|
| `declared` | The deployment emitted the statement. `independent_check` is null. |
| `verified` | The statement cites an independent check. That check's own record is the verification. |

The status word sits inside a document the deployment can write. It becomes evidence of verification when the statement cites a separate check record: a checker role, a check identifier, and the digest of the declared bytes that checker evaluated. This note defines no checker, no procedure, and no pass criteria.

A deployment that emits no self-report has produced no declaration for anyone to verify.

## What the declaration contains

A declaration is one JSON object. The fields below are the informative v0.1 shape. They are labels for a statement a deployment could make.

`self_report` identifies this shape: `smp-implementation-self-report/v0.1`. That identifier is the declaration format. It is separate from the protocol version the deployment claims.

`declaring_authority` names the authority the deployment attributes the statement to. The examples use Primary Users.

`deployment_id` is the deployment's own label for the system the statement describes.

### Protocol version

`protocol_version` carries:

- `protocol`, the protocol name;
- `version_label`, the version string the deployment claims;
- `document_pins`, each with a repository `path` and a `role` of `claimed`;
- `profile_pins`, the encoding, signature, or assurance profiles the deployment claims.

A pin records a claim. This note publishes no released protocol version. The synthetic examples use the label `unreleased-draft`. An empty `profile_pins` array means the deployment declares no profile.

### Required and optional capabilities

`capabilities.required` and `capabilities.optional` are the deployment's own lists. Each entry has an `id` and a `claim` of `provided` or `not_implemented`.

In this declaration, required means the deployment includes that capability in the claim it makes for its covered surfaces. Optional means the deployment lists the capability and records whether it provides it. Which capabilities would be mandatory for a named profile is a conformance question. This note leaves that question open.

These identifiers describe protocol behavior the deployment claims to implement. They are not capability grants, and they authorize no operation. See [spec/10-capability-and-policy-v0.1.md](../spec/10-capability-and-policy-v0.1.md) for the separate authority contract.

### Declared extensions

`extensions` lists behavior the deployment adds beyond the documents it pins. Each entry has an `id`, a `criticality` of `critical` or `noncritical`, and a `summary`.

Criticality here is the value the deployment declares, using the labels already present in the custody drafts. This note adds no rule for unknown extensions. An extension entry announces that the behavior exists in the deployment. Admission of that behavior into the protocol is separate work.

### Representation mappings

`representation_mappings` pairs a protocol concept with the deployment's local representation. Each entry has `protocol_concept`, `deployment_representation`, and a `summary`.

A mapping states how the deployment stores or names a concept. The local representation remains the deployment's representation. The examples below are synthetic stand-ins, built for this note, and describe no running system.

### Covered surfaces

`covered_surfaces` names the surfaces the declaration speaks for. Each entry has an `id` and `coverage` of `included`. The list is the whole covered set for that statement. A surface absent from the list lies outside the declaration. Coverage at this layer is the deployment's statement of scope. A test result would come from an independent check.

### Declaration-versus-verified status

`evaluation_status` is `declared` or `verified`.

When the status is `declared`, `independent_check` is null.

When the status is `verified`, `independent_check` carries:

- `checker`, a role name for the independent checker;
- `check_id`, a stable identifier;
- `declaration_digest`, the digest of the declaration in its `declared` form, with `independent_check` null;
- `artifact`, a locator for the check record.

The verified form cites that digest. It does not replace the check record. The examples use a placeholder digest because this note computes nothing.

## Synthetic example: declaration only

```json
{
  "self_report": "smp-implementation-self-report/v0.1",
  "declaring_authority": "Primary Users",
  "deployment_id": "example-deployment-01",
  "evaluation_status": "declared",
  "independent_check": null,
  "protocol_version": {
    "protocol": "smp",
    "version_label": "unreleased-draft",
    "document_pins": [
      {"path": "spec/01-records.md", "role": "claimed"},
      {"path": "spec/02-provenance-and-custody.md", "role": "claimed"},
      {"path": "spec/05-verification.md", "role": "claimed"}
    ],
    "profile_pins": []
  },
  "capabilities": {
    "required": [
      {"id": "protocol.evidence-lineage", "claim": "provided"},
      {"id": "protocol.authority-at-write", "claim": "provided"}
    ],
    "optional": [
      {"id": "protocol.signed-checkpoint", "claim": "provided"},
      {"id": "protocol.bilateral-transfer", "claim": "not_implemented"}
    ]
  },
  "extensions": [
    {
      "id": "example.operator-color-tag/v0",
      "criticality": "noncritical",
      "summary": "A local operator color tag stored beside a record. The tag is display metadata."
    }
  ],
  "representation_mappings": [
    {
      "protocol_concept": "observed-time",
      "deployment_representation": "field seen_at on object example_observation",
      "summary": "Synthetic timestamp field for the observed-time claim."
    },
    {
      "protocol_concept": "projection",
      "deployment_representation": "rebuildable index example_search_index",
      "summary": "Synthetic derived index. The index is rebuildable projection state."
    }
  ],
  "covered_surfaces": [
    {"id": "custody-append", "coverage": "included"},
    {"id": "lineage-read", "coverage": "included"},
    {"id": "export-bundle", "coverage": "included"}
  ]
}
```

Read this example as a statement by Primary Users about `example-deployment-01`:

- The protocol claim is the unreleased draft, limited to the three pinned documents, with no profile pin. Any other document is outside this claim.
- Evidence lineage and authority-at-write are included as required capabilities the deployment says it provides. Signed checkpoint is optional and stated as provided. Bilateral transfer is optional and stated as not implemented.
- The color-tag extension is declared noncritical local metadata.
- Observed time is mapped to `seen_at`. Projection is mapped to `example_search_index`.
- The declaration covers custody append, lineage read, and export bundle. Restore, erasure, and any surface left off the list are outside this statement.
- `evaluation_status` is `declared`. No independent check is cited.

## Synthetic example: the same statement citing a check

A later, separate check could be cited by changing only the status and the citation. The digest below is the placeholder `example-digest-not-computed`. It stands in for a digest of the declared form; this note did not calculate one.

```json
{
  "self_report": "smp-implementation-self-report/v0.1",
  "declaring_authority": "Primary Users",
  "deployment_id": "example-deployment-01",
  "evaluation_status": "verified",
  "independent_check": {
    "checker": "example-independent-checker",
    "check_id": "example-check-1001",
    "declaration_digest": "example-digest-not-computed",
    "artifact": "example-checks/example-check-1001.json"
  },
  "protocol_version": {
    "protocol": "smp",
    "version_label": "unreleased-draft",
    "document_pins": [
      {"path": "spec/01-records.md", "role": "claimed"},
      {"path": "spec/02-provenance-and-custody.md", "role": "claimed"},
      {"path": "spec/05-verification.md", "role": "claimed"}
    ],
    "profile_pins": []
  },
  "capabilities": {
    "required": [
      {"id": "protocol.evidence-lineage", "claim": "provided"},
      {"id": "protocol.authority-at-write", "claim": "provided"}
    ],
    "optional": [
      {"id": "protocol.signed-checkpoint", "claim": "provided"},
      {"id": "protocol.bilateral-transfer", "claim": "not_implemented"}
    ]
  },
  "extensions": [
    {
      "id": "example.operator-color-tag/v0",
      "criticality": "noncritical",
      "summary": "A local operator color tag stored beside a record. The tag is display metadata."
    }
  ],
  "representation_mappings": [
    {
      "protocol_concept": "observed-time",
      "deployment_representation": "field seen_at on object example_observation",
      "summary": "Synthetic timestamp field for the observed-time claim."
    },
    {
      "protocol_concept": "projection",
      "deployment_representation": "rebuildable index example_search_index",
      "summary": "Synthetic derived index. The index is rebuildable projection state."
    }
  ],
  "covered_surfaces": [
    {"id": "custody-append", "coverage": "included"},
    {"id": "lineage-read", "coverage": "included"},
    {"id": "export-bundle", "coverage": "included"}
  ]
}
```

`example-independent-checker` and `example-check-1001` are placeholders. No such check exists. The citation shows where a real check record would be named. The check record, once it exists, carries the result. This self-report only points at it.

## Relation to the current drafts

[spec/06-conformance.md](../spec/06-conformance.md) already says this draft defines no single binary conformance claim, and that reports identify profile, version, fixtures, implementation version, and tested surfaces. This note describes the deployment statement that could supply the version, profile pins, and covered surfaces for such a report. It does not add fixtures or outcomes.

[ROADMAP.md](../ROADMAP.md) lists implementation self-description as later protocol work: protocol and profile pins, representation mappings, and explicit extensions. [STATUS.md](../STATUS.md) still marks that area as a proposed extraction. [Open questions](open-questions/README.md) still include self-declaration versus independent conformance review. This note illustrates that distinction for the self-report. It does not close the question, and it does not amend those documents.

## Claim limits

- Emitting the JSON records a declaration.
- `evaluation_status` of `verified` is meaningful together with the cited check record.
- Covered surfaces bound the statement.
- Required and optional classify the deployment's claim.
- The examples are synthetic. They name Primary Users, `example-deployment-01`, and placeholder check identifiers only.
