Using Group Folders
===================

Group folders are used to define groups.  Before you can define
groups, you have to create a group folder and configure it in a
pluggable authentication utility. The group folder has to be
registered with a pluggable authentication utility before defining any
groups.  This is because the groups folder needs to use the pluggable
authentication utility to find all of the groups containing a given
group so that it can check for group cycles. Not all of a group's
groups need to be defined in it's group folder. Other groups folders
or group-defining plugins could define groups for a group.

Let's walk through an example.

First, We need to create and register a pluggable authentication utility.

  >>> print(http(r"""
  ... POST /++etc++site/default/@@contents.html HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Content-Type: application/x-www-form-urlencoded
  ... Cookie: zope3_cs_6a553b3=-j7C3CdeW9sUK8BP5x97u2d9o242xMJDzJd8HCQ5AAi9xeFcGTFkAs
  ... Referer: http://localhost/++etc++site/default/@@contents.html?type_name=BrowserAdd__zope.pluggableauth.authentication.PluggableAuthentication
  ...
  ... type_name=BrowserAdd__zope.pluggableauth.authentication.PluggableAuthentication&new_value=PAU"""))
  HTTP/1.1 303 See Other
  ...

  >>> print(http(r"""
  ... GET /++etc++site/default/PAU/@@registration.html HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Cookie: zope3_cs_6a553b3=-j7C3CdeW9sUK8BP5x97u2d9o242xMJDzJd8HCQ5AAi9xeFcGTFkAs
  ... Referer: http://localhost/++etc++site/default/@@contents.html?type_name=BrowserAdd__zope.pluggableauth.authentication.PluggableAuthentication
  ... """))
  HTTP/1.1 200 Ok
  ...

Register PAU.

  >>> content_type, content = encodeMultipartFormdata([
  ...     ('field.comment', ''),
  ...     ('field.actions.register', 'Register')])
  >>> print(http(b"""
  ... POST /++etc++site/default/PAU/addRegistration.html HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Content-Type: %b
  ... Cookie: zope3_cs_6a553b3=-j7C3CdeW9sUK8BP5x97u2d9o242xMJDzJd8HCQ5AAi9xeFcGTFkAs
  ... Referer: http://localhost/++etc++site/default/PAU/addRegistration.html
  ...
  ... %b
  ... """ % (content_type, content)))
  HTTP/1.1 303 See Other
  ...

Add a Principal folder plugin `users` to PAU.

  >>> content_type, content = encodeMultipartFormdata([
  ...     ('field.prefix', 'users'),
  ...     ('UPDATE_SUBMIT', 'Add'),
  ...     ('add_input_name', 'users')])
  >>> print(http(b"""
  ... POST /++etc++site/default/PAU/+/AddPrincipalFolder.html%%3D HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Content-Type: %b
  ... Cookie: zope3_cs_6a553b3=-j7C3CdeW9sUK8BP5x97u2d9o242xMJDzJd8HCQ5AAi9xeFcGTFkAs
  ... Referer: http://localhost/++etc++site/default/PAU/+/AddPrincipalFolder.html=
  ...
  ... %b
  ... """ % (content_type, content)))
  HTTP/1.1 303 See Other
  ...

