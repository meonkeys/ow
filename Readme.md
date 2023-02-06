# 🦉 ow

ow - Nextcloud command-line client

## Usage

### Help

List available actions.

```
$ ow --help
usage: ow [-h] [-d] {i,internal-link,l,lock,u,unlock} path

positional arguments:
  {i,internal-link,l,lock,u,unlock}
                        action to perform
  path                  local path to operate on

options:
  -h, --help            show this help message and exit
  -d, --debug           enable debug messages
```

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
    * use a real argument parser
    * add tests
* improve cross-platform compatibility
    * add Windows support
    * add macOS support
* pick a better name
* use a real contributor agreement
* Are there other/better free software utilities like this one? List/promote them.
* Would it make more sense to implement this and the other feature ideas (above) within the [official client](https://docs.nextcloud.com/desktop/latest/advancedusage.html)? Do the maintainers want these features?
* support Windows, Linux, macos
    * test on platforms other than Linux
    * add documentation for platforms other than Linux

## COPYLEFT AND LICENSE

* Copyright ©2023 Adam Monsen <haircut@gmail.com>
* License: AGPL v3 or later (see COPYING)
