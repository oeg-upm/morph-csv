import React, {useState} from 'react'
import { Row,Col,Form, Input, Button, Switch, Typography, Divider} from 'antd';

const {Text} = Typography



const RunMorph = (props) => {
    let [isCsvwFile, setIsCsvwFile] = useState(false);
    let [isYarrrmlFile, setIsYarrrmlFile] = useState(false);
    let [isQueryFile, setIsQueryFile] = useState(false);
    let [queryFile, setQueryFile] = useState(null)
    let [csvwFile, setCsvwFile] = useState(null)
    let [yarrrmlFile, setYarrrmlFile] = useState(null)
    let [uploaded, setUploaded] = useState(false)
    let [uploading, setUploading] = useState(false)
    let [runMorphRdb,setRunMorphRdb] = useState(false)
    let [morphRdbData,setMorphRdbData] = useState({})
    const onFinish = values => {
    uploadFiles(values)
  };
  function callBack(data){
    props.parentCallback(data,runMorphRdb)
  }
  const uploadFiles = (values) => {
    const formData = new FormData();
    if(isCsvwFile){
      formData.append("csvwFile", csvwFile)
    }else{
      formData.append("csvwLink", values.csvwLink)
    }
    if(isYarrrmlFile){
      formData.append("yarrrmlFile", yarrrmlFile)
    }else{
      formData.append("yarrrmlLink", values.yarrrmlLink)

    }
    if(isQueryFile){
      formData.append("queryFile", queryFile)
    }else if (values.queryLink !== undefined){
      formData.append("queryLink", values.queryLink)
    }        
    callBack(formData)
  }

  return (
    <>
    <Form
      name="basic"
      onFinish={onFinish}
    >
        <Row gutter={[16,16]}>
            <Col>
                <Text>Do you prefer upload a CSVW file?</Text> 
            </Col>
            <Col>
                <Switch value={isCsvwFile} onChange={() => {setIsCsvwFile(!isCsvwFile)}} />            
            </Col>
        </Row>
        {
            !isCsvwFile?(
                <Form.Item
                label="CSVW Url"
                name="csvwLink"
              >
                <Input value=""/>
              </Form.Item>
            ):(
              <Form.Item label={(csvwFile)
                ? `File ${csvwFile.name} selected`
                : ' Choose  File'
            }>
              <label className="custom-file-upload">
              <Input
                    className="file-input"
                    type="file" name="file"
                    onChange={(e) => {
                        if (e.target.files && e.target.files.length > 0) {
                            setCsvwFile(e.target.files[0], );
                        }
                    }} />                    
              </label>
            </Form.Item>
            )
        }

<Row gutter={[16,16]}>
            <Col>
                <Text>Do you prefer upload a YARRRML+FnO file?</Text> 
            </Col>
            <Col>
                <Switch value={isYarrrmlFile} onChange={() => {setIsYarrrmlFile(!isYarrrmlFile)}} />            
            </Col>
</Row>

{
            !isYarrrmlFile?(
                <Form.Item
                label="YARRRML+FnO Url"
                name="yarrrmlLink"
                value=""
              >
                <Input />
              </Form.Item>
            ):(
              <Form.Item label={(yarrrmlFile)
                ? `File ${yarrrmlFile.name} selected`
                : ' Choose File'
            }>
              <label className="custom-file-upload">
              <Input
                    className="file-input"
                    type="file" name="file"
                    onChange={(e) => {
                        if (e.target.files && e.target.files.length > 0) {
                            setYarrrmlFile(e.target.files[0], );
                        }
                    }} />                    
              </label>
            </Form.Item>
            )
        }
        <Row gutter={[16,16]}>
            <Col>
                <Text>Do you prefer upload a Query file?</Text> 
            </Col>
            <Col>
                <Switch value={isQueryFile} onChange={() => {setIsQueryFile(!isQueryFile)}} />            
            </Col>
        </Row>
{
            !isQueryFile?(
                <Form.Item
                label="Query Url"
                name="queryLink"
              >
                <Input />
              </Form.Item>
            ):(
              <Form.Item label={(queryFile)
                ? `File ${queryFile.name} selected`
                : ' Choose  File'
            }>
              <label className="custom-file-upload">
              <Input
                    className="file-input"
                    type="file" name="file"
                    onChange={(e) => {
                        if (e.target.files && e.target.files.length > 0) {
                            setQueryFile(e.target.files[0], );
                        }
                    }} />                    
              </label>
            </Form.Item>
            )
        }    
        <Row gutter={[16,16]}>
          <Col>
          <Text>Run Morph-RDB?</Text>
          </Col>
          <Col>
          <Switch onChange={() => {setRunMorphRdb(!runMorphRdb);}} />            
          </Col>
          <Col>
            <Text type="secondary"> This will return a table with the sparql result</Text>
          </Col>
        </Row>
      <Form.Item >
        <Button type="primary" htmlType="submit">
          Submit
        </Button>
      </Form.Item>
    </Form>
    <Divider></Divider>
    </>
  );
};
export default RunMorph