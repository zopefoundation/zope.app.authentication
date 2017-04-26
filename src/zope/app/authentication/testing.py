##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
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
"""zope.app.authentication common test related classes/functions/objects.

"""

__docformat__ = "reStructuredText"



from zope.testbrowser.wsgi import TestBrowserLayer
from zope.app.wsgi.testlayer import BrowserLayer
import zope.app.authentication

class _AppAuthenticationBrowserLayer(TestBrowserLayer,
                                     BrowserLayer):

    def setUp(self):
        # Typically this would be done by zope.app.principalannotation's
        # bootstrap.zcml but we don't have a dep on that.
        super(_AppAuthenticationBrowserLayer, self).setUp()
        from zope.principalannotation.utility import PrincipalAnnotationUtility
        from zope.principalannotation.interfaces import IPrincipalAnnotationUtility
        from zope import component
        component.getGlobalSiteManager().registerUtility(PrincipalAnnotationUtility(),
                                                         IPrincipalAnnotationUtility)


AppAuthenticationLayer = _AppAuthenticationBrowserLayer(zope.app.authentication,
                                                        allowTearDown=True)
