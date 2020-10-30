import React, {useState} from 'react'
import { Row,Col,Form, Input, Button, Switch, Typography } from 'antd';

const {Text} = Typography

const tailLayout = {
  wrapperCol: { offset: 8, span: 24 },
};

const RunMorph = (props) => {
    let [isCsvwFile, setIsCsvwFile] = useState(false);
    let [isYarrrmlFile, setIsYarrrmlFile] = useState(false);
    let [isQueryFile, setIsQueryFile] = useState(false);
    let [queryFile, setQueryFile] = useState(null)
    let [csvwFile, setCsvwFile] = useState(null)
    let [yarrrmlFile, setYarrrmlFile] = useState(null)
    let [uploaded, setUploaded] = useState(false)
    let [uploading, setUploading] = useState(false)
    let [runMorphRdb,setRunMorphRdb] = useState(true)
    let [morphRdbData,setMorphRdbData] = useState({})
    const onFinish = values => {
    console.log('Success:', values);
    uploadFiles(values)
  };
  function callBack(data){
    props.parentCallback(data,runMorphRdb)
  }
  const uploadFiles = (values) => {
    values.yarrrmlLink = "https://raw.githubusercontent.com/oeg-upm/morph-csv/evaluation/swj2020-si-webofdata/resources/gtfs/gtfs-csv.yaml"
    values.csvwLink = "https://raw.githubusercontent.com/oeg-upm/morph-csv/evaluation/swj2020-si-webofdata/resources/gtfs/gtfs.csvw.json"   
    values.queryLink = "https://raw.githubusercontent.com/oeg-upm/morph-csv/evaluation/swj2020-si-webofdata/resources/gtfs/queries/original/q1.rq" 
    const formData = new FormData();
    formData.append('runMorphRdb',runMorphRdb)
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
    <Form
      name="basic"
      onFinish={onFinish}
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
                <Input value="https://raw.githubusercontent.com/oeg-upm/morph-csv/evaluation/swj2020-si-webofdata/resources/gtfs/gtfs.csvw.json"/>
              </Form.Item>
            ):(
              <Form.Item label={(csvwFile)
                ? `File ${csvwFile.name} selected`
                : ' Choose File'
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
                <Text>Would you rather upload a Yarrrml file?</Text> 
            </Col>
            <Col>
                <Switch value={isYarrrmlFile} onChange={() => {setIsYarrrmlFile(!isYarrrmlFile)}} />            
            </Col>
</Row>

{
            !isYarrrmlFile?(
                <Form.Item
                label="yarrrmlLink"
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
                <Text>Would you rather upload a Query file?</Text> 
            </Col>
            <Col>
                <Switch value={isQueryFile} onChange={() => {setIsQueryFile(!isQueryFile)}} />            
            </Col>
        </Row>
{
            !isQueryFile?(
                <Form.Item
                label="queryLink"
                name="queryLink"
              >
                <Input />
              </Form.Item>
            ):(
              <Form.Item label={(queryFile)
                ? `File ${queryFile.name} selected`
                : ' Choose File'
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
          <Col><Text>Run Morphrdb?</Text></Col>
          <Col>
          <Switch value={runMorphRdb} defaultChecked onChange={() => {setRunMorphRdb(!runMorphRdb)}} />            
          </Col>
        </Row>
      <Form.Item {...tailLayout}>
        <Button type="primary" htmlType="submit">
          Submit
        </Button>
      </Form.Item>
    </Form>
  );
};
export default RunMorph