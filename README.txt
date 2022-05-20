Antes de ejecutar el programa se debe:
1) abrir el cmd en modo administrador.
2) Escribir el siguiente comando:
	Get-ExecutionPolicy -List
3) Verificar que CurrentUser este en RemoteSigned:
	Scope ExecutionPolicy
        ----- ---------------
MachinePolicy       Undefined
   UserPolicy       Undefined
      Process       Undefined
  CurrentUser    RemoteSigned
 LocalMachine       Undefined

4) En caso que no este, ejecutar el siguiente comando:
	Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

5) Volver a ejecutar el comando del paso 2. y debe aparecer de la siguiente manera:
	Scope ExecutionPolicy
        ----- ---------------
MachinePolicy       Undefined
   UserPolicy       Undefined
      Process       Undefined
  CurrentUser    RemoteSigned
 LocalMachine       Undefined

Para mayor información acerca de estos comandos, visita la página:
https://docs.microsoft.com/es-es/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.2

Estos comandos ayudan a ejecutar los procesos distribuidos del programa.