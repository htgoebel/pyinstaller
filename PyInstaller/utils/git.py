#-----------------------------------------------------------------------------
# Copyright (c) 2005-2016, PyInstaller Development Team.
#
# Distributed under the terms of the GNU General Public License with exception
# for distributing bootloader.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------


"""
This module contains various helper functions for git DVCS
"""

from __future__ import print_function

import os
from ..compat import exec_command, exec_command_rc, FileNotFoundError

try:
    WindowsError
except NameError:
    # No running on Windows
    WindowsError = FileNotFoundError

def get_repo_revision():
    path = os.path # shortcut
    gitdir = path.normpath(path.join(path.dirname(os.path.abspath(__file__)), '..', '..', '.git'))
    cwd = os.path.dirname(gitdir)
    if not path.exists(gitdir):
        try:
            from ._gitrevision import rev
            if not rev.startswith('$'):
                # the format specifier has been substituted
                return '+' + rev
        except ImportError:
            pass
        return ''
    try:
        # need to update index first to get reliable state
        exec_command_rc('git', 'update-index', '-q', '--refresh', cwd=cwd)
        recent = exec_command('git', 'describe', '--long', '--dirty', '--tag',
                              cwd=cwd).strip()
        import sys
        print(repr(recent), file=sys.stderr)
        tag, changes, rev = recent.rsplit('-', 2)
        import sys
        print(repr((changes, rev)), file=sys.stderr)
        if changes == '0':
            return ''
        if rev == 'dirty':
            rev = changes + '.mod'
        # According to pep440 local version identifier starts with '+'.
        return '+' + rev
    except (FileNotFoundError, WindowsError):
        # Be silent when git command is not found.
        pass
    return ''


if __name__ == '__main__':
    print(get_repo_revision())
