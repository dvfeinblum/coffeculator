#!/usr/bin/env bash

REL_FP=dump/$(date '+%Y-%m-%d/%H-%M')
mkdir -p $REL_FP
pg_dump -h localhost -d coffeeculator -U postgres -Fd -f $REL_FP
