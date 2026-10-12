# Agent rules for this repo

- Never fabricate, estimate, or hand-edit results, numbers, figures, accessions, or citations. Every number in MANUSCRIPT.md must come from a file in `results/` produced by code in this repo.
- If a step fails (download blocked, no network, tool missing), stop that step, record the exact error in `docs/RUNLOG.md`, and report it. Do not substitute made-up data.
- Keep simulated and real results clearly separated and labelled (`results/simulated/` vs `results/real/`).
- Mark any script you have not actually executed as UNTESTED.
- Before finishing, run `make demo` and confirm it still passes.
- Cite only references you can verify; otherwise leave a `TODO: verify` marker.
