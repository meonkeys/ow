# 🦉 ow

## Name

ow - Nextcloud command-line client

## Synopsis

```
ow action target
```

## Description

ow (like, you're trying to say "owl" and almost succeed) is your handy local command-line pal for Nextcloud. ow enhances local editing, collaboration, and more by providing missing features or by providing a command-line interface for existing features.

Output is generally minimal on success. If an error occurs, messages are printed to standard error and a nonzero exit code is returned.

### Quick examples

```bash
# Add all media in a folder to an album.
ow dir-album "Photos/2020/Camping trip"

# Get internal link for a file.
ow internal-link ~/Nextcloud/Readme.md

# Find and delete old calendar events.
ow delete-old-events 'calendar=personal,minimumAge=2y'

# Lock a file.
ow lock ~/Nextcloud/Readme.md

# Unlock a file.
ow unlock ~/Nextcloud/Readme.md
```

## Install

* clone this repository
    * or just download the `ow` script
    * put `ow` in your `$PATH` and make it executable, e.g. `ln -s ~/git/meonkeys/ow/ow ~/.local/bin`
* install required dependencies
    * Python 3
    * Python `requests` library (via e.g. `pip install requests` or `apt install python3-requests`)
* install optional dependencies
    * Nextcloud desktop sync client (for lock, unlock, internal-url; not needed for dir-album)
    * `xmllint` at `/usr/bin/xmllint` (for debugging API responses)
        * on Debian/Ubuntu: `apt install libxml2-utils`
    * `python3-argcomplete` for Bash programmable (Tab) completion
        * must also set this up with, e.g. `eval "$(register-python-argcomplete3 ow)"` in your `~/.bashrc`
    * [Temporary files lock app](https://apps.nextcloud.com/apps/files_lock) for locking and unlocking files.
* create config file based on "example config" below

### example config

Create `~/.config/ow/ow.ini` and customize, following the example below:

```ini
[server]
# Must start with https
baseUrl = https://cloud.example.com
username = user
# If you use multi-factor auth, use an app password here.
password = redacted

[local]
# If you use the Nextcloud Desktop client, set this to indicate where files are sync'd.
# Required for lock, unlock, and internal-url.
# Not needed for dir-album nor delete-old-events.
syncFolder = /home/user/Nextcloud
```

## Detailed usage

### Help

List available actions.

```bash
ow --help
```

### Create album from folder

Add all media in a folder to an album.

```bash
ow dir-album "Photos/2020/Camping trip"
```

This works directly against the Nextcloud WebDAV API; the desktop client is not required.

This command expects that the provided path contains media compatible with the Photos and Memories apps (generally just photos and videos). Sub-folders and non-compatible file types are ignored.

The new album will be named by transforming the last path element. Some arbitary cleanup steps are performed. Examples:

| Path                           | Album             |
|--------------------------------|-------------------|
| Photos/2020/Camping trip/      | Camping trip      |
| Photos/2020-Camping trip       | 2020-Camping trip |
| Photos/2020-04-01 Camping trip | Camping trip      |

#### convert many folders to albums

Example Python script for converting a bunch of folders to albums at once:

```python
import subprocess

folders = [
    'Photos/2020/Camping trip',
    'Photos/2021/sunny day'
]

for folder in folders:
    subprocess.run(['./ow', 'dir-album', folder])
```

### Get internal link

Given a local file path sync'd by the Nextcloud desktop client, return the "internal link" on the Nextcloud server.

```bash
ow internal-link ~/Nextcloud/test.md
# example output:
# https://cloud.example.com/f/229
```

### Delete old calendar events

Find and delete old calendar events given an event filter specification.

This will delete events older than 2 years on a calendar called "personal":

```bash
ow delete-old-events 'calendar=personal,minimumAge=2y'
```

### Lock

Lock a file.

```bash
ow lock ~/Nextcloud/Readme.md
```

Locking indicates to other users your wish to avoid conflicts in shared files.

### Unock

Unlock a file.

```bash
ow unlock ~/Nextcloud/Readme.md
```

## Contributions

Patches welcome. Ask before submitting anything larger than an obvious bugfix. Create a GitHub pull request. Add your name below.

### Contributors

* Adam Monsen
* Frederik Berg
* Tom Laermans

## Architecture

ow is written in Python. It examines local files sync'd by the [Nextcloud desktop client](https://github.com/nextcloud/desktop/) for some operations, and talks with the [Nextcloud WebDAV API](https://docs.nextcloud.com/server/latest/developer_manual/client_apis/WebDAV/basic.html) for others.

## History

ow [started](https://help.nextcloud.com/t/get-internal-link-for-a-file-in-nextcloud-from-a-local-command-line/152774) with one command (get internal link for locally sync'd file).

## Ideas

* testing
    * add unit tests (very fast and specific, code-level)
    * add integration tests (slower, maybe only run on merges)
    * add end-to-end/acceptance tests (many things under test, complex, brittle, possibly manual)
    * security, penetration, fuzzing, etc.
    * use continuous integration
    * document manual acceptance tests, perform regularly, record results
    * document test matrix ("tested with" table showing all combinations of client OS, client version, server version, etc. that are tested / known / expected to work)
* add more features
    * post chat messages
    * add a task
    * add a calendar event
    * search
* improve setup
    * automate install
* improve config
    * read and use config from Nextcloud desktop client
    * [read and use secrets from desktop/OS password manager](https://pypi.org/project/keyring/) or smartcard
* improve code maintainability
    * add tests (see "testing")
* improve cross-platform compatibility
    * currently only built for and tested on recent Ubuntu LTS
    * add Windows support
    * add macOS support
* pick a better name?
* consider [cla or not](https://sfconservancy.org/blog/2014/jun/09/do-not-need-cla/), [copyright ownership](https://sfconservancy.org/blog/2021/jun/30/who-should-own-foss-copyrights/)
* Are there other/better free software utilities like this one? List/promote them.
* Would it make more sense to implement this and the other feature ideas (above) within the [official client](https://docs.nextcloud.com/desktop/latest/advancedusage.html)?
    * [Do the maintainers want these features?](https://github.com/nextcloud/desktop/issues?q=label%3A%22feature%3A+%3Awhite_square_button%3A+nextcloudcmd%22+)
* use [Nextcloud Python Framework](https://github.com/cloud-py-api/nc_py_api) instead of WebDAV API?

## COPYLEFT AND LICENSE

* Copyright ©2023-2024 Adam Monsen <haircut@gmail.com>
* License: AGPL v3 or later (see COPYING)
