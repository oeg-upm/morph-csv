import React from 'react'
import { Modal, Button,Table } from 'antd';
import Title from 'antd/lib/skeleton/Title';

export default class SparqlResult extends React.Component {
    constructor(props){
        super(props);
        this.state = { visible: true };

    }

  showModal = () => {
    this.setState({
      visible: true,
    });
  };

  handleOk = e => {
    console.log(e);
    this.setState({
      visible: false,
    });
  };

  handleCancel = e => {
    console.log(e);
    this.setState({
      visible: false,
    });
  };

  render() {
    return (
      <>
      <Title level={3} >Sparql Result:</Title>
        <Table dataSource={this.props.data} bordered columns={this.props.head}></Table>
      </>
    );
  }
}