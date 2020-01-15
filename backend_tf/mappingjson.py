def get(label):
    dataJson={}
    if(label=='toolbar'):
        dataJson = {
            'name'  : 'Toolbar',
            'attrs' :{
                'android:layout_alignParentTop' : 'true',
                'android:id' : '@+id/toolbar',
                'android:layout_width' : 'match_parent',
                'android:layout_height' : '?attr/actionBarSize',
                'android:background' : '?attr/colorPrimary',
                'android:elevation' : '4dp',
                'android:theme' : '@style/ThemeOverlay.AppCompat.ActionBar',
                'android:popupTheme' : '@style/ThemeOverlay.AppCompat.Light',
                'android:title' : 'Toolbar',
                'android:titleTextColor' : '@android:color/white',
            }
        }
    elif(label=='switch'):
        dataJson = {
            'name'  : 'Switch',
            'attrs' :{
                'android:layout_width' : 'wrap_content',
                'android:layout_height' : 'wrap_content',
                'android:text' : 'Switch',
            }
        }
    elif(label=='textView'):
        dataJson = {
            'name'  : 'TextView',
            'attrs' :{
                'android:layout_width' : 'wrap_content',
                'android:layout_height' : 'wrap_content',
                'android:text' : 'TextView',
            }
        }
    elif(label=='slider'):
        dataJson = {
            'name'  : 'SeekBar',
            'attrs' :{
                'style' : '@style/Widget.AppCompat.SeekBar.Discrete',
                'android:layout_width' : 'wrap_content',
                'android:layout_height' : 'wrap_content',
                'android:layout_weight' : '1',
                'android:max' : '10',
                'android:progress' : '3',
            }
        }
    elif(label=='radioButton'):
        dataJson = {
            'name'  : 'RadioButton',
            'attrs' :{
                'android:layout_width' : 'wrap_content',
                'android:layout_height' : 'wrap_content',
                'android:text' : 'RadioButton',
            }
        }
    elif(label=='navigationButton'):
        dataJson = {
            'name'  : 'com.google.android.material.bottomnavigation.BottomNavigationView',
            'attrs' :{
                'android:background' : '?android:attr/windowBackground',
                'android:layout_width' : 'match_parent',
                'android:layout_height' : 'wrap_content',
                'android:layout_alignParentBottom' : 'true',
                'android:elevation' : '20dp',
                'app:labelVisibilityMode' : 'labeled',
                'app:menu' : '@menu/bottomnavigation_menu',
            }
        }
    elif(label=='button'):
        dataJson = {
            'name'  : 'Button',
            'attrs' :{
                'android:layout_width' : 'wrap_content',
                'android:layout_height' : 'wrap_content',
                'android:text' : 'Button',
            }
        }
    elif(label=='checkBox'):
        dataJson = {
            'name'  : 'CheckBox',
            'attrs' :{
                'android:layout_width' : 'wrap_content',
                'android:layout_height' : 'wrap_content',
                'android:text' : 'CheckBox'
            }
        }
    elif(label=='editText'):
        dataJson = {
            'name'      : 'com.google.android.material.textfield.TextInputLayout',
            'attrs'     : {
                'android:layout_width' : 'match_parent',
                'android:layout_height' : 'match_parent',
            },
            'children' : [{
                'name'  : 'com.google.android.material.textfield.TextInputEditText',
                'attrs' :{
                    'android:layout_width' : 'match_parent',
                    'android:layout_height' : 'wrap_content',
                    'android:hint' : 'Edit Text',
                }
            }]
        }
    elif(label=='ratingBar'):
        dataJson = {
            'name'  : 'RatingBar',
            'attrs' :{
                'android:layout_width' : 'wrap_content',
                'android:layout_height' : 'wrap_content',
            }
        }
    elif(label=='floatingButton'):
        dataJson = {
            'name'  : 'com.google.android.material.floatingactionbutton.FloatingActionButton',
            'attrs' :{
                'android:layout_width' : 'wrap_content',
                'android:layout_height' : 'wrap_content',
                'android:layout_alignParentRight' : 'true',
                'android:layout_alignParentBottom' : 'true',
                'android:layout_marginStart' : '20dp',
                'android:layout_marginTop' : '20dp',
                'android:layout_marginEnd' : '20dp',
                'android:layout_marginBottom' : '20dp',
                'android:clickable' : 'true',
                'app:srcCompat' : '@drawable/ic_add_white_24dp',
            }
        }
    elif(label=='linearHorizontal'):
        dataJson = {
            'name'      : 'LinearLayout',
            'attrs'     : {
                'android:layout_width' : 'match_parent',
                'android:layout_height' : 'match_parent',
                'android:orientation' : 'horizontal',
            },
            'children'  : []
        }

    return dataJson