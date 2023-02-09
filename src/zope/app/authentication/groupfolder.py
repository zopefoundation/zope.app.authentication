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
"""Zope Groups Folder implementation."""

# BBB using zope.pluggableauth.plugin.groupfolder
from zope.pluggableauth.plugins.groupfolder import GroupCycle
from zope.pluggableauth.plugins.groupfolder import GroupFolder
from zope.pluggableauth.plugins.groupfolder import GroupInfo
from zope.pluggableauth.plugins.groupfolder import GroupInformation
from zope.pluggableauth.plugins.groupfolder import IGroupContained
from zope.pluggableauth.plugins.groupfolder import IGroupFolder
from zope.pluggableauth.plugins.groupfolder import IGroupInformation
from zope.pluggableauth.plugins.groupfolder import IGroupPrincipalInfo
from zope.pluggableauth.plugins.groupfolder import IGroupSearchCriteria
from zope.pluggableauth.plugins.groupfolder import InvalidGroupId
from zope.pluggableauth.plugins.groupfolder import InvalidPrincipalIds
from zope.pluggableauth.plugins.groupfolder import nocycles
from zope.pluggableauth.plugins.groupfolder import setGroupsForPrincipal
from zope.pluggableauth.plugins.groupfolder import setMemberSubscriber
from zope.pluggableauth.plugins.groupfolder import specialGroups
