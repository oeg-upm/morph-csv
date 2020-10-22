import React, {useState} from 'react'
import { Row,Col,Form, Input, Button, Switch, Typography } from 'antd';

const {Text} = Typography
const layout = {
  labelCol: { span: 8 },
  wrapperCol: { span: 24 },
};
const tailLayout = {
  wrapperCol: { offset: 8, span: 24 },
};

const RunMorph = () => {
    let [isCsvwFile, setIsCsvwFile] = useState(false);
    let [isYarrrmlFile, setIsYarrrmlFile] = useState(false);
    let [isQueryFile, setIsQueryFile] = useState(false);

    const onFinish = values => {
    console.log('Success:', values);
  };

  const onFinishFailed = errorInfo => {
    console.log('Failed:', errorInfo);
  };

  return (
    <Form
      name="basic"
      onFinish={onFinish}
      onFinishFailed={onFinishFailed}
    >
        <Row gutter={[16,16]}>
            <Col>
                <Text>Would you rather upload a CSVW file?</Text> 
            </Col>
            <Col>
                <Switch value={isCsvwFile} onChange={() => {setIsCsvwFile(!isCsvwFile)}} />            
            </Col>
        </Row>
        {
            !isCsvwFile?(
                <Form.Item
                label="csvwLink"
                name="csvwLink"
              >
                <Input />
              </Form.Item>
            ):(
                <Form.Item
                label="csvwFile"
                name="csvwFile"
              >
                <Input type="file" />
              </Form.Item>
            )
        }

<Row gutter={[16,16]}>
            <Col>
                <Text>Would you rather upload a Yarrrml file?</Text> 
            </Col>
            <Col>
                <Switch value={isYarrrmlFile} onChange={() => {setIsYarrrmlFile(!isYarrrmlFile)}} />            
            </Col>
</Row>

{
            !isYarrrmlFile?(
                <Form.Item
                label="csvwLink"
                name="csvwLink"
              >
                <Input />
              </Form.Item>
            ):(
                <Form.Item
                label="csvwFile"
                name="csvwFile"
              >
                <Input type="file" />
              </Form.Item>
            )
        }
        <Row gutter={[16,16]}>
            <Col>
                <Text>Would you rather upload a Query file?</Text> 
            </Col>
            <Col>
                <Switch value={isQueryFile} onChange={() => {setIsQueryFile(!isQueryFile)}} />            
            </Col>
        </Row>
{
            !isQueryFile?(
                <Form.Item
                label="csvwLink"
                name="csvwLink"
              >
                <Input />
              </Form.Item>
            ):(
                <Form.Item
                label="csvwFile"
                name="csvwFile"
              >
                <Input type="file" />
              </Form.Item>
            )
        }    
      <Form.Item {...tailLayout}>
        <Button type="primary" htmlType="submit">
          Submit
        </Button>
      </Form.Item>
    </Form>
  );
};
export default RunMorph