##############################################################################
#
# Copyright (c) 2004 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Granting Roles and Permissions to Principals

"""

__docformat__ = "reStructuredText"

import base64

import zope.schema
from zope.authentication.principal import PrincipalSource
from zope.component import getUtilitiesFor
from zope.formlib.interfaces import IInputWidget
from zope.formlib.interfaces import MissingInputError
from zope.formlib.utility import setUpWidget
from zope.formlib.widget import renderElement
from zope.formlib.widgets import RadioWidget
from zope.i18nmessageid import ZopeMessageFactory as _
from zope.schema.vocabulary import SimpleTerm
from zope.security.interfaces import IPermission
from zope.securitypolicy.interfaces import Allow
from zope.securitypolicy.interfaces import Deny
from zope.securitypolicy.interfaces import IPrincipalPermissionManager
from zope.securitypolicy.interfaces import IPrincipalRoleManager
from zope.securitypolicy.interfaces import IRole
from zope.securitypolicy.interfaces import Unset
from zope.securitypolicy.vocabulary import GrantVocabulary


try:
    text_type = unicode
except NameError:
    text_type = str

settings_vocabulary = GrantVocabulary([
    SimpleTerm(Allow, token="allow", title=_('Allow')),
    SimpleTerm(Unset, token="unset", title=_('Unset')),
    SimpleTerm(Deny, token='deny', title=_('Deny')),
])


class GrantWidget(RadioWidget):
    """Grant widget for building a colorized matrix.

    The matrix shows anytime the status if you edit the radio widgets.
    This special widget shows the radio input field without labels.
    The labels are added in the header of the table. The order of the radio
    input fields is 'Allowed', 'Unset', 'Deny'.

    """
    orientation = "horizontal"
    _tdTemplate = (
        '\n<td class="%s">\n<center>\n<label for="%s" title="%s">\n'
        '%s\n</label>\n</center>\n</td>\n'
    )

    def __call__(self):
        """See IBrowserWidget."""
        value = self._getFormValue()
        return self.renderValue(value)

    def renderItem(self, index, text, value, name, cssClass):
        """Render an item of the list.

        Revert the order of label and text. Added field id to the lable
        attribute.

        Added tabel td tags for fit in the matrix table.

        """

        tdClass = ''
        id = f'{name}.{index}'
        elem = renderElement('input',
                             value=value,
                             name=name,
                             id=id,
                             cssClass=cssClass,
                             type='radio',
                             extra='onclick="changeMatrix(this);"')
        return self._tdTemplate % (tdClass, id, text, elem)

    def renderSelectedItem(self, index, text, value, name, cssClass):
        """Render a selected item of the list.

        Revert the order of label and text. Added field id to the lable
        attribute.
        """

        tdClass = 'default'
        id = f'{name}.{index}'
        elem = renderElement('input',
                             value=value,
                             name=name,
                             id=id,
                             cssClass=cssClass,
                             checked="checked",
                             type='radio',
                             extra='onclick="changeMatrix(this);"')
        return self._tdTemplate % (tdClass, id, text, elem)

    def renderItems(self, value):
        # check if we want to select first item, the previously selected item
        # or the "no value" item.
        if (value == self.context.missing_value
                and getattr(self, 'firstItem', False)
                and len(self.vocabulary) > 0):
            if self.context.required:
                # Grab the first item from the iterator:
                values = [next(iter(self.vocabulary)).value]
        elif value != self.context.missing_value:
            values = [value]
        else:
            values = []

        items = self.renderItemsWithValues(values)
        return items

    def renderValue(self, value):
        rendered_items = self.renderItems(value)
        return " ".join(rendered_items)


class Granting:

    principal = None

    principal_field = zope.schema.Choice(
        __name__='principal',
        source=PrincipalSource(),
        required=True)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.permissions = None
        self.roles = None
        self.principal_widget = None

    def status(self):
        setUpWidget(self, 'principal', self.principal_field, IInputWidget)
        if not self.principal_widget.hasInput():
            return ''
        try:
            principal = self.principal_widget.getInputValue()
        except MissingInputError:
            return ''

        self.principal = principal

        # Make sure we can use the principal id in a form by base64ing it
        principal_str = text_type(principal)
        principal_bytes = principal_str.encode('utf-8')
        principal_token = base64.b64encode(
            principal_bytes).strip().replace(b'=', b'_')
        if not isinstance(principal_token, str):
            principal_token = principal_token.decode('utf-8')

        roles = [role for name, role in getUtilitiesFor(IRole)]
        roles.sort(key=lambda x: x.title)
        principal_roles = IPrincipalRoleManager(self.context)

        self.roles = []
        for role in roles:
            name = principal_token + '.role.' + role.id
            field = zope.schema.Choice(__name__=name,
                                       title=role.title,
                                       vocabulary=settings_vocabulary)
            setUpWidget(self, name, field, IInputWidget,
                        principal_roles.getSetting(role.id, principal))
            self.roles.append(getattr(self, name + '_widget'))

        perms = [perm for name, perm in getUtilitiesFor(IPermission)]
        perms.sort(key=lambda x: x.title)
        principal_perms = IPrincipalPermissionManager(self.context)

        self.permissions = []
        for perm in perms:
            if perm.id == 'zope.Public':
                continue
            name = principal_token + '.permission.' + perm.id
            field = zope.schema.Choice(__name__=name,
                                       title=perm.title,
                                       vocabulary=settings_vocabulary)
            setUpWidget(self, name, field, IInputWidget,
                        principal_perms.getSetting(perm.id, principal))
            self.permissions.append(
                getattr(self, name + '_widget'))

        if 'GRANT_SUBMIT' not in self.request:
            return ''

        for role in roles:
            name = principal_token + '.role.' + role.id
            role_widget = getattr(self, name + '_widget')
            if role_widget.hasInput():
                try:
                    setting = role_widget.getInputValue()
                except MissingInputError:  # pragma: no cover
                    pass
                else:
                    # Arrgh!
                    if setting is Allow:
                        principal_roles.assignRoleToPrincipal(
                            role.id, principal)
                    elif setting is Deny:
                        principal_roles.removeRoleFromPrincipal(
                            role.id, principal)
                    else:
                        principal_roles.unsetRoleForPrincipal(
                            role.id, principal)

        for perm in perms:
            if perm.id == 'zope.Public':
                continue
            name = principal_token + '.permission.' + perm.id
            perm_widget = getattr(self, name + '_widget')
            if perm_widget.hasInput():
                try:
                    setting = perm_widget.getInputValue()
                except MissingInputError:  # pragma: no cover
                    pass
                else:
                    # Arrgh!
                    if setting is Allow:
                        principal_perms.grantPermissionToPrincipal(
                            perm.id, principal)
                    elif setting is Deny:
                        principal_perms.denyPermissionToPrincipal(
                            perm.id, principal)
                    else:
                        principal_perms.unsetPermissionForPrincipal(
                            perm.id, principal)

        return _('Grants updated.')
