#!/usr/bin/python3

# ow - Nextcloud command-line client - main code
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

import argparse
import os
import re
import requests
import sys
import xml.etree.cElementTree as cET
from dotenv import load_dotenv

##########################################################################
# INTERNAL CONFIG
##########################################################################

nextcloudWebdavRoot = 'remote.php/dav'

##########################################################################
# LOAD EXTERNAL CONFIG FROM .env FILE
##########################################################################

load_dotenv()
nextcloudServer = os.getenv('nextcloudServer')
nextcloudUsername = os.getenv('nextcloudUsername')
nextcloudPassword = os.getenv('nextcloudPassword')

##########################################################################
# MAIN CODE - probably leave this alone unless you wanna hack
##########################################################################

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--debug', help='enable debug messages', action='store_true')
parser.add_argument('action', help='action to perform', choices=['da','dir-album'])
parser.add_argument('target', help='path or name or something')
args = parser.parse_args()

# Check for debug mode and import additional libraries if needed
if args.debug:
    try:
        import tempfile
        import subprocess
        import urllib
    except ImportError:
        print('⛔ You need to install additional libraries for debugging via '
              'pip install -r requirements-dev.txt',
              file=sys.stderr)
        sys.exit(1)


def debug(msg):
    if args.debug:
        print(msg, file=sys.stderr)

debug(f'👟 action is {args.action}')

_auth = (nextcloudUsername, nextcloudPassword)

def getFilesUrl(path):
    global nextcloudServer, nextcloudWebdavRoot, nextcloudUsername

    _filesUrl = '/'.join([nextcloudServer, nextcloudWebdavRoot, 'files', nextcloudUsername, path])
    debug(f'💻 WebDAV files URL is {_filesUrl}')
    return _filesUrl

def getAlbumUrl(albumName):
    global nextcloudServer, nextcloudWebdavRoot, nextcloudUsername
    safeAlbumName = urllib.parse.quote(albumName)
    _albumUrl = '/'.join([nextcloudServer, nextcloudWebdavRoot, 'photos', nextcloudUsername, 'albums', safeAlbumName])
    debug(f'💻 WebDAV album URL is {_albumUrl}')
    return _albumUrl

def captureXmlResponse(text):
    f = tempfile.NamedTemporaryFile(mode='w', prefix='diralbum_', delete=False)
    f.write(text)
    f.close()
    prettyOutputFilename = f.name + '.xml'
    subprocess.run(['/usr/bin/xmllint', '--format', '--output', prettyOutputFilename, f.name])
    return prettyOutputFilename

def isCollectionOrExit(filesUrl):
    global _auth, args
    debug('🏃 fetching internal file ID...')

    _propfindBody = '''<?xml version="1.0" encoding="UTF-8"?>
    <d:propfind xmlns:d="DAV:" xmlns:oc="http://owncloud.org/ns">
      <d:prop>
        <oc:fileid />
        <d:getcontenttype />
        <d:resourcetype />
      </d:prop>
    </d:propfind>'''

    headers = {'Depth': '0'}
    try:
        response = requests.request('PROPFIND', filesUrl, auth=_auth, data=_propfindBody, headers=headers)
    except requests.RequestException as e:
        print('⛔ PROPFIND request failed: {}'.format(e), file=sys.stderr)
        sys.exit(1)

    # response status code must be between 200 and 400 to continue
    # use overloaded __bool__() to check this
    if not response:
        print(f'⛔ HTTP response code {response.status_code}. Response text: {response.text}', file=sys.stderr)
        sys.exit(1)

    if args.debug:
        prettyOutputFilename = captureXmlResponse(response.text)
        debug(f'📝 HTTP response code {response.status_code}. Response text saved in: {prettyOutputFilename}')

    root = cET.fromstring(response.text)
    dirobjs = root.findall('.//{DAV:}resourcetype/{DAV:}collection')

    if len(dirobjs) != 1:
        print('⛔ path is not a directory. HTTP response code {}. Response text: {}'.format(response.status_code, response.text), file=sys.stderr)
        sys.exit(1)

