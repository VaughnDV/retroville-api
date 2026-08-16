# History rewrite playbook

Use this only after a recoverable backup exists. The 2019 author names and
commit dates should be preserved because they are part of the showcase.

## 1. Backup

```bash
git clone --mirror git@github.com:VaughnDV/retroville-api.git retroville-api-backup.git
tar -czf retroville-api-backup-$(date +%Y%m%d).tar.gz retroville-api-backup.git
```

Keep the archive offline until the rewrite has been verified.

## 2. Filter the current clone

Install `git-filter-repo`, then from a fresh clone:

```bash
git filter-repo \
  --invert-paths \
  --path dump.rdb \
  --path .travis.yml \
  --replace-text ../replacements.txt
```

Example `replacements.txt`:

```
NEWSAPI_KEY_REDACTED==>NEWSAPI_KEY_REDACTED
REDACTED==>REDACTED
vaughndevilliers@gmail.com==>owner@example.com
erimfranci@gmail.com==>collaborator@example.com
```

Do not use `git rebase -i`. Do not force-push to `master` until the backup is
verified and the rewritten history has been reviewed.

## 3. Verify

```bash
git log --all -- dump.rdb
git grep -n -I -E 'NEWSAPI_KEY_REDACTED|#!Chai' $(git rev-list --all)
```

Both commands should return no matches.

## 4. Restore dates

`git-filter-repo` preserves author and committer dates by default. Confirm with:

```bash
git log --format='%H %ad %s' --date=iso
```
