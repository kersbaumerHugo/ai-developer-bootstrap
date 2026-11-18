# AI Developer Bootstrap — Engineering Instructions

## Mission
Build a reproducible developer environment bootstrap.
Tucano is the first candidate for multi-agent DevEx.
OpenCode is the initial development harness.

## Engineering principles
- Git is the source of truth.
- Vertical Slice First.
- Complexity Must Earn Its Place.
- Evidence over Claims.
- Reuse Before Rebuild.
- Prefer small, independently verifiable changes.

## Working rules
- Inspect the repository before making changes.
- Explain the chosen implementation briefly.
- Implement one bounded capability per iteration.
- Add appropriate automated tests.
- Run validations and report actual results.
- Never fabricate execution evidence.
- Never commit secrets, tokens or local databases.
- Never run sudo, destructive commands, or
  install host software without explicit approval.
- Do not push, merge or create remote repositories
  without approval.

## Architecture boundaries
- Bootstrap owns desired configuration and verification.
- Tucano owns candidate multi-agent user experience.
- Harnesses remain interchangeable.
- Runtime state and credentials remain outside Git.
- Do not modify Tucano upstream in the first slice.
- Do not add Kubernetes, Terraform, Ansible, ai-jail
  or ai-memory without a demonstrated need.

## Initial target
Debian 13, starting on dev01.

## Development cycle
Implement -> Validate -> Understand ->
Experiment -> Consolidate.
