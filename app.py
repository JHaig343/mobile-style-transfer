import json
import os
from flask import Flask
from flask import send_file
from flask import render_template
from flask import request
from binascii import a2b_base64
import base64

from arbitrarystyle import draw_image_stylized
app = Flask(__name__)


@app.route('/', methods=['GET'])
def send_homepage():
    return render_template('index.html')


# given to filenames, draw the 'content' image in the style of the 'style' image
# For testing purposes; use with HTTP client (ex. Postman)
@app.route('/styletransfer', methods=['POST'])
def stylize():
    savename = "images/flaskimage.png" 
    draw_image_stylized("images/webster.jpg", "images/orphism.jpg", savename=savename)
    
    return send_file(savename, mimetype='image/png')


@app.route('/testjson', methods=['GET'])
def testJSONResponse():
    return json.dumps({'foo': 'bar'})


# Upload and generate images here
@app.route('/baseImages', methods=['POST'])
def upload_and_generate():
    print("Test Test")
    if request.method == 'POST':
        print("in the IF")
        print(request)
        content_image = request.form['contentImage']
        style_image = request.form['styleImage']
        binary_content = a2b_base64(content_image)
        binary_style = a2b_base64(style_image)
        # TODO: break this up into a separate function
        fd = open('content.png', 'wb')
        fd.write(binary_content)
        fd.close()
        fd = open('style.png', 'wb')
        fd.write(binary_style)
        fd.close()

        draw_image_stylized('content.png', 'style.png', savename='images/' + request.form['savename'])
        # # remove the files after
        os.remove('content.png')
        os.remove('style.png')

        with open('images/' + request.form['savename'], 'rb') as image_file:
            encoded_image = base64.b64encode(image_file.read())
        
        return encoded_image
        # TODO: convert new image to base64 and send back to client
        # return send_file('images/' + request.form['savename'], mimetype='image/png')