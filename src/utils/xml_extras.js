export function bottom_navigation_menu (){
    var code = '<?xml version="1.0" encoding="utf-8"?>\n<menu xmlns:android="http://schemas.android.com/apk/res/android">\n    <item\n         android:id="@+id/home_menu"\n            android:title="Home"\n            android:icon="@drawable/ic_home_black_24dp"/>\n        <item\n            android:id="@+id/search_menu"\n            android:title="Search"\n            android:icon="@drawable/ic_search_black_24dp"/>\n        <item\n            android:id="@+id/favorite_menu"\n            android:title="Favorite"\n            android:icon="@drawable/ic_favorite_black_24dp"/>\n        <item\n            android:id="@+id/account_menu"\n            android:title="Account"\n            android:icon="@drawable/ic_account_box_black_24dp"/>\n    </menu>';
    return code;
}

export function icon_drawable (icon,color){
    var pathData;
    if (icon==="home") {
        pathData = "M10,20v-6h4v6h5v-8h3L12,3 2,12h3v8z";
    }else if(icon==="search"){
        pathData = "M15.5,14h-0.79l-0.28,-0.27C15.41,12.59 16,11.11 16,9.5 16,5.91 13.09,3 9.5,3S3,5.91 3,9.5 5.91,16 9.5,16c1.61,0 3.09,-0.59 4.23,-1.57l0.27,0.28v0.79l5,4.99L20.49,19l-4.99,-5zM9.5,14C7.01,14 5,11.99 5,9.5S7.01,5 9.5,5 14,7.01 14,9.5 11.99,14 9.5,14z";
    }else if(icon==="favorite"){
        pathData = "M12,21.35l-1.45,-1.32C5.4,15.36 2,12.28 2,8.5 2,5.42 4.42,3 7.5,3c1.74,0 3.41,0.81 4.5,2.09C13.09,3.81 14.76,3 16.5,3 19.58,3 22,5.42 22,8.5c0,3.78 -3.4,6.86 -8.55,11.54L12,21.35z";
    }else if(icon==="account"){
        pathData = "M3,5v14c0,1.1 0.89,2 2,2h14c1.1,0 2,-0.9 2,-2L21,5c0,-1.1 -0.9,-2 -2,-2L5,3c-1.11,0 -2,0.9 -2,2zM15,9c0,1.66 -1.34,3 -3,3s-3,-1.34 -3,-3 1.34,-3 3,-3 3,1.34 3,3zM6,17c0,-2 4,-3.1 6,-3.1s6,1.1 6,3.1v1L6,18v-1z";
    }else if(icon==="add"){
        pathData = "M19,13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z";
    }
    var code = '<vector android:height="24dp" android:tint="#212121"\n    android:viewportHeight="24.0" android:viewportWidth="24.0"\n    android:width="24dp" xmlns:android="http://schemas.android.com/apk/res/android">\n    <path android:fillColor="'+{color}+'" android:pathData="'+pathData+'"/>\n</vector>';
    return code;
}