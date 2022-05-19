from sqlalchemy.exc import DataError

from my_app import app
from flask import render_template


@app.errorhandler(404)
def page_not_found(e):
    return render_template("general/404.html")

@app.errorhandler(Exception)
def error_server(e):
    #print(e)

    #if isinstance(e, DataError):
       # return 'error dataerror'
    return render_template("general/500.html",e=e)