import React from 'react';

import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';
 
import {bottom_navigation_menu} from '../utils/xml_extras';
import {icon_drawable} from '../utils/xml_extras';


import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { tomorrow } from 'react-syntax-highlighter/dist/esm/styles/prism';

import {CopyToClipboard} from 'react-copy-to-clipboard';

import { saveAs } from 'file-saver';
var JSZip = require("jszip");

export default class ImageDetail extends React.Component {
    download(dataxml,hasNavigationButton,hasFloatingButton){
        var zip = new JSZip();
        var res = zip.folder("res");
        var layout = res.folder("layout");
        layout.file("layout_generate.xml", dataxml);

        if(hasNavigationButton===true){
            var menu = res.folder("menu");
            menu.file("bottomnavigation_menu.xml", bottom_navigation_menu());
            var drawable = res.folder("drawable");
            drawable.file("ic_home_black_24dp.xml", icon_drawable("home","#FF000000"));
            drawable.file("ic_search_black_24dp.xml", icon_drawable("search","#FF000000"));
            drawable.file("ic_favorite_black_24dp.xml", icon_drawable("favorite","#FF000000"));
            drawable.file("ic_account_box_black_24dp.xml", icon_drawable("account","#FF000000"));
        }
        if(hasFloatingButton===true){
            var drawable = res.folder("drawable");
            drawable.file("ic_add_white_24dp.xml", icon_drawable("add","#FFFFFFFF"));
        }
        
        zip.generateAsync({type:"blob"}).then(function(content) {
            // see FileSaver.js
            saveAs(content, "res.zip");
        });
    }
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
        console.log(xml);
        const resultXML = {
            textAlign : "left",
        };
        return (
            <div style={resultXML}>
                <Grid container spacing={2} justify="center">
                    <Grid item xs={12}>
                        <Grid container spacing={2} justify="center">
                            <Grid item>
                                <Button variant="contained" color="primary" onClick={() => this.download(xml,this.props.hasNavigationButton,this.props.hasFloatingButton)}>
                                    Download File xml
                                </Button>
                            </Grid>
                            <Grid item>
                                <CopyToClipboard text={xml}>
                                    <Button variant="contained" color="secondary" onClick={() => alert("Copied")}>
                                        Copy To Clipboard
                                    </Button>
                                </CopyToClipboard>
                            </Grid>
                        </Grid>
                    </Grid>    
                    <Grid item xs={12}>
                        <SyntaxHighlighter showLineNumbers={true} language="xml" style={tomorrow}>
                            {xml}
                        </SyntaxHighlighter>
                    </Grid> 
                </Grid>
            </div>
        )
    }
}