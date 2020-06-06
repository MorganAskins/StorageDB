import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash_database import DashDatabase
from .SDBTab import SDBTab

class EntryTab( SDBTab ):
    def __init__(self, app, db):
        name="Entry Tab"
        SDBTab.__init__(self, name, app, db)
        self.setup()

    def setup(self):
        children = []
        # Key box
        children.append(
                dcc.Input( placeholder = "<unique_key>", id="new_key_div" )
                )
        
        # Value box
        children.append(
                dcc.Input( placeholder = "<value>", id="new_input_div" )
                )
        
        # old things
        #children.append(
        #        dcc.Input(placeholder = "EV", id="input_div")
        #        )
        children.append(
                html.Button(children="OK", id="ok_button")
                )
        children.append(
                dcc.Markdown(id="success_value_saved")
                )
        self.children = children

    def create_callbacks(self, app:dash.Dash, db:DashDatabase):
        @app.callback( Output('success_value_saved', 'children'),
                [Input('ok_button', 'n_clicks')], # The button triggers the callback
                [State('new_key_div', 'value'),
                 State('new_input_div', 'value'),
                 State('session_id_div_id', 'data')])
        def save_value(n_clicks, key, value, session_id):
            if n_clicks is None:
                raise PreventUpdate
    
            # save vlaue
            db.store_user_value(user_id = session_id, key_name=key, value=value)
    
            return "Value saved"
