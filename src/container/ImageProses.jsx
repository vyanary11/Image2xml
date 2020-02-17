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

import ImageDetail from '../component/ImageDetail';

 
export default class ImageProses extends React.Component {
   
    constructor(props) {
       super(props);
 
       this.state = {
            hasNavigationButton:false,
            hasFloatingnButton:false, 
            image_object: null,
            image_object_details: {},
            status_proses: false
       }
   }
 
   updateImageObject(e) {
       const file  = e.target.files[0];
       const reader = new FileReader();
      
       reader.readAsDataURL(file);
       reader.onload = () => {
           this.setState({
                hasNavigationButton:false,
                hasFloatingnButton:false,
                image_object: reader.result, 
                image_object_details: null, 
                status_proses: false
            });
       };
 
   }
 
    getDataFromServer() {

        this.setState({status_proses: true, image_object_details:null}, () => {
 
            api("detect_image_objects", this.state.image_object).then((response) => {
                this.setState({
                    hasNavigationButton     : response.hasNavigationButton,
                    hasFloatingnButton      : response.hasFloatingnButton,
                    image_object_details    : response.data 
                });
            });
        
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
                                <Grid item xs={6}>
                                    <Card>
                                        <CardHeader title="Image" />
                                        <CardContent>
                                            <Grid container spacing={2} justify="center">
                                                <Grid item>
                                                    <Button variant="contained" component='label'>
                                                        Upload Image
                                                        <input accept="image/png,image/jpeg" onChange={(e) =>  this.updateImageObject(e)} type="file" style={{ display: 'none' }} />
                                                    </Button>
                                                </Grid>
                                                {this.state.image_object && <Grid item>
                                                    <Button onClick={() => this.getDataFromServer()} variant="contained" color="primary">
                                                        Prosess
                                                    </Button>
                                                </Grid>}
                                                <Grid item xs={12}>
                                                    {this.state.image_object &&
                                                        <img src={this.state.image_object} alt="" height="600px"/>
                                                    }
                                                </Grid>
                                            </Grid>
                                        </CardContent>
                                    </Card>
                                </Grid>    
                                {this.state.status_proses && this.state.image_object_details &&
                                    <Grid item xs={6}>
                                        <Card>
                                            <CardHeader title="Result" />
                                            <CardContent>
                                                <ImageDetail data = {this.state.image_object_details} hasNavigationButton = {this.state.hasNavigationButton} hasFloatingnButton = {this.state.hasFloatingnButton}></ImageDetail>
                                            </CardContent>
                                        </Card>
                                    </Grid>
                                }
                                {this.state.status_proses && !this.state.image_object_details &&
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
                            </Grid>
                        </Container>
                    </div>
                </main>
            </div>
        )
    }
} 