Next we will add some users.

  >>> content_type, content = encodeMultipartFormdata([
  ...     ('field.login', 'bob'),
  ...     ('field.passwordManagerName', 'Plain Text'),
  ...     ('field.password', '123'),
  ...     ('field.title', 'Bob'),
  ...     ('field.description', ''),
  ...     ('UPDATE_SUBMIT', 'Add'),
  ...     ('add_input_name', '')])
  >>> print(http(b"""
  ... POST /++etc++site/default/PAU/users/+/AddPrincipalInformation.html%%3D HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Content-Type: %b
  ... Cookie: zope3_cs_6a553b3=-j7C3CdeW9sUK8BP5x97u2d9o242xMJDzJd8HCQ5AAi9xeFcGTFkAs
  ... Referer: http://localhost/++etc++site/default/PAU/users/+/AddPrincipalInformation.html%%3D
  ...
  ... %b
  ... """ % (content_type, content), handle_errors=False))
  HTTP/1.1 303 See Other
  ...

  >>> content_type, content = encodeMultipartFormdata([
  ...     ('field.login', 'bill'),
  ...     ('field.passwordManagerName', 'Plain Text'),
  ...     ('field.password', '123'),
  ...     ('field.title', 'Bill'),
  ...     ('field.description', ''),
  ...     ('UPDATE_SUBMIT', 'Add'),
  ...     ('add_input_name', '')])
  >>> print(http(b"""
  ... POST /++etc++site/default/PAU/users/+/AddPrincipalInformation.html%%3D HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Content-Type: %b
  ... Cookie: zope3_cs_6a553b3=-j7C3CdeW9sUK8BP5x97u2d9o242xMJDzJd8HCQ5AAi9xeFcGTFkAs
  ... Referer: http://localhost/++etc++site/default/PAU/users/+/AddPrincipalInformation.html%%3D
  ...
  ... %b
  ... """ % (content_type, content)))
  HTTP/1.1 303 See Other
  ...


  >>> content_type, content = encodeMultipartFormdata([
  ...     ('field.login', 'joe'),
  ...     ('field.passwordManagerName', 'Plain Text'),
  ...     ('field.password', '123'),
  ...     ('field.title', 'Joe'),
  ...     ('field.description', ''),
  ...     ('UPDATE_SUBMIT', 'Add'),
  ...     ('add_input_name', '')])
  >>> print(http(b"""
  ... POST /++etc++site/default/PAU/users/+/AddPrincipalInformation.html%%3D HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Content-Type: %b
  ... Cookie: zope3_cs_6a553b3=-j7C3CdeW9sUK8BP5x97u2d9o242xMJDzJd8HCQ5AAi9xeFcGTFkAs
  ... Referer: http://localhost/++etc++site/default/PAU/users/+/AddPrincipalInformation.html%%3D
  ...
  ... %b
  ... """ % (content_type, content)))
  HTTP/1.1 303 See Other
  ...


  >>> content_type, content = encodeMultipartFormdata([
  ...     ('field.login', 'sally'),
  ...     ('field.passwordManagerName', 'Plain Text'),
  ...     ('field.password', '123'),
  ...     ('field.title', 'Sally'),
  ...     ('field.description', ''),
  ...     ('UPDATE_SUBMIT', 'Add'),
  ...     ('add_input_name', '')])
  >>> print(http(b"""
  ... POST /++etc++site/default/PAU/users/+/AddPrincipalInformation.html%%3D HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Content-Type: %b
  ... Cookie: zope3_cs_6a553b3=-j7C3CdeW9sUK8BP5x97u2d9o242xMJDzJd8HCQ5AAi9xeFcGTFkAs
  ... Referer: http://localhost/++etc++site/default/PAU/users/+/AddPrincipalInformation.html%%3D
  ...
  ... %b
  ... """ % (content_type, content)))
  HTTP/1.1 303 See Other
  ...

  >>> content_type, content = encodeMultipartFormdata([
  ...     ('field.login', 'betty'),
  ...     ('field.passwordManagerName', 'Plain Text'),
  ...     ('field.password', '123'),
  ...     ('field.title', 'Betty'),
  ...     ('field.description', ''),
  ...     ('UPDATE_SUBMIT', 'Add'),
  ...     ('add_input_name', '')])
  >>> print(http(b"""
  ... POST /++etc++site/default/PAU/users/+/AddPrincipalInformation.html%%3D HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Content-Type: %b
  ... Cookie: zope3_cs_6a553b3=-j7C3CdeW9sUK8BP5x97u2d9o242xMJDzJd8HCQ5AAi9xeFcGTFkAs
  ... Referer: http://localhost/++etc++site/default/PAU/users/+/AddPrincipalInformation.html%%3D
  ...
  ... %b
  ... """ % (content_type, content)))
  HTTP/1.1 303 See Other
  ...

  >>> content_type, content = encodeMultipartFormdata([
  ...     ('field.login', 'mary'),
  ...     ('field.passwordManagerName', 'Plain Text'),
  ...     ('field.password', '123'),
  ...     ('field.title', 'Mary'),
  ...     ('field.description', ''),
  ...     ('UPDATE_SUBMIT', 'Add'),
  ...     ('add_input_name', '')])
  >>> print(http(b"""
  ... POST /++etc++site/default/PAU/users/+/AddPrincipalInformation.html%%3D HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Content-Type: %b
  ... Cookie: zope3_cs_6a553b3=-j7C3CdeW9sUK8BP5x97u2d9o242xMJDzJd8HCQ5AAi9xeFcGTFkAs
  ... Referer: http://localhost/++etc++site/default/PAU/users/+/AddPrincipalInformation.html%%3D
  ...
  ... %b
  ... """ % (content_type, content)))
  HTTP/1.1 303 See Other
  ...

  >>> content_type, content = encodeMultipartFormdata([
  ...     ('field.login', 'mike'),
  ...     ('field.passwordManagerName', 'Plain Text'),
  ...     ('field.password', '123'),
  ...     ('field.title', 'Mike'),
  ...     ('field.description', ''),
  ...     ('UPDATE_SUBMIT', 'Add'),
  ...     ('add_input_name', '')])
  >>> print(http(b"""
  ... POST /++etc++site/default/PAU/users/+/AddPrincipalInformation.html%%3D HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Content-Type: %b
  ... Cookie: zope3_cs_6a553b3=-j7C3CdeW9sUK8BP5x97u2d9o242xMJDzJd8HCQ5AAi9xeFcGTFkAs
  ... Referer: http://localhost/++etc++site/default/PAU/users/+/AddPrincipalInformation.html%%3D
  ...
  ... %b
  ... """ % (content_type, content)))
  HTTP/1.1 303 See Other
  ...

