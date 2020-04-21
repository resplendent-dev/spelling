#!/bin/bash

set -euxo pipefail

BASEDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TOP="$(dirname "${BASEDIR}")"

cd "${TOP}"
git checkout -- \
 app/spelling \
 app/tests \
 app/data \
 app/conftest.py \
 README.md \
 docs/index.rst
