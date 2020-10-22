import React from 'react'

import {Row,Col} from 'antd'

import Runmorph from '../components/Runmorph.js'
import Layout from '../components/Layout'
export default function Home(){
    return(
       <Layout>
        <h1>Home</h1>
        <Row>
           <Col>
                <Runmorph  />
           </Col>
       </Row>
       </Layout>
    )
}