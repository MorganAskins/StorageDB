import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash_database import DashDatabase
from .SDBTab import SDBTab

class ViewTab( SDBTab ):
    def __init__(self, app, db):
        name="Viewport"
        SDBTab.__init__(self, name, app, db)
        self.setup()

    def setup(self):
        children = []
        # Search Box
        children.append(
                dcc.Input( placeholder="<filter value>", id="filter" )
                )

        # Button
        children.append(
                html.Button(children="Show me the value", id="show_value_button")
                )
        
        # Output
        children.append(
                dcc.Markdown(id="show_value_div")
                )
        self.children = children

    def update(self, session_id, query=None):
        ret_string = '| key | value |\n'
        ret_string += '| :-- | :-- |\n'
        for key in self.db.list_stored_user_keys(user_id = session_id):
            value = self.db.get_user_value(user_id = session_id, key_name=key)
            if query is not None:
                if query in value:
                    ret_string += f'|{key}|{value}|\n'
            else:
                ret_string += f'|{key}|{value}|\n'

        return ret_string

    def create_callbacks(self, app:dash.Dash, db:DashDatabase):
        # Update on button press
        @app.callback( Output('show_value_div', 'children'),
                [Input('show_value_button', 'n_clicks'), Input('filter', 'value')],
                [State('session_id_div_id', 'data')])
        def retrieve_value(n_clicks, query, session_id):
            # Loop over all stored keys, as string for now md table
            # if n_clicks is None:
            #     raise PreventUpdate
            return self.update(session_id, query)
