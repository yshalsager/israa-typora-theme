#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
  printf 'Usage: %s input.md [output.pdf]\n' "$0" >&2
  exit 2
fi

script_dir="$(cd "$(dirname "$0")" && pwd)"
input="$1"
output="${2:-${input%.*}.pdf}"

if [[ "$input" != /* ]]; then
  input="$(pwd)/$input"
fi

if [[ "$output" != /* ]]; then
  output="$(pwd)/$output"
fi

cd "$script_dir"
pandoc "$input" --defaults israa-defaults.yaml -o "$output"
