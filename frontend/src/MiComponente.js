//  import required libraries
import React, {useState} from "react";
import ReactFileReader from 'react-file-reader';
import axios from 'axios';
import './estilos.css';
//import { extractSheetData } from "../util/util.js";
import { IO } from "@grapecity/spread-excelio";

export const MiComponente = () => {
  
  const [nokiaFileSelected, setNokiaFileSelected] = useState('');
  const [posfaFileSelected, setPosfaFileSelected] = useState('');
  const [respuestaNokiaPost, setRespuestaNokiaPost] = useState('');
  const [respuestaPosfaPost, setRespuestaPosfaPost] = useState('');
  const lblNokiaFile = nokiaFileSelected.name;
  const lblPosfaFile = posfaFileSelected.name;

  
  const [_spread, setSpread] = useState({});
    
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
    
    (files[0].name.endsWith('.csv')) ? setNokiaFileSelected(files[0]) : setPosfaFileSelected(files[0])
    
  };

  const fileChange = (e) => {
    if (_spread) {
        const fileDom = e.target || e.srcElement;
        const excelIO = new IO();
        const spread = spread;
        /*const deserializationOptions = {
            frozenRowsAsColumnHeaders: true
        };
        excelIO.open(fileDom.files[0], (data) => {
            const newSalesData = extractSheetData(data);
            console.log(newSalesData);
        });*/
    };
  };

  const btnProcesar = async() => {
    const formuNk = new FormData();
    const formuPf = new FormData();
    
    formuNk.append("file", nokiaFileSelected);
    formuPf.append("file", posfaFileSelected);

    document.getElementById("btn-procesar").disabled = true;
    document.getElementById("estado").innerText = "Estamos trabajando....";

    await axios.post("http://ec2-54-235-43-10.compute-1.amazonaws.com:5000/nokia_s3", formuNk)
    .then(response=>{
      setRespuestaNokiaPost(response.data);
    }).catch(error=>{
      console.log(error);
    });

    document.getElementById("respuestaNokia").innerText = respuestaNokiaPost.toString().endsWith("éxito") ? "  " & { respuestaNokiaPost } : "  Ocurrió un error";
    
    await axios.post("http://ec2-54-235-43-10.compute-1.amazonaws.com:5000/facturacion_s3", formuPf)
    .then(response=>{
      console.log(response.data);
      setRespuestaPosfaPost(response.data);
    }).catch(error=>{
      console.log(error);
    });
    document.getElementById("respuestaPosfa").innerText = respuestaPosfaPost.toString().endsWith("éxito") ? "  " & { respuestaPosfaPost } : "  Ocurrió un error";

    document.getElementById("estado").innerText = "Procesamos los datos ....";
  };

  return (
    <>
      <div>
        <div id="estado-line">
          <label id="estado"></label>
        </div>
          <div id="form-line">
            <label> Seleccione el archivo CSV de la <strong>NOKIA</strong> a leer:
              <input 
                type="text" 
                name="nokiaFile"              
                value={ lblNokiaFile }
                onChange={e => setNokiaFileSelected(e.target.nokiaFile)}
              />
            </label>
            <ReactFileReader handleFiles = {uploadFile} fileTypes={".csv"}>
              <button className="btn"> Leer archivo NOKIA </button>
            </ReactFileReader>
            <label className="respuesta" id="respuestaNokia">{ respuestaNokiaPost }</label>
          </div>
          <div id="form-line">
            <label> Seleccione el archivo XLS de la <strong>POSFA</strong> a leer:
              <input 
                type="text" 
                name="posfaFile"              
                value={ lblPosfaFile }
                onChange={e => setPosfaFileSelected(e.target.posfaFile)}
              />
            </label>
            <ReactFileReader handleFiles = {uploadFile} fileTypes={".csv"}>
              <button className="btn"> Leer archivo POSFA </button>
            </ReactFileReader>
            <label className="respuesta" id="respuestaPosfa">{ respuestaPosfaPost }</label>
          </div>
          <div id="form-line">
            <button className="btn" id="btn-procesar" onClick={()=>btnProcesar()}> Procesar archivos </button>
          </div>     
          <div>
        <div>
          <b>Import Excel File:</b>
          <input type="file" className="fileSelect" 
            onChange={(e) => fileChange(e)} />
        </div>
    </div>
      </div>
    </>
  );
}
