#!/bin/bash

set -euxo pipefail

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Validate working from pypi
python3 -m pip install nox
nox

# Validate regular CI
"${BASEDIR}/ci.sh"

