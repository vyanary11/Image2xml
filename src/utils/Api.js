import fetch from  'isomorphic-fetch';

// const BASE_API_URL = "http://192.168.1.5:5000/"
const BASE_API_URL = "http://ac9d4a12.ngrok.io/"
 
export function api(api_end_point, data) {
 
   return fetch(BASE_API_URL+api_end_point,
       {
           method: 'POST',
           headers: {
               'Content-Type': 'application/json'
           },
           body:data
       }).then((response) => {
           return response.json();
       });
}