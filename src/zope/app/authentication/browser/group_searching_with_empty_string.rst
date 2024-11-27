We can search group folder with an empty string.

We'll add a  pluggable authentication utility:


  >>> print(http(r"""
  ... POST /++etc++site/default/@@contents.html HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Content-Type: application/x-www-form-urlencoded
  ... Referer: http://localhost/++etc++site/default/@@contents.html?type_name=BrowserAdd__zope.pluggableauth.authentication.PluggableAuthentication
  ...
  ... type_name=BrowserAdd__zope.pluggableauth.authentication.PluggableAuthentication&new_value=PAU"""))
  HTTP/1.1 303 See Other
  ...


And register it:

  >>> content_type, content = encodeMultipartFormdata([
  ...    ('field.comment', ''),
  ...    ('field.actions.register', 'Register'),
  ... ])
  >>> print(http(b"""
  ... POST /++etc++site/default/PAU/addRegistration.html HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Content-Type: %b
  ... Referer: http://localhost/++etc++site/default/PAU/addRegistration.html
  ...
  ... %b
  ... """ % (content_type, content)))
  HTTP/1.1 303 See Other
  ...


Next, we'll add the group folder:

  >>> content_type, content = encodeMultipartFormdata([
  ...     ('field.prefix', 'groups'),
  ...     ('UPDATE_SUBMIT', 'Add'),
  ...     ('add_input_name', 'groups'),
  ... ])
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


And add some groups:

  >>> content_type, content = encodeMultipartFormdata([
  ...     ('field.title', 'Test1'),
  ...     ('field.description', ''),
  ...     ('UPDATE_SUBMIT', 'Add'),
  ...     ('add_input_name', 'Test1'),
  ... ])
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

  >>> content_type, content = encodeMultipartFormdata([
  ...     ('field.title', 'Test2'),
  ...     ('field.description', ''),
  ...     ('UPDATE_SUBMIT', 'Add'),
  ...     ('add_input_name', 'Test2'),
  ... ])
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


Now we'll configure our pluggable-authentication utility to use the
group folder:

  >>> content_type, content = encodeMultipartFormdata([
  ...     ('field.credentialsPlugins.to', 'U2Vzc2lvbiBDcmVkZW50aWFscw=='),
  ...     ('field.credentialsPlugins-empty-marker', ''),
  ...     ('field.authenticatorPlugins.to', 'Z3JvdXBz'),
  ...     ('field.authenticatorPlugins-empty-marker', ''),
  ...     ('UPDATE_SUBMIT', 'Change'),
  ...     ('field.credentialsPlugins', 'U2Vzc2lvbiBDcmVkZW50aWFscw=='),
  ...     ('field.authenticatorPlugins', 'Z3JvdXBz'),
  ... ])
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


Now, if we search for a group, but don't supply a string:

  >>> print(http(r"""
  ... POST /@@grant.html HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Content-Type: application/x-www-form-urlencoded
  ... Referer: http://localhost/@@grant.html
  ...
  ... field.principal.displayed=y&"""
  ... "field.principal.MC5ncm91cHM_.field.search=&"
  ... "field.principal.MC5ncm91cHM_.search=Search&"
  ... "field.principal.MQ__.searchstring="))
  HTTP/1.1 200 Ok
  ...Test1...Test2...

We get both of our groups in the result.
