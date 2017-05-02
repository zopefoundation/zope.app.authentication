##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
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
"""Login Form

"""
from zope.authentication.interfaces import IUnauthenticatedPrincipal

class LoginForm(object):
    """Mix-in class to implement login form logic"""

    context = None
    request = None
    unauthenticated = None
    camefrom = None

    def __call__(self):
        request = self.request
        principal = request.principal

        unauthenticated = IUnauthenticatedPrincipal.providedBy(principal)
        self.unauthenticated = unauthenticated

        camefrom = request.get('camefrom')
        if isinstance(camefrom, list):
            # Beginning on python2.6 this happens if the parameter is
            # supplied more than once
            camefrom = camefrom[0]
        self.camefrom = camefrom

        if not unauthenticated and 'SUBMIT' in request:
            # authenticated by submitting
            request.response.redirect(camefrom or '.')
            return ''

        return self.index() # call template
