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
"""Pluggable Authentication Utility Interfaces"""

import zope.interface
import zope.schema
import zope.security.interfaces
# BBB: the password managers were moved into zope.password package.
from zope.password.interfaces import IPasswordManager
# BBB: using zope.pluggableauth
from zope.pluggableauth.interfaces import AuthenticatedPrincipalCreated
from zope.pluggableauth.interfaces import FoundPrincipalCreated
from zope.pluggableauth.interfaces import IAuthenticatedPrincipalCreated
from zope.pluggableauth.interfaces import IAuthenticatedPrincipalFactory
from zope.pluggableauth.interfaces import IAuthenticatorPlugin
from zope.pluggableauth.interfaces import ICredentialsPlugin
from zope.pluggableauth.interfaces import IFoundPrincipalCreated
from zope.pluggableauth.interfaces import IFoundPrincipalFactory
from zope.pluggableauth.interfaces import IGroupAdded
from zope.pluggableauth.interfaces import IPluggableAuthentication
from zope.pluggableauth.interfaces import IPlugin
from zope.pluggableauth.interfaces import IPrincipal
from zope.pluggableauth.interfaces import IPrincipalCreated
from zope.pluggableauth.interfaces import IPrincipalFactory
from zope.pluggableauth.interfaces import IPrincipalInfo
from zope.pluggableauth.interfaces import IPrincipalsAddedToGroup
from zope.pluggableauth.interfaces import IPrincipalsRemovedFromGroup
from zope.pluggableauth.interfaces import IQueriableAuthenticator
from zope.pluggableauth.interfaces import IQuerySchemaSearch
# BBB: using zope.pluggableauth
from zope.pluggableauth.plugins.groupfolder import GroupAdded

from zope.app.authentication.i18n import ZopeMessageFactory as _
