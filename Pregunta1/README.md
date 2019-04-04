# Redes 3 ESCOM - IPN
## Fault management Self-Assesment
**Pregunta resuelta:**

Does the organization have a ping poller which results in a fault being raised when a device fails to respond to a ping?
### Archivos 

Se crearon diferentes scripts para dar solución a la pregunta propuesta.

```
├── outputs
│   ├── host_live.list
│   ├── network_hosts.xml
│   └── subnets.list
├── requirements.txt
├── scripts
│   ├── message.txt
│   ├── mycontacts.txt
│   ├── obtenersubredes.py
│   ├── parse.py
│   └── ping.py
└── solution.sh

```
### Requisitos

A continuación enlistamos los requisitos para el correcto funcionamiento

```
* Nmap
* Python 2
* Python 3
* XSLT (opcional)
```
## Funcionamiento
### Directorios
**scripts:** Este directorio contiene los scripts que hacen toda la magia.
**outputs:** Directorio donde se almacenan las salidas de cada script.
### DDF
![Figura 1. Diagrama de flujo solution.sh](https://github.com/todmephis/redes3ESCOM/blob/master/Pregunta1/images/p1_1.png)

## Equipo

* **Iván Sánchez** 
* **Jorge Gibbs**
* **Gabriel Campos**
* **Luis Benitez**
* **Mauricio Rodriguez**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

