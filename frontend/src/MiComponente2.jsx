import React, {useState} from 'react';
import './estilos.css';
import { saveAs } from 'file-saver';
import axios from 'axios';

export const MiComponente2 = () => {

    const [nokia, setNokia] = useState('');
    const [posfa, setPosfa] = useState('');
    const [respuestaNokiaPost, setRespuestaNokiaPost] = useState('');
    const [respuestaPosfaPost, setRespuestaPosfaPost] = useState('');

    
    const fileChange = (e) => {
        const fileDom = e.target || e.srcElement;
        setPosfa(fileDom.files[0]);
        console.log(posfa);
        console.log(fileDom.files[0]);
    }
    const leerExcel = (e) => {
        e.preventDefault();
        /*const formData = new FormData(e.currentTarget);
        let excel = formData.get("excel");
        let listWorksheet = [];

        let reader = new FileReader();
        reader.readAsArrayBuffer(excel);
        reader.onloadend = (e) => {
            let data = new Uint8Array(e.target.result);
            let excelRead = XLSX.read(data, { type: 'array' });
            excelRead.SheetNames.forEach(function(sheetName, index) {
                listWorksheet.push({
                    data: excelRead.Sheets[sheetName],
                    name: sheetName,
                    index: index
                })
            });

            this.state.woorksheets = listWorksheet;
            this.setState({
                woorksheets: this.state.woorksheets
            })

            this.leerPropiedades(0);
            this.leerFilas(0);
            this.setState({
                filas: this.state.filas,
                propiedades: this.state.propiedades,
                status: true
            })
        }*/
        //setPosfaFileSelected(e.target.excel)
    };

    const leerArchivo = (e) => {
        const fileDom = e.target || e.srcElement;
        const file = e;
        let dato = e.target ? fileDom.files[0] : file;
        console.log(dato.name)
        dato.name.toLowerCase().includes("nokia") ? setNokia(dato) : setPosfa(dato);
        
    }

    const crearCSV = (myValue, fileName) => {
        const file = new File([myValue], fileName, {type: "text/plain;charset=utf-8"});
        saveAs(file);
        leerArchivo(file);
    };

    const  leerCSV = (e) => {
        e.preventDefault();

        const formData = new FormData(e.currentTarget);
        let file = formData.get("csv");
        
        const reader = new FileReader();

        reader.onload = function(e) {
            const nameNokia = "mi-archivo-nokia" + (new Date()).getMilliseconds().toString() + ".csv";
            console.log(file.name);
            const namePosfa = "mi-archivo-posfa" + (new Date()).getMilliseconds().toString() + ".csv";
            const fileName = file.name.toLowerCase().includes("nokia") ? nameNokia : namePosfa;
            console.log(fileName);
            const text = e.target.result;

            let nuevoTexto = '';
            fileName.includes("nokia") ? nuevoTexto = text.replaceAll(",", ' ') : nuevoTexto = text.replaceAll(",", '.');
            
            text.includes(',') ?  crearCSV(nuevoTexto, fileName) : console.log('todo ok');            
        }

        console.log('file', formData);
        reader.readAsText(file);       
    };

       

    const btnProcesar = async() => {
        const formuNk = new FormData();
        const formuPf = new FormData();
        
        formuNk.append("file", nokia);
        formuPf.append("file", posfa);

        console.log(nokia);
        console.log(posfa);
            
        document.getElementById("btn-procesar").disabled = true;
        document.getElementById("estado").innerText = "Estamos trabajando....";
         /*   
        await axios.post("http://ec2-54-235-43-10.compute-1.amazonaws.com:5000/nokia_s3", formuNk)
        .then(response=>{
          setRespuestaNokiaPost(response.data);
        }).catch(error=>{
          console.log(error);
        })
            
        document.getElementById("respuestaNokia").innerText = respuestaNokiaPost.toString().endsWith("éxito") ? "  " & { respuestaNokiaPost } : "  Ocurrió un error";
        
        await axios.post("http://ec2-54-235-43-10.compute-1.amazonaws.com:5000/facturacion_s3", formuPf)
        .then(response=>{
          console.log(response.data);
          setRespuestaPosfaPost(response.data);
        }).catch(error=>{
          console.log(error);
        });
        document.getElementById("respuestaPosfa").innerText = respuestaPosfaPost.toString().endsWith("éxito") ? "  " & { respuestaPosfaPost } : "  Ocurrió un error";
    
        document.getElementById("estado").innerText = "Procesamos los datos ....";*/
      };

  return (
    <>
      <div>
        <div id="estado-line">
          <label id="estado"></label>
        </div>
        <div id="form-line">
            <form onSubmit={ leerCSV } >
                <label className="form-label">Selecciona el archivo de NOKIA:</label>
                <input 
                    type="file" 
                    className="form-control"
                    accept=".csv"
                    name="csv" 
                    onChange={e => leerArchivo(e)}
                   />
                <button className="btn btn-primary mt-3">Leer NOKIA</button>
                <label className="respuesta" id="respuestaNokia">{ respuestaNokiaPost }</label>
            </form>
            <form onSubmit={ leerCSV } >
                <label className="form-label">Selecciona el archivo de POSFA:</label>
                <input 
                    type="file" 
                    className="form-control"
                    //accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    accept=".csv"
                    name="excel"
                    //onChange={(e) => fileChange(e)}/>
                    onChange={e => leerArchivo(e)}/>
                <button className="btn btn-primary mt-3">Leer NOKIA</button>
                <label className="respuesta" id="respuestaPosfa">{ respuestaPosfaPost }</label>
            </form>
            
        </div>
        <div id="form-line">
            <button className="btn" id="btn-procesar" onClick={()=>btnProcesar()}> Procesar archivos </button>
        </div>  
      </div>        
    </>)
};
