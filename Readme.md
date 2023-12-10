# 🦉 ow

ow - Nextcloud command-line client

## WIP diralbum branch

This is a throwaway or work-in-progress branch with code to convert Nextcloud folders to albums.

### USAGE

1. Install the requirements listed in `requirements.txt`, e.g. via `pip3 install -r requirements.txt`. For debugging, install `pip3 install -r requirements-dev.txt` instead.
1. Create `todo-photo-folders.txt`. This is a list of paths in a Nextcloud instance you want converted to albums, one per line. `Photos/2020/Camping trip`, `Photos/2021/sunny day`, etc.
1. Copy the `template.env` file and name the copy `.env`. Change the variables in the new `.env` file accordingly.
1. Run `./convert-all.sh`.

It expects that the folders listed contain media compatible with the Photos and Memories apps (generally just photos and videos). Sub-folders and non-compatible file types are ignored.

## COPYLEFT AND LICENSE

* Copyright ©2023 Adam Monsen <haircut@gmail.com>
* License: AGPL v3 or later (see COPYING)
