# Repo Governance Kernel Preview

This repository currently prepares the internal preview release of
`repo-governance-kernel`.

The reusable package surface lives under [`kernel/`](./kernel/).
The `projects/session-memory/` tree remains the host-local dogfood sample and is
not part of the package contract.

Preview release notes are in [`RELEASE.md`](./RELEASE.md).
Package-facing usage and support-boundary notes are in
[`kernel/README.md`](./kernel/README.md).

The current preview now includes a kernel-owned shadow host adoption assessment
surface for governed external repos. It is still an alpha observation/reporting
path, not a general live-host rewrite promise.

For `external-target-shadow`, the preview now also includes a draft surface that
turns the external repo's observed dirty paths into suggested round/task scope
before the real assessment runs. That draft artifact is now distinct from the
later shadow-adoption report instead of reusing one overloaded owner label.

It also now includes one bounded workflow wrapper that can draft scope, rewrite
the active round/task, refresh the anchor, and run the assessment in one pass.

That workflow is now bundle-backed, and there is also one bounded natural-language
entry for the same single-assessment path.

The bootstrap validation path now also proves one installed wheel can bootstrap
and audit a disposable host repo from an isolated environment, not only from
the source tree.
