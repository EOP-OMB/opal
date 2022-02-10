#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyclamd
import sys
import datetime
import os

from nose.tools import assert_equals
from nose.tools import raises
from nose import with_setup

from multiprocessing import Value

"""
test_pyclamd.py - tests cases for pyclamd

Source code : https://bitbucket.org/xael/pyclamd

Author :

* Alexandre Norman - norman at xael.org


Licence : GPL v3 or any later version


This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""

##########################################################################################

"""
This plugin provides ``--pdb`` and ``--pdb-failures`` options. The ``--pdb``
option will drop the test runner into pdb when it encounters an error. To
drop into pdb on failure, use ``--pdb-failures``.
"""

import pdb
from nose.plugins.base import Plugin

class Pdb(Plugin):
    """
    Provides --pdb and --pdb-failures options that cause the test runner to
    drop into pdb if it encounters an error or failure, respectively.
    """
    enabled_for_errors = False
    enabled_for_failures = False
    score = 5 # run last, among builtins

    def options(self, parser, env):
        """Register commandline options.
        """
        parser.add_option(
            "--pdb", action="store_true", dest="debugBoth",
            default=env.get('NOSE_PDB', False),
            help="Drop into debugger on failures or errors")
        parser.add_option(
            "--pdb-failures", action="store_true",
            dest="debugFailures",
            default=env.get('NOSE_PDB_FAILURES', False),
            help="Drop into debugger on failures")
        parser.add_option(
            "--pdb-errors", action="store_true",
            dest="debugErrors",
            default=env.get('NOSE_PDB_ERRORS', False),
            help="Drop into debugger on errors")

    def configure(self, options, conf):
        """Configure which kinds of exceptions trigger plugin.
        """
        self.conf = conf
        self.enabled_for_errors = options.debugErrors or options.debugBoth
        self.enabled_for_failures = options.debugFailures or options.debugBoth
        self.enabled = self.enabled_for_failures or self.enabled_for_errors

    def addError(self, test, err):
        """Enter pdb if configured to debug errors.
        """
        if not self.enabled_for_errors:
            return
        self.debug(err)

    def addFailure(self, test, err):
        """Enter pdb if configured to debug failures.
        """
        if not self.enabled_for_failures:
            return
        self.debug(err)

    def debug(self, err):
        import sys # FIXME why is this import here?
        ec, ev, tb = err
        stdout = sys.stdout
        sys.stdout = sys.__stdout__
        try:
            pdb.post_mortem(tb)
        finally:
            sys.stdout = stdout

##########################################################################################

def setup_module():
    global cd
    cd = pyclamd.ClamdAgnostic()
    return

def teardown_module():
    os.remove('/tmp/EICAR')
    os.remove('/tmp/NO_EICAR')
    os.remove('/tmp/EICAR-éèô请收藏我们的网址')
    return

def test_ping():
    """
    Tests pinging clamd
    """
    assert(cd.ping())


def test_version():
    """
    Tests version
    """
    assert_equals(cd.version().split()[0], 'ClamAV')

def test_reloading_base():
    """
    Reloads clamd database
    """
    assert_equals(cd.reload(), 'RELOADING')


def test_stats():
    """
    Checks stats
    """
    assert_equals(cd.stats().split()[0], 'POOLS:')


def test_eicar():
    """
    Tests eicar infected file
    """
    void = open('/tmp/EICAR','wb').write(cd.EICAR())
    assert_equals(cd.scan_file('/tmp/EICAR')['/tmp/EICAR'], ('FOUND', 'Eicar-Test-Signature'))

def test_no_eicar():
    """
    Tests standard non infected file
    """
    void = open('/tmp/NO_EICAR','w').write('no virus in this file')
    assert(cd.scan_file('/tmp/NO_EICAR') is None)

def test_stream():
    """
    Tests eicar infected stream
    """
    assert_equals(cd.scan_stream(cd.EICAR())['stream'], ('FOUND', 'Eicar-Test-Signature'))


def test_directory_scanning():
    """
    Tests directory scanning with eicar infected file
    """
    directory = cd.contscan_file('/tmp/')
    assert_equals(directory['/tmp/EICAR'], ('FOUND', 'Eicar-Test-Signature'))

def test_multiscan_file():
    """
    Tests multiscan file scanning with eicar infected file
    """
    directory = cd.multiscan_file('/tmp/')
    assert_equals(directory['/tmp/EICAR'], ('FOUND', 'Eicar-Test-Signature'))


def test_unicode_scanning():
    """
    Tests encoding with non latin characters
    (Chinese ideograms taken from random site, don't know what it mean, sorry)
    """
    void = open('/tmp/EICAR-éèô请收藏我们的网址','wb').write(cd.EICAR())
    r = cd.scan_file('/tmp/EICAR-éèô请收藏我们的网址')
    assert_equals(list(r.keys())[0], '/tmp/EICAR-éèô请收藏我们的网址')
    assert_equals(r['/tmp/EICAR-éèô请收藏我们的网址'], ('FOUND', 'Eicar-Test-Signature'))



def test_scan_stream_unicode_test_eicar_in_pdf():
    """
    Tests stream scan with eicar in pdf file. Not detected by design of ClamAv.
    """
    file_data = open('./probleme_data.pdf', 'rb').read()
    v = cd.scan_stream(file_data)
    assert_equals(v, None)


def test_scan_stream_unicode_test_clean():
    """
    Tests stream scan with clean pdf file
    """
    file_data = open('./probleme_data_clean.pdf', 'rb').read()
    v = cd.scan_stream(file_data)
    assert_equals(v, None)
    return


def test_scan_stream_filelike_eicar():
    void = open('/tmp/EICAR','wb').write(cd.EICAR())
    f = open('/tmp/EICAR', 'rb')
    v = cd.scan_stream(f)
    assert_equals(v, {'stream': ('FOUND', 'Eicar-Test-Signature')})


def test_scan_stream_filelike_clean():
    void = open('/tmp/NO_EICAR','w').write('no virus in this file')
    f = open('/tmp/NO_EICAR', 'rb')
    v = cd.scan_stream(f)
    assert_equals(v, None)


def test_scan_file_unicode_test_eicar_in_pdf():
    """
    Tests stream scan with clean pdf file
    """
    v = cd.scan_file('/home/xael/ESPACE_KM/python/pyclamd/probleme_data.pdf')
    #.assertEqual(v, {u'stream': ('FOUND', 'Eicar-Test-Signature')})
    assert_equals(v, None)
    return


##########################################################################################
