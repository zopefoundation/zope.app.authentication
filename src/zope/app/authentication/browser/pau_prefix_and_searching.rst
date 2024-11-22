================================
Using a PAU Prefix and Searching
================================

This test confirms that both principals and groups can be searched for in
PAUs that have prefixes.

First we'll create a PAU with a prefix of `pau1_` and and register:

  >>> content_type, content = encodeMultipartFormdata([
  ...     ('field.prefix', 'pau1_'),
  ...     ('UPDATE_SUBMIT', 'Add'),
  ...     ('add_input_name', 'PAU1'),
  ... ])
  >>> print(http(b"""
  ... POST /++etc++site/default/+/AddPluggableAuthentication.html%%3D HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Content-Type: %b
  ...
  ... %b
  ... """ % (content_type, content)))
  HTTP/1.1 303 See Other
  ...

  >>> content_type, content = encodeMultipartFormdata([
  ...     ('field.comment', ''),
  ...     ('field.actions.register', 'Register'),
  ... ])
  >>> print(http(b"""
  ... POST /++etc++site/default/PAU1/addRegistration.html HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Content-Type: %b
  ...
  ... %b
  ... """ % (content_type, content)))
  HTTP/1.1 303 See Other
  ...

Next we'll create and register a principal folder:

  >>> content_type, content = encodeMultipartFormdata([
  ...     ('field.prefix', 'users_'),
  ...     ('UPDATE_SUBMIT', 'Add'),
  ...     ('add_input_name', 'Users'),
  ... ])
  >>> print(http(b"""
  ... POST /++etc++site/default/PAU1/+/AddPrincipalFolder.html%%3D HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Content-Type: %b
  ...
  ... %b
  ... """ % (content_type, content)))
  HTTP/1.1 303 See Other
  ...

and add a principal that we'll later search for:

  >>> content_type, content = encodeMultipartFormdata([
  ...     ('field.login', 'bob'),
  ...     ('field.passwordManagerName', 'Plain Text'),
  ...     ('field.password', 'bob'),
  ...     ('field.title', 'Bob'),
  ...     ('field.description', ''),
  ...     ('UPDATE_SUBMIT', 'Add'),
  ...     ('add_input_name', ''),
  ... ])
  >>> print(http(b"""
  ... POST /++etc++site/default/PAU1/Users/+/AddPrincipalInformation.html%%3D HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Content-Type: %b
  ...
  ... %b
  ... """ % (content_type, content)))
  HTTP/1.1 303 See Other
  ...

Next, we'll add and register a group folder:

  >>> content_type, content = encodeMultipartFormdata([
  ...     ('field.prefix', 'groups_'),
  ...     ('UPDATE_SUBMIT', 'Add'),
  ...     ('add_input_name', 'Groups'),
  ... ])
  >>> print(http(b"""
  ... POST /++etc++site/default/PAU1/+/AddGroupFolder.html%%3D HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Content-Type: %b
  ...
  ... %b
  ... """ % (content_type, content)))
  HTTP/1.1 303 See Other
  ...

and add a group to search for:

  >>> content_type, content = encodeMultipartFormdata([
  ...     ('field.title', 'Nice People'),
  ...     ('field.description', ''),
  ...     ('UPDATE_SUBMIT', 'Add'),
  ...     ('add_input_name', 'nice'),
  ... ])
  >>> print(http(b"""
  ... POST /++etc++site/default/PAU1/Groups/+/AddGroupInformation.html%%3D HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Content-Type: %b
  ...
  ... %b
  ... """ % (content_type, content)))
  HTTP/1.1 303 See Other
  ...

Since we're only searching in this test, we won't bother to add anyone to the
group.

Before we search, we need to register the two authenticator plugins with the
PAU:

  >>> content_type, content = encodeMultipartFormdata([
  ...     ('field.credentialsPlugins-empty-marker', ''),
  ...     ('field.authenticatorPlugins.to', 'R3JvdXBz'),
  ...     ('field.authenticatorPlugins.to', 'VXNlcnM='),
  ...     ('field.authenticatorPlugins-empty-marker', ''),
  ...     ('UPDATE_SUBMIT', 'Change'),
  ...     ('field.authenticatorPlugins', 'R3JvdXBz'),
  ...     ('field.authenticatorPlugins', 'VXNlcnM='),
  ... ])
  >>> print(http(b"""
  ... POST /++etc++site/default/PAU1/@@configure.html HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Content-Type: %b
  ...
  ... %b
  ... """ % (content_type, content)))
  HTTP/1.1 200 Ok
  ...

Now we'll use the 'grant' interface of the root folder to search for all of
the available groups:

  >>> print(http(r"""
  ... POST /@@grant.html HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Content-Type: application/x-www-form-urlencoded
  ...
  ... field.principal.displayed=y&"""
  ... "field.principal.MC5Hcm91cHM_.field.search=&"
  ... "field.principal.MC5Hcm91cHM_.search=Search&"
  ... "field.principal.MC5Vc2Vycw__.field.search=&"
  ... "field.principal.MQ__.searchstring="))
  HTTP/1.1 200 Ok
  ...
  <select name="field.principal.MC5Hcm91cHM_.selection">
  <option value="cGF1MV9ncm91cHNfbmljZQ__">Nice People</option>
  </select>
  ...

Note in the results that the dropdown box (i.e. the select element) has the
single group 'Nice People' that we added earlier.

Next, we'll use the same 'grant' interface to search for all of the available
principals:

  >>> print(http(r"""
  ... POST /@@grant.html HTTP/1.1
  ... Authorization: Basic bWdyOm1ncnB3
  ... Content-Type: application/x-www-form-urlencoded
  ...
  ... field.principal.displayed=y&"""
  ... "field.principal.MC5Hcm91cHM_.field.search=&"
  ... "field.principal.MC5Hcm91cHM_.selection=cGF1MV9ncm91cHNfbmljZQ__&"
  ... "field.principal.MC5Vc2Vycw__.field.search=&"
  ... "field.principal.MC5Vc2Vycw__.search=Search&"
  ... "field.principal.MQ__.searchstring="))
  HTTP/1.1 200 Ok
  ...
  <select name="field.principal.MC5Vc2Vycw__.selection">
  <option value="cGF1MV91c2Vyc18x">Bob</option>
  </select>
  ...

Note here the dropdown contains Bob, the principal we added earlier.
