# 🦉 ow

ow - Rudimentary Nextcloud command-line client

## Usage

### Get internal link

Given a local file path sync'd by the Nextcloud desktop client, return the Internal link on the Nextcloud server.

```
$ ow pl ~/Nextcloud/test.md
https://cloud.example.com/f/229
```

## Installation

NOTE: only works on Linux so far

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

ow [started](https://help.nextcloud.com/t/get-internal-link-for-a-file-in-nextcloud-from-a-local-command-line/152774) with one command: `pl`. Hopefully by the time you are reading this it has learned more tricks. It began as a small, working proof of concept to see if I and others use this, like it, and want to do more with it. If we choose to continue working on it, here are some ideas on what we might do:

## Other ideas

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

## COPYLEFT AND LICENSE

* Copyright ©2023 Adam Monsen <haircut@gmail.com>
* License: AGPL v3 or later (see COPYING)
