http://www.zope.org/Collectors/Zope3-dev/663
============================================

Two plugins(basic-auth and session credentials) link
on PAU add menu are broken and can't add them.

For IPluggableAuthentication, "plugins.html" is a correct
view name but "contents.html" is used.

because menu implementation supporsing that all view
uses "zope.app.container.browser.contents.Contents" are
named "contents.html".

In Zope3.2, PluggableAuthentication inherits
SiteManagementFolder that provides "contents.html" view.

    >>> from zope.testbrowser.wsgi import Browser
    >>> browser = Browser()

Create a pau

    >>> browser.addHeader('Authorization', 'Basic mgr:mgrpw')
    >>> browser.open('http://localhost/@@contents.html')
    >>> browser.getLink('Pluggable Authentication Utility').click()
    >>> browser.getControl(name='add_input_name').value = 'auth'
    >>> browser.getControl('Add').click()
    >>> browser.getLink('auth').click()

Go to the plugins view

    >>> browser.getLink('Plugins').click()

Add aa basic auth plugin

    >>> browser.getLink('HTTP Basic-Auth Plugin').click()
    >>> browser.getControl(name='new_value').value = 'basic'
    >>> browser.getControl('Apply').click()

Add a session-credential plugin

    >>> browser.getLink('Session Credentials Plugin').click()
    >>> browser.getControl(name='new_value').value = 'session'
    >>> browser.getControl('Apply').click()

Make sure we can use them:

    >>> browser.getLink('Configure').click()
    >>> browser.getControl(name='field.credentialsPlugins.from').value = [
    ...     'Wm9wZSBSZWFsbSBCYXNpYy1BdXRo']
    >>> browser.getControl(name='field.credentialsPlugins.from').value = [
    ...     'YmFzaWM=']
    >>> browser.getControl(name='field.credentialsPlugins.from').value = [
    ...     'U2Vzc2lvbiBDcmVkZW50aWFscw==']
    >>> browser.getControl('Change').click()
