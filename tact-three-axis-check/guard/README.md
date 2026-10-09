# TACT Toolkit Version Lock and Permission Protection (guard/)

This directory provides "version lock + integrity check + write-lock convention" to prevent controlled files from being rolled back/tampered with by external processes (this once happened on 2026-10-01: the v1.1.0 finalized changes were externally rolled back to v1.0.3).

## Controlled files
- `SKILL.md` (criterion guidance, v1.1.1)
- `references/calibration_cases.json` (calibration set, v1.2.0)
- `references/coordinate_data.json` (coordinate base, v2.7.8, **never modified**)

## The three tools
| Tool | Purpose | Usage |
|---|---|---|
| `verify.sh` | **Integrity check**: compares the SHA-256 of controlled files against the MANIFEST baseline; alerts on rollback/tampering (exit 1) | `guard/verify.sh` |
| `lock.sh` | Sets controlled files to read-only 444, preventing accidental writes / low-privilege overwrites | `guard/lock.sh` |
| `unlock.sh` | Restores controlled files to writable 644, **only used when finalizing edits**; refuses to unlock if a `LOCK` file exists | `guard/unlock.sh` |

`MANIFEST.json` is the SHA-256 + version baseline; **it must be regenerated after controlled files are updated** (see below).

## Standard finalization flow (write-lock convention)
```bash
guard/unlock.sh        # 1. Unlock (no LOCK conflict)
# 2. Edit controlled files
# 3. Update guard/MANIFEST.json (recompute sha256; use git diff as an aid)
git add -A && git commit -m "Describe this change"   # 4. Commit to leave traceable history
guard/lock.sh          # 5. Re-lock read-only
guard/verify.sh        # 6. Re-verify PASS
```

## Single-writer governance
- The toolkit directory **allows finalization only by the main agent + manual user edits**; other processes are read-only.
- If multiple processes edit concurrently, first acquire the lock with `touch guard/LOCK` and run `rm guard/LOCK` when done; unlock.sh will refuse to unlock when it sees LOCK, preventing mutual overwrites.
- Controlled files are already under **git version control** (`.git` in this directory). For any anomalous change you may use:
  - `git status` to detect changes immediately
  - `git log` for traceability of who changed what and when
  - `git restore <file>` to restore in one step
  - `git diff` to inspect the difference

## Rollback-Handling SOP
1. `guard/verify.sh` → FAIL to locate the altered file
2. `git log --oneline` + `git diff` to see what it was changed to
3. `git restore <file>` to restore to a known-good baseline
4. `guard/verify.sh` → PASS to confirm
5. Trace back to the source (see `guard/watch.sh` and the "Traceability" section) to prevent recurrence

## Traceability (investigating the rollback source)
- Check the precise modification time: `stat SKILL.md references/calibration_cases.json`
- Who has it open / is writing: `lsof +D .`
- Scheduled tasks: `crontab -l`; `ls /etc/cron*`
- Capture the writer in real time: `guard/watch.sh` (based on inotifywait; once hooked, any write to controlled files reports its PID)
