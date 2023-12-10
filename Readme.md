# 🦉 ow

ow - Nextcloud command-line client

## Introduction

ow (like, you're trying to say "owl" and almost succeed) is your handy local command-line pal for Nextcloud. Perform various operations to enhance local editing, collaboration, and more.

Output is minimal on success. If an error occurs, messages are printed to standard error and a nonzero exit code is returned.

## Usage

### Help

List available actions.

```
$ ow --help
```

### Get HTML link

FIXME remove this feature

Given a local file path sync'd by the Nextcloud desktop client, return a snippet of HTML to link to the file.

```
$ ow html-link ~/Nextcloud/Documents/test.md
<a href="https://cloud.example.com/f/216">Documents/test.md</a>
```

On Ubuntu Desktop, you can feed the output to `wl-copy -t text/html` then paste the link into any rich text editor.

### Create album from folder

FIXME: change command to `aff`, `album-from-folder`
FIXME: move install instructions down
FIXME: mention python3-requests package

Install the requirements listed in `requirements.txt`, e.g. via `pip3 install -r requirements.txt`. For debugging, install `pip3 install -r requirements-dev.txt` instead.

FIXME: remove the need for `convert-all.sh`

Create `todo-photo-folders.txt`. This is a list of paths in a Nextcloud instance you want converted to albums, one per line. `Photos/2020/Camping trip`, `Photos/2021/sunny day`, etc.

FIXME: use `configparser` instead of python-dotenv

Copy the `template.env` file and name the copy `.env`. Change the variables in the new `.env` file accordingly.
Run `./convert-all.sh`.

It expects that the folders listed contain media compatible with the Photos and Memories apps (generally just photos and videos). Sub-folders and non-compatible file types are ignored.

### Get internal link

Given a local file path sync'd by the Nextcloud desktop client, return the "internal link" on the Nextcloud server.

```
$ ow internal-link ~/Nextcloud/test.md
https://cloud.example.com/f/229
```

### Lock

Lock a file. Requires the [Temporary files lock app](https://apps.nextcloud.com/apps/files_lock).

```
$ ow lock ~/Nextcloud/test.md
```

Locking indicates to other users your wish to avoid conflicts in shared files.

### Unock

Unlock a file. Requires the [Temporary files lock app](https://apps.nextcloud.com/apps/files_lock).

```
$ ow unlock ~/Nextcloud/test.md
```

## Installation

* clone this repository, or just grab the `ow` script
* install required dependencies
    * Python 3
    * Python `requests` library (via e.g. `pip install requests` or `apt install python3-requests`)
* install optional dependencies
    * Nextcloud desktop sync client (for lock, unlock, internal-url; not needed for diralbum)
    * `xmllint` at `/usr/bin/xmllint` (for debugging API responses)
        * on Debian/Ubuntu: `apt install libxml2-utils`
* edit values under `YOUR CONFIG` ← FIXME
* put the script in your path
    * example: `cd ~/.local/bin && ln -s ~/git/meonkeys/ow/ow`
* make sure it is executable
* for auto-completion in Bash, source `bash_completion`

## Architecture

ow talks with the [Nextcloud WebDAV API](https://docs.nextcloud.com/server/latest/developer_manual/client_apis/WebDAV/basic.html).

## History

ow [started](https://help.nextcloud.com/t/get-internal-link-for-a-file-in-nextcloud-from-a-local-command-line/152774) with one command (get internal link for locally sync'd file). Hopefully by the time you are reading this it has learned more tricks. If I and others use this, like it, and want to do more with it, here are some ideas on what we might do:

## Ideas

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
    * use a real argument parser (DONE)
    * add tests
* improve cross-platform compatibility
    * currently only built for and tested on recent Ubuntu LTS
    * add Windows support
    * add macOS support
* pick a better name
* use a real contributor agreement
* Are there other/better free software utilities like this one? List/promote them.
* Would it make more sense to implement this and the other feature ideas (above) within the [official client](https://docs.nextcloud.com/desktop/latest/advancedusage.html)?
    * [Do the maintainers want these features?](https://github.com/nextcloud/desktop/issues?q=label%3A%22feature%3A+%3Awhite_square_button%3A+nextcloudcmd%22+)
* improve Bash programmable completion
    * handle spaces gracefully, like `ls` <kbd>Tab</kbd> or `vim` <kbd>Tab</kbd>
    * get completions from the python script itself so we [DRY](https://en.wikipedia.org/wiki/Don't_repeat_yourself)
    * see also: [this](https://stackoverflow.com/questions/14597466/custom-tab-completion-in-python-argparse), [this](https://stackoverflow.com/questions/9568611/how-does-argparse-and-the-deprecated-optparse-respond-to-tab-keypress-after), and [this](https://spin.atomicobject.com/2016/02/14/bash-programmable-completion/)

## COPYLEFT AND LICENSE

* Copyright ©2023 Adam Monsen <haircut@gmail.com>
* License: AGPL v3 or later (see COPYING)
