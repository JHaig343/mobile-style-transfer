# Mobile Style Transfer
A mobile version of the neural style transfer web application: https://bitbucket.org/jhaig343/styletransferapp/

Front-end development was done using React Native, with Expo(https://expo.io/) used for rapid prototyping on iOS and Android platforms. 

Requests from the frontend go to a separately run Flask server that performs the image stylization (using an imported Tensorflow model from TF Hub) and returns the result.

## Prerequisites:
- Nodejs and NPM: https://nodejs.org
- Expo NPM package: `npm install expo-cli --global`
- Python 3 and pip package manager: https://www.python.org/downloads/
- `pip install -r requirements.txt` to install all of the required Python packages (FLask, Tensorflow, numpy, etc.)
- The Expo client needs to be installed to work on iOS: https://apps.apple.com/ca/app/expo-client/id982107779

## To Run:
### 1. Start the Flask Server
- in the root directory, run `flask run --host=0.0.0.0`
    - NOTE: this listens on every port; requests must be made to the local IP of device running the FLask server. (ex. 10.0.0.220)
### 2. Start the Expo Application
- in the root directory in a separate terminal, run `expo start`
- A web page will open in your default browser that contains a QR code. scan the QR code with your phone Camera and select the pop-up to start the application. 