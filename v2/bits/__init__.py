from pyramid.config import Configurator

from pyramid.session import SignedCookieSessionFactory

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    secret = config.get_settings().get('bits.secret')
    if not secret:
        # thius should never happen in production! aaahhh!
        secret = 'bits_secret'
    httponly = False if config.get_settings().get('bits.header_httponly') == 'false' else True
    secure = False if config.get_settings().get('bits.header_secure') == 'false' else True
    my_session_factory = SignedCookieSessionFactory(
        secret,
        httponly=httponly,
        secure=secure,
    )
    config.set_session_factory(my_session_factory)

    # todo: enable this
    #config.set_default_csrf_options(require_csrf=True)

    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.routes')
    config.scan()
    return config.make_wsgi_app()
