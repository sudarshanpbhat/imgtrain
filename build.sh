#!/bin/bash

pyinstaller \
  ./scripts/imgtrain.py \
  --onefile \
  --distpath ./bin/ \
  --specpath ./bin/ 