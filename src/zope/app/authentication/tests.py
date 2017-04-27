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
"""Pluggable Authentication Service Tests
"""
from __future__ import absolute_import
__docformat__ = "reStructuredText"

import unittest

import doctest
from zope.interface import implementer
from zope.component import provideUtility, provideAdapter, provideHandler
from zope.component.eventtesting import getEvents, clearEvents
from zope.component.testing import setUp as CASetUp, tearDown
from zope.component.testing import PlacelessSetup as CAPlacelessSetup
from zope.component.eventtesting import PlacelessSetup as EventPlacelessSetup

from zope.publisher.interfaces import IRequest

from zope.session.interfaces import \
        IClientId, IClientIdManager, ISession, ISessionDataContainer
from zope.session.session import \
        ClientId, Session, PersistentSessionDataContainer
from zope.session.http import CookieClientIdManager

from zope.publisher import base
from zope.pluggableauth.plugins.session import SessionCredentialsPlugin

@implementer(IClientId)
class TestClientId(object):
    def __new__(cls, request):
        return 'dummyclientidfortesting'

import zope.component.hooks

from zope.annotation.attribute import AttributeAnnotations
def setUpAnnotations():
    zope.component.provideAdapter(AttributeAnnotations)


from zope.traversing.interfaces import ITraversable
import zope.traversing.api
from zope.container.interfaces import ISimpleReadContainer
from zope.container.traversal import ContainerTraversable
def setUpTraversal():
    from zope.traversing.testing import setUp
    setUp()
    zope.component.provideAdapter(ContainerTraversable,
                                  (ISimpleReadContainer,), ITraversable)

from zope.site.site import SiteManagerAdapter
from zope.component.interfaces import IComponentLookup
from zope.interface import Interface
def setUpSiteManagerLookup():
    zope.component.provideAdapter(SiteManagerAdapter, (Interface,),
                                  IComponentLookup)

from zope.site.folder import rootFolder

from zope.site.site import LocalSiteManager
import zope.component.interfaces

def createSiteManager(folder, setsite=False):
    if not zope.component.interfaces.ISite.providedBy(folder):
        folder.setSiteManager(LocalSiteManager(folder))
    if setsite:
        zope.component.hooks.setSite(folder)
    return zope.traversing.api.traverse(folder, "++etc++site")

from zope.password.testing import setUpPasswordManagers
from zope.container.testing import PlacelessSetup as ContainerPlacelessSetup
from zope.schema.vocabulary import setVocabularyRegistry
from zope.component.testing import PlacelessSetup as CAPlacelessSetup
from zope.component.eventtesting import PlacelessSetup as EventPlacelessSetup
from zope.i18n.testing import PlacelessSetup as I18nPlacelessSetup

class PlacelessSetup(CAPlacelessSetup,
                     EventPlacelessSetup,
                     I18nPlacelessSetup,
                     ContainerPlacelessSetup):

    def setUp(self, doctesttest=None):
        CAPlacelessSetup.setUp(self)
        EventPlacelessSetup.setUp(self)
        ContainerPlacelessSetup.setUp(self)
        I18nPlacelessSetup.setUp(self)

        setUpPasswordManagers()
        #ztapi.browserView(None, 'absolute_url', AbsoluteURL)
        #ztapi.browserViewProviding(None, AbsoluteURL, IAbsoluteURL)

        from zope.security.testing import addCheckerPublic
        addCheckerPublic()

        from zope.security.management import newInteraction
        newInteraction()

        setVocabularyRegistry(None)

setUp = PlacelessSetup().setUp

def placefulSetUp(site=False):
    PlacelessSetup().setUp()
    zope.component.hooks.setHooks()
    setUpAnnotations()
    setUpTraversal()
    setUpSiteManagerLookup()

    if site:
        site = rootFolder()
        createSiteManager(site, setsite=True)
        return site

def placefulTearDown():
    PlacelessSetup().tearDown()
    zope.component.hooks.resetHooks()
    zope.component.hooks.setSite()

def siteSetUp(test):
    placefulSetUp(site=True)

def siteTearDown(test):
    placefulTearDown()

def sessionSetUp(session_data_container_class=PersistentSessionDataContainer):
    setUp()
    provideAdapter(TestClientId, [IRequest], IClientId)
    provideAdapter(Session, [IRequest], ISession)
    provideUtility(CookieClientIdManager(), IClientIdManager)
    sdc = session_data_container_class()
    provideUtility(sdc, ISessionDataContainer, '')

def nonHTTPSessionTestCaseSetUp(sdc_class=PersistentSessionDataContainer):
    # I am getting an error with ClientId and not TestClientId
    setUp()
    provideAdapter(ClientId, [IRequest], IClientId)
    provideAdapter(Session, [IRequest], ISession)
    provideUtility(CookieClientIdManager(), IClientIdManager)
    sdc = sdc_class()
    provideUtility(sdc, ISessionDataContainer, '')


