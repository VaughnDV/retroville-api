# History rewrite playbook

Applied locally on 2026-08-16. Author names and commit dates were preserved.
The local backup bundle was destroyed after the rewritten history was on GitHub.

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

Both should be empty on a fresh clone of the rewritten `master`. GitHub may
still serve pre-rewrite objects by SHA until Support runs garbage collection.
See GitHub's [removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository) guide.
