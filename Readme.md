# 🦉 ow

ow - Nextcloud command-line client

## Introduction

ow (like, you're trying to say "owl" and almost succeed) is your handy local command-line pal for Nextcloud. Perform various operations to enhance local editing, collaboration, and more.

## Usage

### Help

List available actions.

```
$ ow --help
usage: ow [-h] [-d] {h,html-link,i,internal-link,l,lock,u,unlock} path

positional arguments:
  {h,html-link,i,internal-link,l,lock,u,unlock}
                        action to perform
  path                  local path to operate on

options:
  -h, --help            show this help message and exit
  -d, --debug           enable debug messages
```

Output is minimal on success. If an error occurs, messages are printed to standard error and a nonzero exit code is returned.

### Get HTML link

Given a local file path sync'd by the Nextcloud desktop client, return a snippet of HTML to link to the file.

```
$ ow html-link ~/Nextcloud/Documents/test.md
<a href="https://cloud.example.com/f/216">Documents/test.md</a>
```

On Ubuntu Desktop, you can feed the output to `wl-copy -t text/html` then paste the link into any rich text editor.

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

* install prerequisites
    * Python 3
    * Nextcloud desktop sync client
* download the `main.py` script, save it as `ow`
* edit values under `YOUR CONFIG`
* put the script in your path, for example: `~/bin/ow`
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
