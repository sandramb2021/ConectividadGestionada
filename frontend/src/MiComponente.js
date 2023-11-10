//  import required libraries
import React, {useState} from "react";
import ReactFileReader from 'react-file-reader';
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
      </div>
    </>
  );
}
export default MiComponente;