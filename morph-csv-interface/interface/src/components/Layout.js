import React from 'react'
import {Row, Col} from 'antd'

export default function Layout(props){
    return(
        <Row
        justify="center"
        >
            <Col
                lg={18}
                md={20}
                xs={22}
            >
                {props.children}
            </Col>
        </Row>
    )
}