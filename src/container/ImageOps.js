import React from 'react';

import Container from '@material-ui/core/Container';
import Grid from '@material-ui/core/Grid';
 
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import CardHeader from '@material-ui/core/CardHeader';
import CssBaseline from '@material-ui/core/CssBaseline';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
 
import {api} from '../utils/Api';

import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import CircularProgress from '@material-ui/core/CircularProgress';

import XMLViewer from 'react-xml-viewer'
 
export default class ImageOps extends React.Component {
   
    constructor(props) {
       super(props);
 
       this.state = {
           image_object: null,
           image_object_details: {},
           active_type: null
       }
   }
 
   updateImageObject(e) {
       const file  = e.target.files[0];
       const reader = new FileReader();
      
       reader.readAsDataURL(file);
       reader.onload = () => {
           this.setState({image_object: reader.result, image_object_details: {}, active_type: null});
       };
 
   }
 
   processImageObject(type) {
 
       this.setState({active_type: type}, () => {
 
           if(!this.state.image_object_details[this.state.active_type]) {
               api("detect_image_objects", this.state.image_object).then((response) => {
                  
                   const filtered_data = response;
                   const image_details = this.state.image_object_details;
      
                   image_details[filtered_data.type] = filtered_data.data;

                   this.setState({image_object_details: image_details });
               });
           }
       });
   }
 
    render() {
        const heroContent = {
            marginTop: "20px"
        };
        return (
            <div>
                <CssBaseline />
                <AppBar position="relative">
                    <Toolbar>
                        <Typography variant="h6">
                            Image2XML
                        </Typography>
                    </Toolbar>
                </AppBar>
                <main>
                    <div style={heroContent}>
                        <Container maxWidth="xl">
                            <Grid container spacing={3} justify="center">
                                {this.state.image_object &&
                                    <Grid item xs={6}>
                                        <Card>
                                            <CardHeader title="Image" />
                                            <CardContent>
                                                <img src={this.state.image_object} alt="" height="450px"/>
                                            </CardContent>
                                        </Card>
                                    </Grid>    
                                }
                                {this.state.active_type && this.state.image_object_details[this.state.active_type] &&
                                    <Grid item xs={6}>
                                        <Card>
                                            <CardHeader title="Result" />
                                            <CardContent>
                                                <ImageDetails type={this.state.active_type} data = {this.state.image_object_details[this.state.active_type]}></ImageDetails>
                                            </CardContent>
                                        </Card>
                                    </Grid>
                                }
                                {this.state.active_type && !this.state.image_object_details[this.state.active_type] &&
                                    <Grid item xs={6}>
                                        <Card>
                                            <CardHeader title="Loading....." />
                                            <CardContent>
                                                <CircularProgress
                                                    color="secondary"
                                                />
                                            </CardContent>
                                        </Card>        
                                    </Grid>
                                }  
                                <Grid item xs={12}>
                                    <Card>
                                        <CardContent>
                                            <Grid container spacing={2} justify="center">
                                                <Grid item>
                                                    <Button variant="contained" component='label'>
                                                        Upload Image
                                                        <input accept="image/png,image/jpeg" onChange={(e) =>  this.updateImageObject(e)} type="file" style={{ display: 'none' }} />
                                                    </Button>
                                                </Grid>
                                                {this.state.image_object && <Grid item>
                                                    <Button onClick={() => this.processImageObject('test')} variant="contained" color="primary">
                                                        Prosess
                                                    </Button>
                                                </Grid>}
                                            </Grid>
                                        </CardContent>
                                    </Card>
                                </Grid>  
                            </Grid>
                        </Container>
                    </div>
                </main>
            </div>
        )
    }
}
 
class ImageDetails extends React.Component {
  
    render() {
        var jsonxml = require('jsontoxml');
        var xml = jsonxml([{
            name    : 'RelativeLayout',
            attrs   : {
                'xmlns:android' : "http://schemas.android.com/apk/res/android",
                'xmlns:app' : "http://schemas.android.com/apk/res-auto",
                'xmlns:tools' : "http://schemas.android.com/tools",
                'android:layout_width' : "match_parent",
                'android:layout_height' : "match_parent",
            },
            children: this.props.data
        }],{xmlHeader:true, prettyPrint:true});
        console.log(this.props.data);
        console.log(xml);
        const resultXML = {
            textAlign : "left",
            whiteSpace: "pre-wrap"
        };
        return (
            <div style={resultXML}>
                <Grid container spacing={2} justify="center">
                    <Grid item xs={12}>
                        <XMLViewer xml={xml} indentSize={4} />
                    </Grid>
                    <Grid item xs={12}>
                        <Button variant="contained" color="primary" onClick={() => alert('Downloding.....')}>
                            Download File xml
                        </Button>
                    </Grid>    
                </Grid>
            </div>
        )
    }
}
 