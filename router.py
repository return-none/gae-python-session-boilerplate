from webapp2 import WSGIApplication, Route
from controller import Index, handle_404, handle_500
from models import User

config = {
    'webapp2_extras.sessions': {
        'secret_key': 'super-secret-key',
    },
    'webapp2_extras.auth': {
        'user_model': User,
    },
    'webapp2_extras.jinja2': {
        'template_path': 'views',
    }
}

routes = [
          Route('/', Index),
          ]

app = WSGIApplication(
                      routes=routes,
                      config=config,
                      debug=True
                      )

app.error_handlers[404] = handle_404
app.error_handlers[500] = handle_500
