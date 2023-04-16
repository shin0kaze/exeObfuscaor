format          PE console 4.0      ; PE формат
entry           start               ; Адрес начала исполнения
include         '%fasminc%/win32a.inc'        ; библиотеки х32
 
; ---=/ Код программы \=---
 
section         '.text' code readable executable
 
  start:
        not     word [ebx]
        mov     ax,5
        mov     ax,64516
        mov     ax,0
        mov     bx,5
        mov     ax,32
        mov     bx,0
        mov     ax,bx
        mov     bx,ax
        invoke  GetStdHandle, STD_OUTPUT_HANDLE
        mov     [stdout], eax
        invoke  GetStdHandle, STD_INPUT_HANDLE
        mov     [stdin], eax
        invoke  WriteConsole,[stdout],cMsg,13,NULL,NULL
        invoke  ReadConsole,[stdin],lpBuffer,10,lpCharsRead,NULL
        invoke  WriteConsole,[stdout],lpBuffer,10,NULL,NULL
  exit:
        invoke  ExitProcess, 0
 
; ---=/ Данные \=--- 
 
section         '.data' data readable writeable
 
cMsg            db      'Hello, world!'
lpBuffer        db      10 dup (0)
lpCharsRead     dd      ?
stdin           dd      ?
stdout          dd      ?
 
; ---=/ Импорты системных библиотек \=---
 
section         '.idata' import data readable writeable
 
library         kernel32,'KERNEL32.DLL'
 
import          kernel32,\ 
                GetStdHandle,'GetStdHandle',\ 
                WriteConsole,'WriteConsoleA',\
                ReadConsole,'ReadConsoleA',\
                ExitProcess,'ExitProcess'