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
"""ZODB-based Authentication Source"""

from zope.pluggableauth.factories import AuthenticatedPrincipalFactory
from zope.pluggableauth.factories import FoundPrincipalFactory
from zope.pluggableauth.factories import Principal
from zope.pluggableauth.factories import PrincipalInfo
# BBB using zope.pluggableauth
from zope.pluggableauth.interfaces import IAuthenticatorPlugin
# BBB using zope.pluggableauth.plugins.principalfolder
from zope.pluggableauth.plugins.principalfolder import IInternalPrincipal
from zope.pluggableauth.plugins.principalfolder import \
    IInternalPrincipalContained
from zope.pluggableauth.plugins.principalfolder import \
    IInternalPrincipalContainer
from zope.pluggableauth.plugins.principalfolder import InternalPrincipal
from zope.pluggableauth.plugins.principalfolder import ISearchSchema
from zope.pluggableauth.plugins.principalfolder import PrincipalFolder
