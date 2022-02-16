"""Configures spam filters and the virus scanner"""
# SPDX-License-Identifier: AGPL-3.0-or-later

import pathlib
import re
import subprocess

from plinth import actions
from plinth.modules.email import postconf

_milter_config = {
    'smtpd_milters': 'inet:127.0.0.1:11332',
    'non_smtpd_milters': 'inet:127.0.0.1:11332',
}


def repair():
    actions.superuser_run('email', ['spam', 'set_filter'])


def action_set_filter():
    _compile_sieve()
    _setup_rspamd()
    postconf.set_many(_milter_config)


def _compile_sieve():
    """Compile all .sieve script to binary format for performance."""
    sieve_dir = '/etc/dovecot/freedombox-sieve-after/'
    subprocess.run(['sievec', sieve_dir], check=True)


def _setup_rspamd():
    """Adjust configuration to include FreedomBox configuration files."""
    configs = [('milter_headers.conf', 'freedombox-milter-headers.conf'),
               ('redis.conf', 'freedombox-redis.conf')]
    base_path = pathlib.Path('/etc/rspamd/local.d')
    for orig_path, include_path in configs:
        _setup_local_include(base_path / orig_path, base_path / include_path)


def _setup_local_include(orig_path, include_path):
    """Adjust configuration to include a FreedomBox configuration file."""
    lines = []
    if orig_path.exists():
        lines = orig_path.read_text().splitlines()

    file_name = include_path.name
    for line in lines:
        if re.match(rf'\s*.include\(.*\)\s+".*/{file_name}"', line):
            return

    lines.append('.include(priority=2,duplicate=merge) '
                 f'"$LOCAL_CONFDIR/local.d/{file_name}"\n')
    orig_path.write_text('\n'.join(lines))