The Query View for Schema Search Plugins
========================================

Placefull setup for making the search plugin IPhysicallyLocatable::

  >>> from zope.component import provideAdapter
  >>> from zope.schema.interfaces import ITextLine
  >>> from zope.publisher.interfaces.browser import IDefaultBrowserLayer
  >>> from zope.formlib.interfaces import IInputWidget
  >>> from zope.formlib.widgets import TextWidget
  >>> from zope.app.authentication.tests import placefulSetUp, placefulTearDown
  >>> site = placefulSetUp(True)
  >>> provideAdapter(TextWidget, (ITextLine, IDefaultBrowserLayer),
  ... IInputWidget)

If a plugin supports `IQuerySchemaSearch`::

  >>> from zope.interface import Interface
  >>> import zope.schema
  >>> class ISearchCriteria(Interface):
  ...     search = zope.schema.TextLine(title=u"Search String")

  >>> from zope.interface import implements
  >>> class MySearchPlugin:
  ...     __name__ = 'searchplugin'
  ...     __parent__ = site
  ...     schema = ISearchCriteria
  ...     data = ['foo', 'bar', 'blah']
  ...
  ...     def get(self, id):
  ...         if id in self.data:
  ...             return {}
  ...
  ...     def search(self, query, start=None, batch_size=None):
  ...         search = query.get('search')
  ...         if search is not None:
  ...             i = 0
  ...             n = 0
  ...             for value in self.data:
  ...                 if search in value:
  ...                     if not ((start is not None and i < start)
  ...                             or
  ...                             (batch_size is not None and n > batch_size)):
  ...                         yield value

then we can get a view::

  >>> from zope.app.authentication.browser.schemasearch \
  ...     import QuerySchemaSearchView
  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> view = QuerySchemaSearchView(MySearchPlugin(), request)

This allows us to render a search form::

  >>> print(view.render('test')) # doctest: +NORMALIZE_WHITESPACE
  <h4>searchplugin</h4>
  <div class="row">
    <div class="label">
      <label for="searchplugin" title="Path to the source utility">
        Source path
      </label>
    </div>
    <div class="field">
        /searchplugin
    </div>
  </div>
  <div class="row">
    <div class="label">
      <label for="test.field.search" title="">
        Search String
      </label>
    </div>
    <div class="field">
      <input class="textType" id="test.field.search" name="test.field.search"
         size="20" type="text" value=""  />
    </div>
  </div>
  <div class="row">
    <div class="field">
      <input type="submit" name="test.search" value="Search" />
    </div>
  </div>

If we ask for results::

  >>> view.results('test')

We don't get any, since we did not provide any. But if we give input::

  >>> request.form['test.field.search'] = 'a'

we still don't get any::

  >>> view.results('test')

because we did not press the button. So let's press the button::

  >>> request.form['test.search'] = 'Search'

so that we now get results (!)::

  >>> list(view.results('test'))
  ['bar', 'blah']

  >>> placefulTearDown()
