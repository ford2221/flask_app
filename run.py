from my_app import app

#app.config.from_pyfile('config.py')

if __name__ == "__main__":
    app.run() #debug=True , ssl_context='adhoc'
#app.config['debug']=True
#app.debug=True