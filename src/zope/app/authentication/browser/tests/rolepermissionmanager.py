##############################################################################
#
# Copyright (c) 2001, 2002 Zope Foundation and Contributors.
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
"""Test IRolePermissionManager class that has no context.
"""

from zope.interface import implementer
from zope.securitypolicy.interfaces import Allow
from zope.securitypolicy.interfaces import Deny
from zope.securitypolicy.interfaces import IRolePermissionManager
from zope.securitypolicy.interfaces import IRolePermissionMap
from zope.securitypolicy.securitymap import SecurityMap


@implementer(IRolePermissionManager, IRolePermissionMap)
class RolePermissionManager:
    """
    provide adapter that manages role permission data in an object attribute
    """

    def __init__(self):
        self._rp = SecurityMap()

    def grantPermissionToRole(self, permission_id, role_id):
        ''' See the interface IRolePermissionManager '''
        rp = self._getRolePermissions(create=1)
        rp.addCell(permission_id, role_id, Allow)

    def denyPermissionToRole(self, permission_id, role_id):
        ''' See the interface IRolePermissionManager '''
        rp = self._getRolePermissions(create=1)
        rp.addCell(permission_id, role_id, Deny)

    def unsetPermissionFromRole(self, permission_id, role_id):
        ''' See the interface IRolePermissionManager '''
        rp = self._getRolePermissions()
        # Only unset if there is a security map, otherwise, we're done
        if rp:
            rp.delCell(permission_id, role_id)

    def getRolesForPermission(self, permission_id):
        '''See interface IRolePermissionMap'''
        rp = self._getRolePermissions()
        if rp:
            return rp.getRow(permission_id)
        raise NotImplementedError("Should never get here")

    def getPermissionsForRole(self, role_id):
        '''See interface IRolePermissionMap'''
        rp = self._getRolePermissions()
        if rp:
            return rp.getCol(role_id)
        raise NotImplementedError("Should never get here")

    def getRolesAndPermissions(self):
        '''See interface IRolePermissionMap'''
        raise NotImplementedError("Not used by tests")

    def getSetting(self, permission_id, role_id):
        '''See interface IRolePermissionMap'''
        raise NotImplementedError("Not used by tests")

    def _getRolePermissions(self, create=0):
        """Get the role permission map stored in the context, optionally
           creating one if necessary"""
        return self._rp
