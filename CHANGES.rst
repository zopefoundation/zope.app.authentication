=======
Changes
=======

3.10 (unreleased)
-----------------

- Nothing changed yet.


3.9 (2010-10-18)
----------------

* Move concrete IAuthenticatorPlugin implementations to
  zope.pluggableauth.plugins. Leave backwards compatibility imports.

* Use zope.formlib throughout to lift the dependency on zope.app.form. As it
  turns out, zope.app.form is still a indirect test dependency though.

3.8.0 (2010-09-25)
------------------

* Using python's ``doctest`` module instead of deprecated
  ``zope.testing.doctest[unit]``.

* Moved the following views from `zope.app.securitypolicy` here, to inverse
  dependency between these two packages, as `zope.app.securitypolicy`
  deprecated in ZTK 1.0:

  - ``@@grant.html``
  - ``@@AllRolePermissions.html``
  - ``@@RolePermissions.html``
  - ``@@RolesWithPermission.html``

3.7.1 (2010-02-11)
------------------

* Using the new `principalfactories.zcml` file, from ``zope.pluggableauth``,
  to avoid duplication errors, in the adapters registration.

3.7.0 (2010-02-08)
------------------

* The Pluggable Authentication utility has been severed and released
  in a standalone package: `zope.pluggableauth`. We are now using this
  new package, providing backward compatibility imports to assure a
  smooth transition.

3.6.2 (2010-01-05)
------------------

* Fix tests by using zope.login, and require new zope.publisher 3.12.

3.6.1 (2009-10-07)
------------------

* Fix ftesting.zcml due to ``zope.securitypolicy`` update.

* Don't use ``zope.app.testing.ztapi`` in tests, use zope.component's
  testing functions instead.

* Fix functional tests and stop using port 8081. Redirecting to
  different port without trusted flag is not allowed.

3.6.0 (2009-03-14)
------------------

* Separate the presentation template and camefrom/redirection logic for the
  ``loginForm.html`` view. Now the logic is contained in the
  ``zope.app.authentication.browser.loginform.LoginForm`` class.

* Fix login form redirection failure in some cases with Python 2.6.

* Use the new ``zope.authentication`` package instead of ``zope.app.security``.

* The "Password Manager Names" vocabulary and simple password manager registry
  were moved to the ``zope.password`` package.

* Remove deprecated code.

3.5.0 (2009-03-06)
------------------

* Split password manager functionality off to the new ``zope.password``
  package. Backward-compatibility imports are left in place.

* Use ``zope.site`` instead of ``zope.app.component``. (Browser code still
  needs ``zope.app.component`` as it depends on view classes of this
  package.)

3.5.0a2 (2009-02-01)
--------------------

* Make old encoded passwords really work.

3.5.0a1 (2009-01-31)
--------------------

* Use ``zope.container`` instead of ``zope.app.container``. (Browser code
  still needs ``zope.app.container`` as it depends on view classes of this
  package.)

* Encoded passwords are now stored with a prefix ({MD5}, {SHA1},
  {SSHA}) indicating the used encoding schema. Old (encoded) passwords
  can still be used.

* Add an SSHA password manager that is compatible with standard LDAP
  passwords. As this encoding gives better security agains dictionary
  attacks, users are encouraged to switch to this new password schema.

* InternalPrincipal now uses SSHA password manager by default.

3.4.4 (2008-12-12)
------------------

* Depend on zope.session instead of zope.app.session. The first one
  currently has all functionality we need.
* Fix deprecation warnings for ``md5`` and ``sha`` on Python 2.6.

3.4.3 (2008-08-07)
------------------

* No changes. Retag for correct release on PyPI.

3.4.2 (2008-07-09)
-------------------

* Make it compatible with zope.app.container 3.6.1 and 3.5.4 changes,
  Changed ``super(BTreeContainer, self).__init__()`` to
  ``super(GroupFolder, self).__init__()`` in ``GroupFolder`` class.

3.4.1 (2007-10-24)
------------------

* Avoid deprecation warning.

3.4.0 (2007-10-11)
------------------

* Updated package meta-data.

3.4.0b1 (2007-09-27)
--------------------

* First release independent of Zope.