def getMedia(filesUrl):
    global _auth, args
    debug('🏃 finding media in given folder...')

    _propfindBody = '''<?xml version="1.0" encoding="UTF-8"?>
    <d:propfind xmlns:d="DAV:" xmlns:oc="http://owncloud.org/ns">
      <d:prop>
        <oc:fileid />
        <d:getcontenttype />
        <d:resourcetype />
      </d:prop>
    </d:propfind>'''

    try:
        response = requests.request('PROPFIND', filesUrl, auth=_auth, data=_propfindBody)
    except requests.RequestException as e:
        print('⛔ PROPFIND request failed: {}'.format(e), file=sys.stderr)
        sys.exit(1)

    # response status code must be between 200 and 400 to continue
    # use overloaded __bool__() to check this
    if not response:
        print(f'⛔ HTTP response code {response.status_code}. Response text: {response.text}', file=sys.stderr)
        sys.exit(1)

    if args.debug:
        prettyOutputFilename = captureXmlResponse(response.text)
        debug(f'📝 HTTP response code {response.status_code}. Response text saved in: {prettyOutputFilename}')

    media = []
    root = cET.fromstring(response.text)
    for r in root.findall('.//{DAV:}response'):
        contentType = r.find('.//{DAV:}getcontenttype').text
        if contentType:
            if contentType.startswith('image') or contentType.startswith('video'):
                # the "d:href" element has a path, like "/remote.php/dav/files/adam/tmp/2023-08-07%20test/test2.png"
                media.append(nextcloudServer + r.find('.//{DAV:}href').text)

    return media

def createAlbum(albumName):
    global _auth
    debug('🏃 creating album...')

    albumUrl = getAlbumUrl(albumName)

    try:
        response = requests.request('MKCOL', albumUrl, auth=_auth)
    except requests.RequestException as e:
        print('⛔ MKCOL request failed: {}'.format(e), file=sys.stderr)
        sys.exit(1)

    # response status code must be between 200 and 400 to continue
    # use overloaded __bool__() to check this
    if not response:
        print(f'⛔ HTTP response code {response.status_code}. Response text: {response.text}', file=sys.stderr)
        sys.exit(1)

    debug(f'📝 HTTP response code {response.status_code}. Response text: {response.text}')

    return albumUrl

def populateAlbum(cleanedAlbumName, albumUrl, mediaUrls):
    global _auth, args
    debug('🏃 populating new album...')

    for mediaUrl in mediaUrls:
        mediaFilename = os.path.basename(mediaUrl)
        debug(f'📰 adding {mediaFilename} to {cleanedAlbumName}')
        headers = {'Destination': '/'.join([albumUrl, mediaFilename])}
        try:
            response = requests.request('COPY', mediaUrl, auth=_auth, headers=headers)
        except requests.RequestException as e:
            print('⛔ COPY request failed: {}'.format(e), file=sys.stderr)
            sys.exit(1)

        # response status code must be between 200 and 400 to continue
        # use overloaded __bool__() to check this
        if not response:
            print(f'⛔ HTTP response code {response.status_code}. Response text: {response.text}', file=sys.stderr)
            sys.exit(1)

def cleanAlbumName(rawAlbumName):
    debug(f'💻 raw album name is {rawAlbumName}')
    noTrailingSlash = re.sub(r'/$', '', rawAlbumName)
    debug(f'💻 without trailing slash: {noTrailingSlash}')
    based = os.path.basename(noTrailingSlash)
    debug(f'💻 basenamed: {based}')
    clean = re.sub(r'^\d{4}-\d{2}-\d{2}\s+', '', based)
    debug(f'💻 cleaned album name is {clean}')
    if not clean:
        print(f'⛔ invalid album name: {clean}', file=sys.stderr)
        sys.exit(1)
    return clean

if args.action in ['da','dir-album']:
    debug('🏃 making album from directory...')
    ncRelativeAlbumPath = args.target
    folderWithPhotosUrl = getFilesUrl(ncRelativeAlbumPath)

    # Confirm we got a path to a collection (folder). If not, this call will
    # exit early. Still might not be a valid photo album, though.
    isCollectionOrExit(folderWithPhotosUrl)

    cleanedAlbumName = cleanAlbumName(ncRelativeAlbumPath)

    debug(f'📁 album name will be: {cleanedAlbumName}...')
    albumUrl = createAlbum(cleanedAlbumName)

    debug(f'📁 walking collection: {ncRelativeAlbumPath}...')
    mediaUrls = getMedia(folderWithPhotosUrl)

    populateAlbum(cleanedAlbumName, albumUrl, mediaUrls)

    debug('🔓 success!')
