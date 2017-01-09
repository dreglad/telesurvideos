# teleSUR Video website

## Requerimientos
Cualquier sistema con las versiones más recientes de:
 - [Virtualbox][1]
 - [Vagrant][2]

## Instalación
  1. Clonar repositorio
  ```{r, engine='bash'}
  $ git clone https://github.com/dreglad/telesurvideos
  ```

  1. Iniciar el ambiente:
  ```{r, engine='bash'}
  $ cd telesurvideos
  $ vagrant up
  ```

## Uso
  - Frontend:
   - Español: http://127.0.0.1:8080/
   - English: http://127.0.0.1:8081/
  - Backend: (credenciales por defecto: *admin/telesur*)
   - Español: http://127.0.0.1:8080/?edit
   - English: http://127.0.0.1:8081/?edit



  [1]: https://www.virtualbox.org/ "Oracle Virtualbox"
  [2]: https://www.vagrantup.com/ "Vagrant"
