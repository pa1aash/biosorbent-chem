#!/usr/bin/env bash
# Upload and unpack an ORCA tarball onto a provisioned instance.
#     bash upload_orca.sh <host> <path/to/orca_*_linux_x86-64_*.tar.xz>
#
# ORCA is NOT redistributed by this repository. Register at https://orcaforum.kofo.mpg.de/
# and download it yourself. See ../../vendor/README_ORCA.md.
set -euo pipefail

HOST="${1:?usage: upload_orca.sh <host> <tarball>}"
TARBALL="${2:?usage: upload_orca.sh <host> <tarball>}"
[ -f "$TARBALL" ] || { echo "no such file: $TARBALL" >&2; exit 1; }

case "$(basename "$TARBALL")" in
    *linux_x86-64*) ;;
    *) echo "WARNING: '$(basename "$TARBALL")' does not look like a Linux x86-64 build." >&2
       echo "         Hetzner instances are x86-64 Linux. A macOS or ARM build will not run." >&2
       read -r -p "         Continue anyway? [y/N] " a; [ "$a" = y ] || exit 1 ;;
esac

echo "==> uploading $(du -h "$TARBALL" | cut -f1)"
rsync -P "$TARBALL" "root@$HOST:/tmp/orca.tar.xz"

echo "==> unpacking into /opt/orca"
ssh "root@$HOST" bash -s <<'REMOTE'
set -euo pipefail
mkdir -p /opt/orca
tar -xf /tmp/orca.tar.xz -C /opt/orca --strip-components=1
rm -f /tmp/orca.tar.xz
chmod +x /opt/orca/orca* 2>/dev/null || true
chown -R chem151:chem151 /opt/orca 2>/dev/null || true
echo "installed version:"
/opt/orca/orca 2>&1 | grep -iE 'program version|Version' | head -2 || echo "  (run a job to confirm)"
REMOTE

echo
echo "Record the exact version. It is a required field of report Table 3.1 (attack A01)."
