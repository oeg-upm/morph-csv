import React, { useState } from 'react'
import { DownloadOutlined ,UploadOutlined, LoadingOutlined } from '@ant-design/icons';
import {Row,Col, Table,Typography, Spin, Button} from 'antd'
import  {runMorphCsv,runMorphRdb} from '../requests/api'
import Runmorph from '../components/Runmorph.js'
import Layout from '../components/Layout'
import logo from '../assets/logo.png'
import SparqlResult from '../components/SparqlResult'
const {Title,Paragraph} = Typography

const loadingIcon = <LoadingOutlined style={{ fontSize: 48 }} spin />;

export default function Home(){
    let [mrdbResult, setMrdbResult] = useState({})
    let [isLoading, setIsLoading] = useState(false)
    let [showDownload, setShowDownload] = useState(false)
    let [mcsvResult, setMcsvResult] = useState(null)

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
        setMcsvResult(null)
        setMrdbResult({})
        setIsLoading(true)
        if(runMrdb){
            data.append('runMorphRdb',runMrdb)
            result = await runMorphRdb(data) 
            console.log(result)
            setMrdbResult(result)
        }else{
            result = await runMorphCsv(data)
            downloadResults(data)
            setMcsvResult(result)
            setShowDownload(true)
        }
        setIsLoading(false)


    }
   
    return(
       <Layout>
           <Row justify="space-between" gutter={[16,16]} align="middle">   
           <Col>
                <img src={logo}  className="imgFluid"/>
            </Col>
           </Row>
           <Row gutter={[16,16]}>
               <Col span={15}>
               <Title level={3}>Morph-CSV Interface</Title>
               <Paragraph className="textJustify" >
                    Morph-CSV is an open source tool for querying tabular data sources using SPARQL. It exploits the information from the query, RML+FnO mappings and CSVW metadata to enhance the performance and completeness of traditional OBDA systems (SPARQL-to-SQL translators).
                </Paragraph>
               </Col>
           </Row>   

           {isLoading ? (
                <Spin indicator={loadingIcon}></Spin>
            ):(
                <Runmorph parentCallback={submitForm} />   
           )}
           {
           Object.keys(mrdbResult).length > 0 ? (
                <SparqlResult data={mrdbResult['data']} head={mrdbResult['head']}></SparqlResult>
           ):showDownload?(
               <Button onClick={() => downloadResults(mcsvResult)}> Download Morph-CSV result <DownloadOutlined /> </Button>
            ):null
            }

       </Layout>
    )
}