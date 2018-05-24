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

@apps @mediawiki
Feature: Wiki Engine
  Manage wikis, multimedia and more.

Background:
  Given I'm a logged in user
  Given the mediawiki application is installed

Scenario: Enable mediawiki application
  Given the mediawiki application is disabled
  When I enable the mediawiki application
  Then the mediawiki site should be available

Scenario: Disable mediawiki application
  Given the mediawiki application is enabled
  When I disable the mediawiki application
  Then the mediawiki site should not be available

Scenario: Enable public registrations
  Given the mediawiki application is enabled
  When I enable mediawiki public registrations
  Then the mediawiki site should allow creating accounts

Scenario: Disable public registrations
  Given the mediawiki application is enabled
  When I disable mediawiki public registrations
  Then the mediawiki site should not allow creating accounts

Scenario: Enable private mode
  Given the mediawiki application is enabled
  When I enable mediawiki private mode
  Then the mediawiki site should not allow creating accounts
  Then the mediawiki site should not allow anonymous reads and writes

Scenario: Disable private mode
  Given the mediawiki application is enabled
  When I disable mediawiki private mode
  Then the mediawiki site should allow anonymous reads and writes
