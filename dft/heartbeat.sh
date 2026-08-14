#!/usr/bin/env bash
# =============================================================================
# Chem-151 | S.T. Yau High School Science Award (Asia) 2026 | Palaash Gang
#
# heartbeat.sh -- append one status line to /opt/dft-jobs/heartbeat.log.
#
# Run from cron every 10 minutes. READ-ONLY: it starts nothing, stops nothing,
# and touches no job directory. Its only side effect is one appended line.
#
#   */10 * * * * /opt/dft-jobs/heartbeat.sh >/dev/null 2>&1
#
# Line format (fixed fields, greppable):
#   <ts> | complete C/T | incomplete I | orca N | disk XG free | ram YG free | queue ALIVE|GONE
# =============================================================================

set -uo pipefail

JOBROOT=/opt/dft-jobs
HB="$JOBROOT/heartbeat.log"

# cron gives a minimal PATH; tmux and pgrep must be findable.
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# shellcheck source=/dev/null
. "$JOBROOT/lib_jobstate.sh"

read -r n_complete n_incomplete n_total <<EOF
$(js_counts)
EOF

n_orca=$(js_orca_procs)
disk=$(df -h /opt | awk 'NR==2 {print $4}')
ram=$(free -g | awk '/^Mem:/ {print $7}')
queue=$(js_queue_alive && echo ALIVE || echo GONE)

printf '%s | complete %2s/%-2s | incomplete %2s | orca %s | disk %s free | ram %sG free | queue %s\n' \
    "$(date -u '+%Y-%m-%dT%H:%M:%SZ')" \
    "$n_complete" "$n_total" "$n_incomplete" "$n_orca" "$disk" "$ram" "$queue" \
    >> "$HB"
