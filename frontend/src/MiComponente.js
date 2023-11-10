//  import required libraries
import React, {useState} from "react";
import ReactFileReader from 'react-file-reader';
import axios from 'axios';
import './estilos.css';

const MiComponente = () => {
  
  const [nokiaFileSelected, setNokiaFileSelected] = useState('');
  const [posfaFileSelected, setPosfaFileSelected] = useState('');
  
  const uploadFile = (files) => {
    // Creating the object of FileReader Class
    var read = new FileReader();
	// when readAsText will invoke, onload() method on the read object will execute.
    read.onload = function (e) {
      // perform some operations with read data
      //alert(files[0].name);
    };
	// Invoking the readAsText() method by passing the uploaded file as a parameter
    read.readAsText(files[0]);
    (files[0].name.endsWith('.csv')) ? setNokiaFileSelected(files[0].name) : setPosfaFileSelected(files[0].name)
    console.log(files[0].name);
  };

  const btnProcesar = async() => {
    const formu = new FormData();

    formu.append("files", nokiaFileSelected);
    formu.append("files", posfaFileSelected);
    
    console.log(formu);

    await axios.post("http://ec2-34-224-8-97.compute-1.amazonaws.com:5000/", formu)
    .then(response=>{
      console.log(response.data);
    }).catch(error=>{
      console.log(error);
    });

  };

  return (
    <>
      <div>
          <div id="form-line">
            <label> Seleccione el archivo CSV de la <strong>NOKIA</strong> a leer:
              <input 
                type="text" 
                id="nokiaFile"              
                value={ nokiaFileSelected }
                onChange={e => setNokiaFileSelected(e.target.value)}
              />
            </label>
            <ReactFileReader handleFiles = {uploadFile} fileTypes={".csv"}>
              <button className="btn"> Leer archivo NOKIA </button>
            </ReactFileReader>
          </div>
          <div id="form-line">
            <label> Seleccione el archivo XLS de la <strong>POSFA</strong> a leer:
              <input 
                type="text" 
                id="posfaFile"              
                value={ posfaFileSelected }
                onChange={e => setPosfaFileSelected(e.target.value)}
              />
            </label>
            <ReactFileReader handleFiles = {uploadFile} fileTypes={".xlsx"}>
              <button className="btn"> Leer archivo POSFA </button>
            </ReactFileReader>
          </div>
          <div id="form-line">
            <button className="btn" onClick={()=>btnProcesar()}> Procesar archivos </button>
            <input type="file" name="files" onChange={ (e) => setPosfaFileSelected(e.target.files) }></input>
          </div>     
      </div>
    </>
  );
}
export default MiComponente;