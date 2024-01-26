# Project Cheat Sheet

## `/meta`

### `views.py`

#### `home(request)`

Directs the user to the home page, called when logo is clicked on website

#### `is_alum(user)`

Returns `True` if the given user profile is an alum, otherwise, `False`

#### `is_student(user)`

Returns `True` if the given user profile is a student, otherwise, `False`

#### `no_access(request)`

Directs alum to `noaccess` if the alum cannot make the given request

#### `no_access_alumni(request)`

Directs user to `/noaccessalumni` if the user cannot make the given request

#### `return_my_requests(request)`

Directs student to `/viewmyrequests` and collects their requests

#### `return_form_data(request)`

Directs alum to `/viewrequests` and collects unanswered requests

# Django Cheat Sheet

### [render(request, template_name)](https://docs.djangoproject.com/en/5.0/topics/http/shortcuts/#render)

Combines a given template with a given context dictionary and returns an HttpResponse object with that rendered text. Directs user to page of HttpResponse.

## [HttpRequest](https://docs.djangoproject.com/en/4.2/ref/request-response/#httprequest-objects)

Object representing an HTTP request.

## [HttpResponse](https://docs.djangoproject.com/en/4.2/ref/request-response/#httprequest-objects)

Object representing an HTTP response from a server.

## [QuerySet](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#queryset-api)

Object representing a set of objects found in a query by some term.

### [`.filter(*args)`](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#filter)

Returns a new QuerySet containing objects that match the given lookup parameters.

### [`.exists()`](https://docs.djangoproject.com/en/5.0/ref/models/querysets/#exists)

Returns `True` if the QuerySet contains any results, and `False` if not. This tries to perform the query in the simplest and fastest way possible, but it does execute nearly the same query as a normal QuerySet query.

## Decorators

### [@never_cache](https://docs.djangoproject.com/en/5.0/topics/http/decorators/#django.views.decorators.cache.never_cache)

This decorator adds an Expires header to the current date/time, a Cache-Control: `max-age=0`, `no-cache`, `no-store`, `must-revalidate`, private header to a response to indicate that a page should never be cached. Each header is only added if it isn’t already set.

### [@user_passes_test(test, login_url)](https://docs.djangoproject.com/en/5.0/topics/auth/default/#django.contrib.auth.decorators.user_passes_test)

Take a boolean function to test if the user is allowed to view the page. If the function returns `False` the user is redirected to `login_url`
