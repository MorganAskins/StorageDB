import dash
import dash_core_components as dcc
import dash_html_components as html
from dash_database import DashDatabase

class SDBTab:
    def __init__(self, name, app, db):
        self.app = app
        self.db = db
        self.name = name
        self.children = []
    def tab(self):
        return dcc.Tab(label=self.name, children=self.children)
    def update(self, session_id):
        pass
    # Virtual method
    def create_callbacks(self, app:dash.Dash, db:DashDatabase):
        pass
