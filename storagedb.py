#!/usr/bin/env python3
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from dash_database import DashDatabase
import uuid

from src import StorageDB

if __name__ == "__main__":
    sdb = StorageDB()
