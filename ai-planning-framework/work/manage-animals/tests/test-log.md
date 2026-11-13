# Test log — manage-animals

| Run | Date time (BST) | Pass / Fail / Blocked | Test-fix | Report |
|-----|-----------------|-----------------------|----------|--------|
| 1 | 2026-10-08 19:27 | 0/0/75 (75 Waiting on scaffolding + env; overall blocked) | test-fix 0/5 | tests/TEST-manage-animals-1-report.md |
| 2 | 2026-10-09 08:39 | 76/0/1 (unit 45 pass + 2 Skip; e2e + harness 64/64 run 5; T-007 S8 @skip not run; overall passed) | test-fix 0/5 (first-run self-fixes F1–F6) | tests/TEST-manage-animals-2-report.md |
| 3 | 2026-10-09 09:22 | 76/0/1 (**Tests blocked: T-007/S8**; unit 52/52; e2e + harness 66/66 + 6 setup, run 9; password scan 0 hits; overall blocked. Addendum 09:48 on Dev Bot 09:35 code: test-code fixes for Dev Bot 09:27, --trace=on probe setup-trace leak fixed (0 hits, probe deleted), unit 52/52, e2e 66/66 + 6 setup run 10, scan 0, counts unchanged. Addendum 2 09:56: T-007/S8 unblocked (Neil 09:46) and passes; e2e 67/67 + 6 setup run 11; scan 0; 77/0/0, status passed) | test-fix 1/5 (Review Bot F-41–F-47) | tests/TEST-manage-animals-3-report.md |
