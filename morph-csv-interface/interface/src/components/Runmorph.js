import React, {useState} from 'react'
import { Row,Col,Form, Input, Button, Switch, Typography } from 'antd';
import axios from 'axios'
import {UploadOutlined} from '@ant-design/icons'
const {Text} = Typography
const layout = {
  labelCol: { span: 8 },
  wrapperCol: { span: 24 },
};
const tailLayout = {
  wrapperCol: { offset: 8, span: 24 },
};
const ENDPOINT = "http://localhost:5000/runmorphcsv"
const RunMorph = () => {
    let [isCsvwFile, setIsCsvwFile] = useState(false);
    let [isYarrrmlFile, setIsYarrrmlFile] = useState(false);
    let [isQueryFile, setIsQueryFile] = useState(false);
    let [queryFile, setQueryFile] = useState(null)
    let [csvwFile, setCsvwFile] = useState(null)
    let [yarrrmlFile, setYarrrmlFile] = useState(null)
    let [uploaded, setUploaded] = useState(false)
    let [uploading, setUploading] = useState(false)

    const onFinish = values => {
    console.log('Success:', values);
    uploadFiles(values)
  };
  const uploadFiles = (values) => {
    const formData = new FormData();
    if(isCsvwFile){
      formData.append("csvwFile", csvwFile)
    }else{
      formData.append("csvwLink", values.csvwLink)
    }
    if(isQueryFile){
      formData.append("yarrrmlFile", yarrrmlFile)
    }else{
      formData.append("yarrrmlLink", values.yarrrmlLink)

    }
    if(isYarrrmlFile){
      formData.append("queryFile", queryFile)
    }else{
      formData.append("queryLink", values.queryLink)
    }        
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
      // our mocked response will always return true
      // in practice, you would want to use the actual response object
      console.log(resp)
      setUploaded(true);
      setUploading(false);
  })
  .catch((err) => console.error(err));    
  }
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
      <Form.Item {...tailLayout}>
        <Button type="primary" htmlType="submit">
          Submit
        </Button>
      </Form.Item>
    </Form>
  );
};
// export default class Demo extends React.Component {
//   state = {
//     file:null,
//     format:"rml",
//     uploading: false,
//     imageUri:null,
//     uploadProgress:0,
//     uploadStatus:false,
//     upload:false,
//     driveUrl:"",
//     acceptedTypes:['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']
//   };

//   getBase64(file,callback){
//       const reader = new FileReader();
//       // FileReader API Spec: https://developer.mozilla.org/en-US/docs/Web/API/FileReader/FileReader
//       reader.addEventListener('load', () => callback(reader.result));
//       reader.readAsDataURL(file);
//   }

//    isValidFileType = (fileType) => {
//        console.log('FileType: ' + fileType)
//       return this.state.acceptedTypes.includes(fileType);
//   };
//    handleClick = event => {
//     // this.hiddenFileInput.current.click();
//   };
//    handleFileUpload = (e) => {
//       e.preventDefault();
//       console.log(this.state.file)
//       if (!this.isValidFileType(this.state.file.type)) {
//           alert('Only XLSX files are allowed');
//           return;
//       }
      
//       this.setState({uploading:true});
//       const formData = new FormData();
//       if(this.state.file === null){
//         formData.append('url', this.state.url);
//       }else{
//         formData.append('file', this.state.file);
//         formData.append('format', this.state.format);
//       }

//       axios({
//           method: 'post',
//           headers: {
//             'accept':'binary/octet-stream',
//             'Content-Type': 'multipart/form-data',
//             'Access-Control-Allow-Headers':'*'
//         },
//           data: formData,
//           url: UPLOAD_SUCCESS_URL,
//           onUploadProgress: (ev) => {
//               const progress = ev.loaded / ev.total * 100;
//               this.setState({uploadProgress:Math.round(progress)});
//           },
//       })
//       .then((resp) => {
//           // our mocked response will always return true
//           // in practice, you would want to use the actual response object
//           console.log(resp)
//           this.setState({uploadStatus:true});
//           this.setState({uploading:false});
//           this.getBase64(this.state.file, (uri) => {
//               this.setState({imageUri:uri});
//           });
//       })
//       .catch((err) => console.error(err));
//   };

//   render() {

//     return (
//         <Layout>
//             <Row>
//                 <Col xs={22} md={12}>
//                 <Title level={2}>Mapeathor Demo</Title>
//                 <Paragraph>
//                     You can test this tool with the demo below, 
//                     just use a Google Spreadsheet URL or an Excel 
//                     file (XLSX) and select a mapping format. 
//                     Check the templates and examples in the GitHub repository. 
//                     You can also check <a href="https://morph.oeg.fi.upm.es/tool/mapeathor/swagger/">this Swagger instance.</a> 
//                 </Paragraph>                
//                 </Col>
//             </Row>
//       <div className="app">

//           <form onSubmit={this.handleFileUpload} className="form">

//               <Form.Item label="URL">
//                   <Input onChange={(e) => this.setState({driveUrl:e.targe.value})}></Input>
//               </Form.Item>
//               <Form.Item label={(this.state.file)
//                       ? `File ${this.state.file.name} selected`
//                       : ' Choose File'
//                   }>
//                 <label className="custom-file-upload">
//                 <Input
//                       className="file-input"
//                       type="file" name="file"
//                       accept={this.state.acceptedTypes.toString()}
//   //                       onChange={(e) => {
//                           if (e.target.files && e.target.files.length > 0) {
//                               this.setState({file:e.target.files[0]})
//                           }
//                       }} />                    
//                     <span>
//                     <UploadOutlined></UploadOutlined> Upload XLSX File
//                     </span>
//                 </label>
//               </Form.Item>
//               <Form.Item>
//                 <Button className="upload-button" onClick={this.handleFileUpload} type="submit">
//                     Upload
//                 </Button>
//               </Form.Item>
//           </form>
          


//       </div>
//         </Layout>
//     );
//   }

// }
export default RunMorph