class NonHTTPSessionTestCase(unittest.TestCase):
    # Small test suite to catch an error with non HTTP protocols, like FTP
    # and SessionCredentialsPlugin.
    def setUp(self):
        nonHTTPSessionTestCaseSetUp()

    def tearDown(self):
        placefulTearDown()

    def test_exeractCredentials(self):
        plugin = SessionCredentialsPlugin()

        self.assertEqual(plugin.extractCredentials(base.TestRequest('/')), None)

    def test_challenge(self):
        plugin = SessionCredentialsPlugin()

        self.assertEqual(plugin.challenge(base.TestRequest('/')), False)

    def test_logout(self):
        plugin = SessionCredentialsPlugin()

        self.assertEqual(plugin.logout(base.TestRequest('/')), False)

class LoginLogout(object):
    # Dummy implementation of zope.app.security.browser.auth.LoginLogout

    def __call__(self):
        return None

from zope.publisher.browser import BrowserView
from zope.publisher.interfaces.browser import IBrowserPublisher
from zope.browsermenu.menu import getFirstMenuItem


@implementer(IBrowserPublisher)
class ManagementViewSelector(BrowserView):
    """View that selects the first available management view.

    Support 'zmi_views' actions like: 'javascript:alert("hello")',
    '../view_on_parent.html' or '++rollover++'.
    """
    # Copied from zope.app.publication
    # Simplified to assert just the test case we expect.

    def browserDefault(self, request):
        return self, ()

    def __call__(self):
        item = getFirstMenuItem('zmi_views', self.context, self.request)
        assert item
        redirect_url = item['action']
        if not redirect_url.lower().startswith(('../', 'javascript:', '++')):
            self.request.response.redirect(redirect_url)
            return u''
        raise AssertionError("Should not get here") # pragma: no cover

from zope.authentication.interfaces import IAuthentication
from zope.component import getUtility
from zope.publisher.browser import BrowserPage


class Unauthorized(BrowserPage):

    def template(self):
        return "You are not authorized"

    def __call__(self):
        # Set the error status to 403 (Forbidden) in the case when we don't
        # challenge the user
        self.request.response.setStatus(403)

        # make sure that squid does not keep the response in the cache
        self.request.response.setHeader('Expires', 'Mon, 26 Jul 1997 05:00:00 GMT')
        self.request.response.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.request.response.setHeader('Pragma', 'no-cache')

        principal = self.request.principal
        auth = getUtility(IAuthentication)
        auth.unauthorized(principal.id, self.request)
        if self.request.response.getStatus() not in (302, 303):
            return self.template()

from zope.testing import renormalizing

import re
checker = renormalizing.RENormalizing([
    (re.compile("u('[^']*?')"), r"\1"),
    (re.compile('u("[^"]*?")'), r"\1"),
])


def test_suite():
    flags = (doctest.NORMALIZE_WHITESPACE
             | renormalizing.IGNORE_EXCEPTION_MODULE_IN_PYTHON2
             | doctest.ELLIPSIS)
    return unittest.TestSuite((
        doctest.DocTestSuite('zope.app.authentication.interfaces'),
        doctest.DocTestSuite('zope.app.authentication.password'),
        doctest.DocTestSuite('zope.app.authentication.generic'),
        doctest.DocTestSuite('zope.app.authentication.httpplugins'),
        doctest.DocTestSuite('zope.app.authentication.ftpplugins'),
        doctest.DocTestSuite('zope.app.authentication.groupfolder'),
        doctest.DocFileSuite('principalfolder.rst',
                             optionflags=flags,
                             checker=checker,
                             setUp=setUp,
                             tearDown=tearDown),
        doctest.DocTestSuite('zope.app.authentication.principalfolder',
                             optionflags=flags,
                             checker=checker,
                             setUp=setUp,
                             tearDown=tearDown),
        doctest.DocTestSuite('zope.app.authentication.idpicker'),
        doctest.DocTestSuite('zope.app.authentication.session',
                             optionflags=flags,
                             checker=checker,
                             setUp=siteSetUp,
                             tearDown=siteTearDown),
        doctest.DocFileSuite('README.rst',
                             setUp=siteSetUp,
                             tearDown=siteTearDown,
                             optionflags=flags,
                             checker=checker,
                             globs={'provideUtility': provideUtility,
                                    'provideAdapter': provideAdapter,
                                    'provideHandler': provideHandler,
                                    'getEvents': getEvents,
                                    'clearEvents': clearEvents,
                                    }),
        doctest.DocFileSuite('groupfolder.rst',
                             setUp=setUp,
                             tearDown=tearDown,
                             optionflags=flags,
                             checker=checker,
                             ),
        doctest.DocFileSuite('vocabulary.rst',
                             setUp=setUp,
                             tearDown=tearDown,
                             optionflags=flags,
                             checker=checker,
                             ),
        unittest.makeSuite(NonHTTPSessionTestCase),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
