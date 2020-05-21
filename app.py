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


def convert_binary_to_image(filename, binary):
    fd = open(filename, 'wb')
    fd.write(binary)
    fd.close()


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
        
        convert_binary_to_image('content.png', binary_content)
        convert_binary_to_image('style.png', binary_style)

        draw_image_stylized('content.png', 'style.png', savename='images/' + request.form['savename'])
        # remove the files after
        os.remove('content.png')
        os.remove('style.png')

        with open('images/' + request.form['savename'], 'rb') as image_file:
            encoded_image = base64.b64encode(image_file.read())
        
        return encoded_image
        
        