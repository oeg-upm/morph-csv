import React, { useState } from 'react'

import {Row,Col, Table} from 'antd'
import  {runMorphCsv,runMorphRdb} from '../requests/api'
import Runmorph from '../components/Runmorph.js'
import Layout from '../components/Layout'
export default function Home(){
    let [mrdbResult, setMrdbResult] = useState({})


    const downloadResults = (data) => {
        const element = document.createElement("a");
        const file = new Blob([data], {type: 'application/zip'});
        element.href = URL.createObjectURL(file);
        let fileFormat = ".zip"
        let fileName = "results"
        element.download = fileName + fileFormat;
        document.body.appendChild(element); // Required for this to work in FireFox
        element.click();    
      }     
    const submitForm = async (data, runMrdb) => {
        let result = null;
        if(runMrdb){
            result = await runMorphRdb(data) 
            console.log(result)
            setMrdbResult(result)
        }else{
            result = await runMorphCsv(data)
            downloadResults(result)
        }

    }
   
    return(
       <Layout>
        <h1>Home</h1>
        <Row>
           <Col>
                <Runmorph parentCallback={submitForm} />
           </Col>
       </Row>
       {
           Object.keys(mrdbResult).length > 0 ? (
               <Table bordered dataSource={mrdbResult['data']} columns={mrdbResult['head']} />
           ):null
       }
       </Layout>
    )
}