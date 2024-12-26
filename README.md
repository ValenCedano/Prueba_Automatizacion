<h1>Programa de generación de facturas de comisiones.</h1>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Tabla de Contenido</summary>
  <ol>
    <li>
      <a href="#about-the-project">Acerca del proyecto </a>
      <ul>
        <li><a href="#built-with">Tecnologías implementadas</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Configuraciones Iniciales</a>
      <ul>
        <li><a href="#prerequisites">Prerequisitos</a></li>
        <li><a href="#installation">Instalaciones</a></li>
      </ul>
    </li>   
    <li><a href="#contact">Autores</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## Acerca del proyecto 
El siguiente programa presenta una forma de automatizar el cobro de comisiones en función del estado de las llamadas a las APIs que ofrece la empresa proveedora. El objetivo es reducir errores, agilizar los procesos y optimizar el uso de los recursos. 
## Tecnologías implementadas

<div align="center">
	<code><img width="50" src="https://user-images.githubusercontent.com/25181517/192108374-8da61ba1-99ec-41d7-80b8-fb2f7c0a4948.png" alt="GitHub" title="GitHub"/></code>
  <code><img width="50" src="https://w7.pngwing.com/pngs/585/822/png-transparent-python-scalable-graphics-logo-javascript-creative-dimensional-code-angle-text-rectangle-thumbnail.png" alt="Python" title="Python"/></code>
  <code><img width="50" src= "https://w7.pngwing.com/pngs/1010/539/png-transparent-sqlite-logo-thumbnail-tech-companies-thumbnail.png" alt="SQLite" title="SQLite"/></code>
  
</div>


<!-- GETTING STARTED -->
## Configuraciones Iniciales

Para poner en funcionamiento una copia local, siga estos sencillos pasos de ejemplo

### Prerequisitos
<ul>
  <li> El sistema operativo donde se ejecuta el programa debe ser  <b>Windows 10 o 11 con Microsoft 365 u Office 2019/2021</b></li>
</ul>

Verificar que tenga instalados los siguientes programas.
* Python 3.8 en adelante
  ```sh
   https://www.python.org/downloads/
  ```
* Aplicación Outlook y estar logueado en la aplicación
  ```sh
   https://www.microsoft.com/es-es/microsoft-365/outlook/outlook-for-windows
  ```

### Instalaciones

Realizar las siguientes instalaciones necesarias.

1. Clonar el repositorio
   ```sh
   https://github.com/ValenCedano/Prueba_Automatizacion.git
   ```
2. Abrir la terminal del sistema operativo e ingresar a la dirrección de la carpeta del repositorio
   ```sh
    C:\Users\valen\Documentos\Valentina work\Prueba_Automatizacion (Ejemplo)
   ```
3. Instalar las librerías necesarias con el siguiente comando
   ```sh
   pip install -r requirements.txt
   ```
4. Ejecutar el siguiente comando
   ```sh
   python 02_AUTOMATIZACION.py
   ```
<h4>Notas Adicionales</h4>
<p>Si necesita modificar la base de datos de contratos, abra el script <b>00_CREACION_TABLA_CONTRATOS</b>, modifique la consulta SQL y luego ejecute el siguiente comando para actualizar la base de datos antes de ejecutar el programa AUTOMATIZACION.</p>

```sh
   python 00_CREACION_TABLA_CONTRATOS.py
```
<p>Después ejecutar le siguiente comando: </p>

```sh
   python 02_AUTOMATIZACION.py
```
En caso de requerir mayor información sobre los scripts, explore el archivo <b>Documentacion Tecnica.pdf</b>
<!-- CONTACT -->
## Desarrolladores

Valentina Cedano: [https://github.com/ValenCedano](https://github.com/ValenCedano)