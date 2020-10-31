import axios from 'axios'
const ENDPOINT = "http://localhost:5000/runmorphcsv"

function runMorphCsv(formData){
    return new Promise((resolve,reject) => {
        axios({
            method: 'post',
            responseType: 'arraybuffer',
            headers: {
              'accept':'binary/octet-stream',
              'Content-Type': 'multipart/form-data',
              'Access-Control-Allow-Headers':'*'
          },
            data: formData,
            url: ENDPOINT
        })
        .then((resp) => {
            resolve(resp.data)
        })
        .catch((err) => reject(err));    
    })
}
function runMorphRdb(formData){
    return new Promise((resolve,reject) => {
        axios({
            method: 'post',
            headers: {
              'accept':'binary/octet-stream',
              'Content-Type': 'multipart/form-data',
              'Access-Control-Allow-Headers':'*'
          },
            data: formData,
            url: ENDPOINT
        })
        .then((resp) => {
            resolve(resp.data)
        })
        .catch((err) => reject(err));    
    })
}


export  {runMorphCsv,runMorphRdb} 