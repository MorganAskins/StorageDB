import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash_database import DashDatabase
import uuid
from .EntryTab import EntryTab
from .ViewTab import ViewTab

class StorageDB:
    """
    Hello world
    """
    def __init__(self):
        # Collection of tabs and their effects
        self.app = dash.Dash()
        self.db  = DashDatabase('./stdata.db')
        # Draw tabs
        self._setup_tabcollection()
        self.layout = self.serve_layout()
        self.app.layout = self.serve_layout
        self.update_tabs()
        self.create_callbacks()
        # And start
        self.app.run_server(debug = True, host='0.0.0.0')

    def _setup_tabcollection(self):
        tab_collection = []
        # Create a tab to enter a value
        tab_collection.append( EntryTab(self.app, self.db) )
        # Create a tab to retrieve the value entered in the other tab
        tab_collection.append( ViewTab(self.app, self.db) )
        self.tab_collection = tab_collection

    def update_tabs(self):
        for t in self.tab_collection:
            t.update(self.session_id)

    def serve_layout(self):
        """Creates the layout for each user of the app.
        This function is executed each time a session is created for the app.
        It creates a new session id (a uuid.uuid1 as string) each time.
    
        This session id will be used in combination with DashDatabase
    
        Tabs should be:
        Box list w/ search :=> Click opens the box in a modal to edit and view
        Add new box with list of items.
        """
    
        # Create a session id
        self.session_id = str(uuid.uuid1())
    
        # Store the session id in a dcc.Store component
        store_session_id_div = dcc.Store( id='session_id_div_id',
                storage_type = 'session', data=self.session_id )

        tabview = [t.tab() for t in self.tab_collection]
        # Assemble tabs
        self.tabs = dcc.Tabs(children=tabview)

    
        # Create layout
        layout = html.Div(children=[self.tabs, store_session_id_div])
    
        return layout

    def create_callbacks(self):
        for tab in self.tab_collection:
            tab.create_callbacks(self.app, self.db)
