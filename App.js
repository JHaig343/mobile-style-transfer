import React from 'react';
import { StyleSheet, Text, View, Button, Image, ScrollView, TouchableOpacity } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import Constants from "expo-constants";
import * as Permissions from 'expo-permissions';

export default class App extends React.Component {
  //FIXME: WTF is this doing??
  state = {
    image1: null,
  };
  
  
  render() {
    let { image, image2, image3 } = this.state;
    
    return (
        <View style={styles.container}>
          <ScrollView showsVerticalScrollIndicator='false'>
            <View>
              <Button color="#0000ff" title="Pick Content Image" onPress={() => this._pickImage('content')} />
            </View>
            <Image source={{uri: 'data:image/jpeg;base64,' + image}} style={{width: 200, height: 200}}/>
            <View>
              <Button color = "#ff0000" title="Pick Style Image" onPress={() => this._pickImage('style')}/>
            </View>
            <Image source={{uri: 'data:image/jpeg;base64,' + image2}} style={{width: 200, height: 200}}/>
            
            <TouchableOpacity onPress={() => this.sendStylizeRequest()} style={styles.button}><Text style={styles.buttonText}>Click to Stylize</Text></TouchableOpacity>
          
            <Image source={{uri: 'data:image/jpeg;base64,' + image3}} style={{width: 200, height: 200}}/>
          </ScrollView>
        </View>
    );  
  }
  
  
  componentDidMount() {
    this.getPermissionsAsync();
  }
  
  //Ask for Camera Roll permissions first before accessing images
  getPermissionsAsync = async() => {
    if (Constants.platform.ios) {
      const {status} = await Permissions.askAsync(Permissions.CAMERA_ROLL);
      if(status !== 'granted') {
        alert("Sorry, we need camera roll permissions to work!");
      }
    }

  };
  //Use fetch() API to send the images to the style transfer model (running on a separate Flask server)
  sendStylizeRequest() {
    let contentImage = this.state.image;
    let styleImage = this.state.image2;
    
    const formData = new FormData();
    //TODO: will probably need to convert these to a file format...
    formData.append('contentImage', contentImage);
    formData.append('styleImage', styleImage);
    formData.append('savename', 'testIOS.png');
    
    console.log(formData);
    // FIXME: request succeeds but server not set up to take format of image data. Pass in URI?
    fetch('http://10.0.0.218:5000/baseImages', {
      method: 'POST',
      body: formData
    }).then(response => response.text())
        .then(result => {
          console.log("Oh looky success!");
          // console.log("Result: " + result);
          this.setState({image3: result });
          console.log("Complete!")
        })
        .catch(error => { console.log('Error: ', error )
        });

  }
  
  _pickImage = async(imageType) => {
    try  {
      let result = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        allowsEditing: true,
        aspect: [4, 3],
        quality: 1,
        base64: true,
        
      });
      if(!result.cancelled) {
        if(imageType === 'content') {
          this.setState({ image: result.base64});
        }
        else if(imageType === 'style') {
          this.setState({ image2: result.base64});
        }
      }
      console.log(result);
      
    } catch(E) {
      console.error("Error: " + E);
    }
  };
  
  
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#ffffff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  button: {
    backgroundColor: "blue",
    padding: 20,
    borderRadius: 5,
    marginTop: 50,
  },
  buttonText: {
    fontSize: 20,
    color: '#ffffff',
  },
});
