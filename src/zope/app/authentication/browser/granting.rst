Granting View
=============

The granting view allows the user to grant permissions and roles to
principals. The view unfortunately depends on a lot of other components:

  - Roles

    >>> from zope.app.authentication.browser import tests as ztapi
    >>> from zope.securitypolicy.role import Role
    >>> from zope.securitypolicy.interfaces import IRole
    >>> ztapi.provideUtility(IRole, Role(u'role1', u'Role 1'), u'role1')
    >>> ztapi.provideUtility(IRole, Role(u'role2', u'Role 2'), u'role2')
    >>> ztapi.provideUtility(IRole, Role(u'role3', u'Role 3'), u'role3')

  - Permissions

    >>> from zope.security.permission import Permission
    >>> from zope.security.interfaces import IPermission
    >>> ztapi.provideUtility(IPermission, Permission(u'permission1',
    ...                      u'Permission 1'), u'permission1')
    >>> ztapi.provideUtility(IPermission, Permission(u'permission2',
    ...                      u'Permission 2'), u'permission2')
    >>> ztapi.provideUtility(IPermission, Permission(u'permission3',
    ...                      u'Permission 3'), u'permission3')

  - Authentication Utility

    >>> class Principal:
    ...     def __init__(self, id, title): self.id, self.title = id, title

    >>> from zope.app.security.interfaces import IAuthentication
    >>> from zope.app.security.interfaces import PrincipalLookupError
    >>> from zope.interface import implementer
    >>> @implementer(IAuthentication)
    ... class AuthUtility(object):
    ...     data = {'jim': Principal('jim', 'Jim Fulton'),
    ...             'stephan': Principal('stephan', 'Stephan Richter')}
    ...
    ...     def getPrincipal(self, id):
    ...         try:
    ...             return self.data.get(id)
    ...         except KeyError:
    ...             raise PrincipalLookupError(id)
    ...
    ...     def getPrincipals(self, search):
    ...         return [principal
    ...                 for principal in self.data.values()
    ...                 if search in principal.title]

    >>> ztapi.provideUtility(IAuthentication, AuthUtility())

  - Security-related Adapters

    >>> from zope.annotation.interfaces import IAnnotatable
    >>> from zope.securitypolicy.interfaces import IPrincipalRoleManager
    >>> from zope.securitypolicy.principalrole import \
    ...     AnnotationPrincipalRoleManager

    >>> ztapi.provideAdapter(IAnnotatable, IPrincipalRoleManager,
    ...                      AnnotationPrincipalRoleManager)

    >>> from zope.securitypolicy.interfaces import \
    ...     IPrincipalPermissionManager
    >>> from zope.securitypolicy.principalpermission import \
    ...     AnnotationPrincipalPermissionManager

    >>> ztapi.provideAdapter(IAnnotatable, IPrincipalPermissionManager,
    ...                      AnnotationPrincipalPermissionManager)

  - Vocabulary Choice Widgets

    >>> from zope.schema.interfaces import IChoice
    >>> from zope.formlib.interfaces import IInputWidget
    >>> from zope.formlib.widgets import ChoiceInputWidget
    >>> ztapi.browserViewProviding(IChoice, ChoiceInputWidget, IInputWidget)

    >>> from zope.schema.interfaces import IVocabularyTokenized
    >>> from zope.publisher.interfaces.browser import IBrowserRequest
    >>> from zope.formlib.widgets import DropdownWidget
    >>> ztapi.provideMultiView((IChoice, IVocabularyTokenized),
    ...                        IBrowserRequest, IInputWidget, '',
    ...                        DropdownWidget)

  - Support Views for the Principal Source Widget

    >>> from zope.app.security.interfaces import IPrincipalSource
    >>> from zope.app.security.browser.principalterms import PrincipalTerms
    >>> from zope.browser.interfaces import ITerms
    >>> ztapi.browserViewProviding(IPrincipalSource, PrincipalTerms, ITerms)

    >>> from zope.app.security.browser.auth import AuthUtilitySearchView
    >>> from zope.formlib.interfaces import ISourceQueryView
    >>> ztapi.browserViewProviding(IAuthentication,
    ...                            AuthUtilitySearchView,
    ...                            ISourceQueryView)


    >>> from zope.schema.interfaces import ISource
    >>> from zope.formlib.source import SourceInputWidget
    >>> ztapi.provideMultiView((IChoice, ISource), IBrowserRequest,
    ...                        IInputWidget, '', SourceInputWidget)

  - Attribute Annotatable Adapter

    >>> from zope.app.authentication import tests as setup
    >>> setup.setUpAnnotations()
    >>> setup.setUpSiteManagerLookup()

  - Content Object

    >>> from zope.annotation.interfaces import IAttributeAnnotatable
    >>> @implementer(IAttributeAnnotatable)
    ... class Content(object):
    ...     __annotations__ = {}

  (This is Jim's understanding of a "easy" setup!)

Now that we have all the components we need, let's create *the* view.

  >>> ob = Content()
  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()

  >>> from zope.app.authentication.browser.granting import Granting
  >>> view = Granting(ob, request)

If we call status, we get nothing and the view's principal attribute is `None`:

  >>> print(view.status())
  <BLANKLINE>
  >>> view.principal

Since we have not selected a principal, we have no role or permission widgets:

  >>> getattr(view, 'roles', None)
  >>> getattr(view, 'permissions', None)

Now that we have a selected principal, then


  >>> view.request.form['field.principal.displayed'] = 'y'
  >>> view.request.form['field.principal'] = 'amlt'

(Yes, 'amlt' is the base 64 code for 'jim'.)

  >>> print(view.status())
  <BLANKLINE>

and now the `view.principal` is set:

  >>> print(view.principal)
  jim

Now we should have a list of role and permission widgets, and all of them
should be unset, because do not have any settings for 'jim'.

  >>> [str(role.context.title) for role in view.roles]
  ['Role 1', 'Role 2', 'Role 3']
  >>> [str(perm.context.title) for perm in view.permissions]
  ['Permission 1', 'Permission 2', 'Permission 3']

Now we change some settings and submit the form:

  >>> from zope.securitypolicy.interfaces import Allow, Deny, Unset

  >>> view.request.form['field.amlt.role.role1'] = 'unset'
  >>> view.request.form['field.amlt.role.role1-empty-makrer'] = 1
  >>> view.request.form['field.amlt.role.role2'] = 'allow'
  >>> view.request.form['field.amlt.role.role2-empty-makrer'] = 1
  >>> view.request.form['field.amlt.role.role3'] = 'deny'
  >>> view.request.form['field.amlt.role.role3-empty-makrer'] = 1

  >>> view.request.form['field.amlt.permission.permission1'] = 'unset'
  >>> view.request.form['field.amlt.permission.permission1-empty-makrer'] = 1
  >>> view.request.form['field.amlt.permission.permission2'] = 'allow'
  >>> view.request.form['field.amlt.permission.permission2-empty-makrer'] = 1
  >>> view.request.form['field.amlt.permission.permission3'] = 'deny'
  >>> view.request.form['field.amlt.permission.permission3-empty-makrer'] = 1

  >>> view.request.form['GRANT_SUBMIT'] = 'Submit'

If we get the status now, the data should be written and a status message
should be returned:

  >>> print(view.status())
  Grants updated.

  >>> roles = IPrincipalRoleManager(ob)
  >>> roles.getSetting('role1', 'jim') is Unset
  True
  >>> roles.getSetting('role2', 'jim') is Allow
  True
  >>> roles.getSetting('role3', 'jim') is Deny
  True

  >>> roles = IPrincipalPermissionManager(ob)
  >>> roles.getSetting('permission1', 'jim') is Unset
  True
  >>> roles.getSetting('permission2', 'jim') is Allow
  True
  >>> roles.getSetting('permission3', 'jim') is Deny
  True
