from webapp2 import RequestHandler, cached_property
from webapp2_extras import sessions, auth, jinja2


class BaseHandler(RequestHandler):
    """
    Class for handling common tasks
    """
    def dispatch(self):
        try:
            super(BaseHandler, self).dispatch()
        finally:
            self.session_store.save_sessions(self.response)

    @cached_property
    def session_store(self):
        return sessions.get_store(request=self.request)

    @cached_property
    def session(self):
        return self.session_store.get_session()

    @cached_property
    def auth(self):
        return auth.get_auth(request=self.request)

    @cached_property
    def user(self):
        user = self.auth.get_user_by_session()
        return user

    @cached_property
    def user_model(self):
        user_model, timestamp = self.auth.store.user_model.get_by_auth_token(
            self.user['user_id'],
            self.user['token']) if self.user else (None, None)
        return user_model

    @cached_property
    def jinja2(self):
        return jinja2.get_jinja2()

    def render_response(self, _template, **context):
        rv = self.jinja2.render_template(_template, **context)
        self.response.write(rv)


class Index(BaseHandler):
    """
    Index page handler
    """
    def get(self):
        context = {'title': 'Welcome', 'message': 'Hello, world!'}
        self.render_response('index.html', **context)


def handle_404(request, response, exception):
    """
    Function for handling 404 server error
    """
    response.write('Sorry, could not find that')
    response.set_status(404)


def handle_500(request, response, exception):
    """
    Function for handling 500 server error
    """
    response.write('Sorry, server troubles')
    response.set_status(500)
