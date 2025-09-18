from flask import Flask
app = Flask (__name__)

@app.route("/")
def start ():
    return """<!doctype html>
        <!html>
             <body>
                 <hl>web-сервер на flask</hl>
             </body>
        <!html>"""
