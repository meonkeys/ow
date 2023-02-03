#!/usr/bin/python3

# ow - Nextcloud command-line client
# Copyright (C) 2023  Adam Monsen
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import re
import requests
import sys
import xml.etree.cElementTree as cET

##########################################################################
# INTERNAL CONFIG - don't change these
##########################################################################

nextcloudWebdavFileRoot = 'remote.php/dav/files'

##########################################################################
# YOUR CONFIG - change these
##########################################################################

nextcloudServer = 'http://localhost:8080'

# where files are sync'd locally
localSyncFolder = '/home/user/Nextcloud'

# root of localSyncFolder on Nextcloud server
remoteDestinationFolder = '/'

nextcloudUsername = 'admin'

# if you use multi-factor auth, use an app password here
nextcloudPassword = 'admin'

##########################################################################
# MAIN CODE - probably leave this alone unless you wanna hack
##########################################################################

if len(sys.argv) != 3:
    print('Usage: {} i FILE'.format(sys.argv[0]), file=sys.stderr)
    sys.exit(1)

if sys.argv[1] != 'i':
    print('Sorry, I only know one trick so far. Care to teach me another?', file=sys.stderr)
    sys.exit(1)

if not os.path.exists(sys.argv[2]):
    print('path does not exist', file=sys.stderr)
    sys.exit(1)

realpath = os.path.realpath(sys.argv[2])

# remove localSyncFolder from realpath
relativePathOnly = re.sub(localSyncFolder, '', realpath)

# munge what's left into fileurl
fileurl = os.path.sep.join([nextcloudServer, nextcloudWebdavFileRoot, nextcloudUsername, relativePathOnly])

_propfindBody = '''<?xml version="1.0" encoding="UTF-8"?>
<d:propfind xmlns:d="DAV:">
  <d:prop xmlns:oc="http://owncloud.org/ns">
    <oc:fileid/>
  </d:prop>
</d:propfind>'''

try:
    response = requests.request('PROPFIND', fileurl, auth=(nextcloudUsername, nextcloudPassword), data=_propfindBody)
except requests.RequestException as e:
    print('PROPFIND request failed: {}'.format(e), file=sys.stderr)
    sys.exit(1)

# response status code must be between 200 and 400 to continue
if not response:
    print('HTTP response code {}. Response text: {}'.format(response.status_code, response.text), file=sys.stderr)
    sys.exit(1)

root = cET.fromstring(response.text)
fileId = root.findtext('.//{http://owncloud.org/ns}fileid')

if fileId is None:
    print('HTTP response code {}. Response text: {}'.format(response.status_code, response.text), file=sys.stderr)
    sys.exit(1)

print('{}/f/{}'.format(nextcloudServer, fileId))
