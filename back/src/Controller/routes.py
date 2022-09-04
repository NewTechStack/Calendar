from Model.calendar import *
from Model.event import *
from Model.sso import *

def setuproute(app, call):
    @app.route('/',                                 ['OPTIONS', 'GET', 'POST'],   lambda x = None: call([])                                                                                         )
    @app.route('/sso',                              ['OPTIONS', 'GET'],           lambda x = None: call([sso_url])                                                                                  )
    @app.route('/sso/conn/<>',                      ['OPTIONS', 'GET'],           lambda x = None: call([sso_token])                                                                                )

    @app.route('/calendars',                        ['OPTIONS', 'GET'],           lambda x = None: call([sso_verify_token, calendar_init, calendar_get])                                            )
    @app.route('/calendar',                         ['OPTIONS', 'POST'],          lambda x = None: call([sso_verify_token, calendar_init, calendar_new])                                            )
    @app.route('/calendar/<>',                      ['OPTIONS', 'GET'],           lambda x = None: call([sso_verify_token, calendar_init, calendar_by_id])                                          )
    @app.route('/calendar/<>',                      ['OPTIONS', 'POST'],          lambda x = None: call([sso_verify_token, calendar_init, calendar_by_id, calendar_update])                         )

    @app.route('/calendar/<>/event',                ['OPTIONS', 'GET'],           lambda x = None: call([sso_verify_token, calendar_init,  calendar_by_id, event_init, event_get])                  )
    @app.route('/calendar/<>/event',                ['OPTIONS', 'POST'],          lambda x = None: call([sso_verify_token, calendar_init,  calendar_by_id, event_init, event_new])                  )
    @app.route('/calendar/<>/event/<>',             ['OPTIONS', 'GET'],           lambda x = None: call([sso_verify_token, calendar_init,  calendar_by_id, event_init, event_by_id])                )
    @app.route('/calendar/<>/event/<>',             ['OPTIONS', 'POST'],          lambda x = None: call([sso_verify_token, calendar_init,  calendar_by_id, event_init, event_by_id, event_update])  )
    @app.route('/calendar/<>/event/<>/confirm',     ['OPTIONS', 'POST'],          lambda x = None: call([sso_verify_token, calendar_init,  calendar_by_id, event_init, event_by_id, event_confirm]) )
    @app.route('/calendar/<>/event/<>/invite',      ['OPTIONS', 'POST'],          lambda x = None: call([sso_verify_token, calendar_init,  calendar_by_id, event_init, event_by_id, event_invite])  )
    def base():
        return
