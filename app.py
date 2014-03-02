#!/usr/bin/python2
# coding: utf-8

import requests

from lxml.html.clean import Cleaner
from flask import Flask


app = Flask(__name__)
app.config['DEBUG'] = True

cleaner = Cleaner()
cleaner.javascript = True
cleaner.style = True


@app.route('/view/<path:url>')
def viewpage(url):
    r = requests.get(str(url))
    return cleaner.clean_html(r.content)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
