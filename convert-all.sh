#!/bin/bash

set -o errexit
set -o nounset
set -o pipefail

todo=todo-photo-folders.txt
done=done-photo-folders.txt

IFS='
'

for folder in $(cat "$todo"); do
    echo "... $folder ..."
    ./diralbum.py dir-album "$folder"
    sleep 2
done

cat "$todo" >> "$done"

truncate --size=0 "$todo"
