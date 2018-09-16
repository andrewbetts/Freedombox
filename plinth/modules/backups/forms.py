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
"""
Forms for backups module.
"""

import os

from django import forms
from django.core import validators
from django.core.validators import FileExtensionValidator
from django.utils.translation import ugettext_lazy as _

from . import backups as backups_api
from . import get_export_locations, get_archive_path


class CreateArchiveForm(forms.Form):
    name = forms.CharField(
        label=_('Archive name'), strip=True,
        help_text=_('Name for new backup archive.'), validators=[
            validators.RegexValidator(r'^[^/]+$', _('Invalid archive name'))
        ])

    selected_apps = forms.MultipleChoiceField(
        label=_('Included apps'),
        help_text=_('Apps to include in the backup'),
        widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        """Initialize the form with selectable apps."""
        super().__init__(*args, **kwargs)
        apps = backups_api.get_all_apps_for_backup()
        self.fields['selected_apps'].choices = [
            (app[0], app[1].name) for app in apps]
        self.fields['selected_apps'].initial = [app[0] for app in apps]


class ExportArchiveForm(forms.Form):
    disk = forms.ChoiceField(
        label=_('Disk'), widget=forms.RadioSelect(),
        help_text=_('Disk or removable storage where the backup archive will '
                    'be saved.'))

    def __init__(self, *args, **kwargs):
        """Initialize the form with disk choices."""
        super().__init__(*args, **kwargs)
        self.fields['disk'].choices = get_export_locations()


class RestoreForm(forms.Form):
    selected_apps = forms.MultipleChoiceField(
        label=_('Restore apps'),
        help_text=_('Apps data to restore from the backup'),
        widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        """Initialize the form with selectable apps."""
        apps = kwargs.pop('apps')
        super().__init__(*args, **kwargs)
        self.fields['selected_apps'].choices = [
            (app[0], app[1].name) for app in apps]
        self.fields['selected_apps'].initial = [app[0] for app in apps]


class UploadForm(forms.Form):
    location = forms.ChoiceField(
        choices=(),
        label=_('Location'),
        initial='',
        widget=forms.Select(),
        required=True,
        help_text=_('Location to upload the archive to'))
    file = forms.FileField(label=_('Upload File'), required=True,
            validators=[FileExtensionValidator(['gz'],
                'Backup files have to be in .tar.gz format')],
            help_text=_('Select the backup file you want to upload'))

    def __init__(self, *args, **kwargs):
        """Initialize the form with location choices."""
        super().__init__(*args, **kwargs)
        # TODO: write a test that assures the format of get_export_locations
        self.fields['location'].choices = get_export_locations()

    def clean(self):
        """Check that the uploaded file does not exist"""
        cleaned_data = super().clean()
        file = cleaned_data.get('file')
        location = cleaned_data.get('location')
        if (file and file.name):
            filepath = get_archive_path(location, file.name)
            if os.path.exists(filepath):
                raise forms.ValidationError("File %s already exists" % file.name)
            else:
                self.cleaned_data.update({'filepath': filepath})
