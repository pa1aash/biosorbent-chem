#!/usr/bin/env bash
# Chem-151 — take a fresh Debian 12 / Ubuntu 22.04 x86-64 instance to a working ORCA install.
#
# Run ON the instance, as root or with sudo:
#     bash provision.sh
#
# This script does NOT download ORCA. ORCA is free for academic use but requires individual
# registration and may not be redistributed; the tarball is uploaded separately by
# upload_orca.sh. See ../../vendor/README_ORCA.md.

set -euo pipefail

CHEM151_USER="${CHEM151_USER:-chem151}"
ORCA_DIR="/opt/orca"
SCRATCH="/scratch"

echo "==> system packages"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq --no-install-recommends \
    build-essential gfortran \
    openmpi-bin libopenmpi-dev \
    python3 python3-pip python3-venv \
    rsync curl xz-utils bzip2 unzip \
    htop tmux jq bc

echo "==> OpenMPI version present"
mpirun --version | head -1
cat <<'NOTE'
    ORCA's parallel build is compiled against a SPECIFIC OpenMPI version, named in the tarball
    filename (e.g. ..._openmpi41.tar.xz). A mismatch is the single most common ORCA failure and
    it presents as an immediate MPI abort, not as a clear error. If the versions differ, either
    download the matching ORCA build or install the matching OpenMPI from source.
NOTE

echo "==> user and directories"
id -u "$CHEM151_USER" >/dev/null 2>&1 || useradd -m -s /bin/bash "$CHEM151_USER"
mkdir -p "$ORCA_DIR" "$SCRATCH" /home/"$CHEM151_USER"/{inputs,outputs}
chown -R "$CHEM151_USER":"$CHEM151_USER" "$ORCA_DIR" "$SCRATCH" /home/"$CHEM151_USER"

echo "==> scratch on the local disk"
# ORCA writes large integral and Hessian files. Keeping scratch off the OS partition avoids
# filling the root filesystem mid-job, which is how a 12-hour frequency run dies at hour 11.
df -h / "$SCRATCH" | sed 's/^/    /'

echo "==> environment"
cat > /etc/profile.d/orca.sh <<PROFILE
export ORCA_DIR="$ORCA_DIR"
export PATH="\$ORCA_DIR:\$PATH"
export LD_LIBRARY_PATH="\$ORCA_DIR:\${LD_LIBRARY_PATH:-}"
export ORCA_EXE="\$ORCA_DIR/orca"
export ORCA_SCRDIR="$SCRATCH"
# ORCA must be launched by ABSOLUTE PATH in parallel; the MPI wrapper re-executes it.
# A bare 'orca job.inp' silently runs serial.
export OMPI_ALLOW_RUN_AS_ROOT=1
export OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1
PROFILE
chmod 644 /etc/profile.d/orca.sh

echo "==> Python for post-processing"
python3 -m pip install --quiet --break-system-packages cclib numpy || \
    python3 -m pip install --quiet cclib numpy

echo
echo "PROVISIONED. Remaining manual step:"
echo "  from your laptop:  bash upload_orca.sh <instance-ip> ~/Downloads/orca_*_linux_x86-64_*.tar.xz"
