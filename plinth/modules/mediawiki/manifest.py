#
# This file is part of FreedomBox.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from django.utils.translation import ugettext_lazy as _

from plinth.modules.backups.api import validate as validate_backup
from plinth.clients import validate

clients = validate([{
    'name': _('MediaWiki'),
    'platforms': [{
        'type': 'web',
        'url': '/mediawiki'
    }]
}])

backup = validate_backup({
    'config': {
        'files': ['/etc/mediawiki/FreedomBoxSettings.php']
    },
    'data': {
        'directories': ['/var/lib/mediawiki-db/']
    }
})
