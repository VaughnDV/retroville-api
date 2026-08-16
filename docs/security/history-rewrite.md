# History rewrite playbook

Applied locally on 2026-08-16. Author names and commit dates were preserved.

## Backup

```bash
git bundle create /Users/vaughn/Projects/retroville-api-backup-20260816.bundle --all
```

Restore if needed:

```bash
git clone /Users/vaughn/Projects/retroville-api-backup-20260816.bundle restored-retroville-api
```

## What was rewritten

```bash
git filter-repo --force \
  --invert-paths \
  --path dump.rdb \
  --path .travis.yml \
  --replace-text replacements.txt
```

`replacements.txt` mapped the leaked News API key and mailbox password to
placeholders. It did not rewrite personal email addresses.

## Verify

```bash
git log --all -- dump.rdb
git log --all -- .travis.yml
```

Both should be empty. GitHub will keep the old objects until the rewritten
branches are force-pushed.
