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


import zope.component
import zope.interface
from zope.testbrowser.wsgi import TestBrowserLayer
from zope.app.wsgi.testlayer import BrowserLayer
import zope.app.authentication
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

class _AppAuthenticationBrowserLayer(TestBrowserLayer,
                                     BrowserLayer):

    def setUp(self):
        # Typically this would be done by zope.app.principalannotation's
        # bootstrap.zcml but we don't have a dep on that.
        super(_AppAuthenticationBrowserLayer, self).setUp()
        from zope.principalannotation.utility import PrincipalAnnotationUtility
        from zope.principalannotation.interfaces import IPrincipalAnnotationUtility
        from zope import component
        gsm = component.getGlobalSiteManager()
        gsm.registerUtility(PrincipalAnnotationUtility(),
                            IPrincipalAnnotationUtility)

        # I think that maybe zope.app.testing was the dependency that register this.
        from zope.session.interfaces import IClientIdManager
        from zope.session.http import CookieClientIdManager
        gsm.registerUtility(CookieClientIdManager(), IClientIdManager)
        from zope.session.interfaces import ISessionDataContainer
        from zope.session.session import PersistentSessionDataContainer

        gsm.registerUtility(PersistentSessionDataContainer(),
                            ISessionDataContainer)

AppAuthenticationLayer = _AppAuthenticationBrowserLayer(zope.app.authentication,
                                                        allowTearDown=True)
# from zope.app.testing.functional import ZCMLLayer
# import os
# AppAuthenticationLayer = ZCMLLayer(
#     os.path.join(os.path.split(__file__)[0], 'ftesting.zcml'),
#     __name__, 'AppAuthenticationLayer', allow_teardown=True)

def provideUtility(provided, component, name=''):
    gsm = zope.component.getGlobalSiteManager()
    gsm.registerUtility(component, provided, name, event=False)

stypes = list, tuple
def provideAdapter(required, provided, factory, name='', using=None, **kw):
    assert 'with' not in kw
    assert not isinstance(factory, stypes), "Factory cannot be a list or tuple"

    gsm = zope.component.getGlobalSiteManager()

    if using:
        required = (required, ) + tuple(using)
    elif not isinstance(required, stypes):
        required = (required,)

    gsm.registerAdapter(factory, required, provided, name, event=False)

def browserView(for_, name, factory, layer=IDefaultBrowserLayer,
                providing=zope.interface.Interface):
    """Define a global browser view
    """
    provideAdapter(for_, providing, factory, name, (layer,))

def browserViewProviding(for_, factory, providing, layer=IDefaultBrowserLayer):
    """Define a view providing a particular interface."""
    return browserView(for_, '', factory, layer, providing)

def provideMultiView(for_, type, providing, name, factory, layer=None):
    if layer is None:
        layer = type
    provideAdapter(for_[0], providing, factory, name, tuple(for_[1:])+(layer,))

from zope.annotation.attribute import AttributeAnnotations
def setUpAnnotations():
    zope.component.provideAdapter(AttributeAnnotations)

from zope.site.site import SiteManagerAdapter
from zope.component.interfaces import IComponentLookup
from zope.interface import Interface
def setUpSiteManagerLookup():
    zope.component.provideAdapter(SiteManagerAdapter, (Interface,),
                                  IComponentLookup)