Next, We'll add out group folder plugin in PAU.

  >>> content_type, content = encodeMultipartFormdata([
  ...     ('field.prefix', 'groups'),
  ...     ('UPDATE_SUBMIT', 'Add'),
  ...     ('add_input_name', 'groups')])
  >>> print(http(b"""
  ... POST /++etc++site/default/PAU/+/AddGroupFolder.html%%3D HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Content-Type: %b
  ... Referer: http://localhost/++etc++site/default/PAU/+/AddGroupFolder.html=
  ...
  ... %b
  ... """ % (content_type, content)))
  HTTP/1.1 303 See Other
  ...


Next we'll select the credentials and authenticators for the PAU:

  >>> content_type, content = encodeMultipartFormdata([
  ...     ('field.credentialsPlugins.to', 'U2Vzc2lvbiBDcmVkZW50aWFscw=='),
  ...     ('field.credentialsPlugins-empty-marker', ''),
  ...     ('field.authenticatorPlugins.to', 'dXNlcnM='),
  ...     ('field.authenticatorPlugins.to', 'Z3JvdXBz'),
  ...     ('field.authenticatorPlugins-empty-marker', ''),
  ...     ('UPDATE_SUBMIT', 'Change'),
  ...     ('field.credentialsPlugins', 'U2Vzc2lvbiBDcmVkZW50aWFscw=='),
  ...     ('field.authenticatorPlugins', 'dXNlcnM='),
  ...     ('field.authenticatorPlugins', 'Z3JvdXBz')])
  >>> print(http(b"""
  ... POST /++etc++site/default/PAU/@@configure.html HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Content-Type: %b
  ... Referer: http://localhost/++etc++site/default/PAU/@@configure.html
  ...
  ... %b
  ... """ % (content_type, content)))
  HTTP/1.1 200 Ok
  ...



