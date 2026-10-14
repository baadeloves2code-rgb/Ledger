# Day 1: Linux essentials

## Done
- Launched lab2 (4 CPU / 8 GB / 40 GB, arm64); IP 192.168.252.3/24, gateway 192.168.252.1.
- LED-0: SSH key, repo cloned, skeleton and starter app committed; app ran under gunicorn on 127.0.0.1:5000.
- LED-1: ledger user, ledger-ops group, /srv, /var/lib, /var/log (2770 setgid) and /etc paths; installed nginx and sqlite3.
- Block B: disk-full drill, auditor access request, LFCS shared directory (3770).

## What broke and how I fixed it
- Cloned inside an existing folder, so the repo was nested; moved it up a level.
- Typed a heredoc on one line; EOF must be alone on its own line.
- Shared directory at 1733 used "others" bits and hid the files; fixed with root:team and 3770.

## What I'd do differently
- Run df -h first on a disk alert, and write down owner, purpose and action for each file.
- Remember: setgid sets the group, umask sets the permissions.
- Check pwd before running git commands.