Now, we can define some groups.  Let's start with a group named "Admin":

  >>> content_type, content = encodeMultipartFormdata([
  ...     ('field.title', 'Admin'),
  ...     ('field.description', ''),
  ...     ('UPDATE_SUBMIT', 'Add'),
  ...     ('add_input_name', 'admin')])
  >>> print(http(b"""
  ... POST /++etc++site/default/PAU/groups/+/AddGroupInformation.html%%3D HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Content-Type: %b
  ... Referer: http://localhost/++etc++site/default/PAU/groups/+/AddGroupInformation.html=
  ...
  ... %b
  ... """ % (content_type, content)))
  HTTP/1.1 303 See Other
  ...


That includes Betty, Mary and Mike:

  >>> content_type, content = encodeMultipartFormdata([
  ...     ('field.title', 'Admin'),
  ...     ('field.description', ''),
  ...     ('field.principals.displayed', 'y'),
  ...     ('field.principals.MC51c2Vycw__.query.field.search', ''),
  ...     ('field.principals:list', 'dXNlcnMz'),
  ...     ('field.principals:list', 'dXNlcnM3'),
  ...     ('field.principals:list', 'dXNlcnM2'),
  ...     ('field.principals.MC51c2Vycw__.apply', 'Apply'),
  ...     ('field.principals.MC5ncm91cHM_.query.field.search', ''),
  ...     ('field.principals.users6.query.field.search', ''),
  ...     ('field.principals.MQ__.query.searchstring', 'Apply')])
  >>> print(http(b"""
  ... POST /++etc++site/default/PAU/groups/admin/@@edit.html HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Content-Type: %b
  ... Referer: http://localhost/++etc++site/default/PAU/groups/admin/@@edit.html
  ...
  ... %b
  ... """ % (content_type, content), handle_errors=False))
  HTTP/1.1 200 Ok
  ...


and a group "Power Users"

  >>> content_type, content = encodeMultipartFormdata([
  ...     ('field.title', 'Power Users'),
  ...     ('field.description', ''),
  ...     ('UPDATE_SUBMIT', 'Add'),
  ...     ('add_input_name', 'power')])
  >>> print(http(b"""
  ... POST /++etc++site/default/PAU/groups/+/AddGroupInformation.html%%3D HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Content-Type: %b
  ... Referer: http://localhost/++etc++site/default/PAU/groups/+/AddGroupInformation.html=
  ...
  ... %b
  ... """ % (content_type, content)))
  HTTP/1.1 303 See Other
  ...

with Bill and Betty as members:

  >>> content_type, content = encodeMultipartFormdata([
  ...     ('field.title', 'Power Users'),
  ...     ('field.description', ''),
  ...     ('field.principals:list', 'dXNlcnMz'),
  ...     ('field.principals:list', 'dXNlcnMy'),
  ...     ('field.principals.displayed', 'y'),
  ...     ('field.principals.MC51c2Vycw__.query.field.search', ''),
  ...     ('field.principals.MC5ncm91cHM_.query.field.search', ''),
  ...     ('field.principals.MQ__.query.searchstring', ''),
  ...     ('UPDATE_SUBMIT', 'Change')])
  >>> print(http(b"""
  ... POST /++etc++site/default/PAU/groups/power/@@edit.html HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Content-Type: %b
  ... Referer: http://localhost/++etc++site/default/PAU/groups/power/@@edit.html
  ...
  ... %b
  ... """ % (content_type, content)))
  HTTP/1.1 200 Ok
  ...

Now, with these groups set up, we should see these groups on the
affected principals.  First, we'll make the root folder the
thread-local site:

  >>> from zope.component.hooks import setSite
  >>> setSite(getRootFolder())

and we'll get the pluggable authentication utility:

  >>> from zope.authentication.interfaces import IAuthentication
  >>> from zope.component import getUtility
  >>> principals = getUtility(IAuthentication)

Finally we'll get Betty and see that she is in the admin and
power-user groups:

  >>> betty = principals.getPrincipal(u'users3')
  >>> betty.groups.sort()
  >>> betty.groups
  ['groupspower', 'zope.Authenticated', 'zope.Everybody']


And we'll get Bill, and see that he is only in the power-user group:

  >>> bill = principals.getPrincipal(u'users2')
  >>> bill.groups
  ['zope.Everybody', 'zope.Authenticated', 'groupspower']
