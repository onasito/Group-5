; *****************************************************************
;  Static Data Declarations (initialized)

section	.data

; -----
;  Define standard constants.

NULL		equ	0			; end of string

TRUE		equ	1
FALSE		equ	0

EXIT_SUCCESS	equ	0			; Successful operation
SYS_exit	equ	60			; call code for terminate

; -----
;  Initialized Static Data Declarations.

;	Place data declarations here...

lst dd 4224, 1116, 1542, 1240, 1677, 1635, 2420, 1820, 1246, 1333 
dd 2315, 1215, 2726, 1140, 2565, 2871, 1614, 2418, 2513, 1422 
dd 1119, 1215, 1525, 1712, 1441, 3622, 1731, 1729, 1615, 2724 
dd 1217, 1224, 1580, 1147, 2324, 1425, 1816, 1262, 2718, 1192 
dd 1435, 1235, 2764, 1615, 1310, 1765, 1954, 1967, 1515, 1556 
dd 1342, 7321, 1556, 2727, 1227, 1927, 1382, 1465, 3955, 1435 
dd 1225, 2419, 2534, 1345, 2467, 1615, 1959, 1335, 2856, 2553 
dd 1035, 1833, 1464, 1915, 1810, 1465, 1554, 1267, 1615, 1656 
dd 2192, 1825, 1925, 2312, 1725, 2517, 1498, 1677, 1475, 2034 
dd 1223, 1883, 1173, 1350, 2415, 1335, 1125, 1118, 1713, 3025
 
length dd 100
lstMin dd 0
estMed dd 0
lstMax dd 0
lstSum dd 0
lstAve dd 0
oddCnt dd 0
oddSum dd 0
oddAve dd 0
nineCnt dd 0
nineSum dd 0
nineAve dd 0

; ----------------------------------------------
;  Uninitialized Static Data Declarations.

section	.bss

;	Place data declarations for uninitialized data here...
;	(i.e., large arrays that are not initialized)


; *****************************************************************

section	.text
global _start
_start:

mov ecx, dword[length]
mov rsi, 0

mov eax, dword[lst+rsi*4] ;lst min
mov dword[lstMin], eax

mov r9d, dword[lst+rsi*4] ; lst max
mov dword[lstMax], r9d  
lp:
add r10d, dword[lst+rsi*4] ;sum

cmp eax, dword[lst+rsi*4]
jbe min

jmp Notmin
Notmin:
mov eax, dword[lst+rsi*4]
mov dword[lstMin], eax
min:

cmp r9d, dword[lst+rsi*4]
jae max

jmp NotMax
NotMax:
mov r9d, dword[lst+rsi*4]
mov dword[lstMax], r9d
max:
mov dword[lstSum], r10d 
add rsi, 1
loop lp
;finds the average
mov rax, 0
mov eax, dword[lstSum]
div dword[length]
mov dword[lstAve], eax

; finds medium
mov r11d, 2
mov r12d, 4

mov r10d, dword[lst]
mov rax, 0
mov r9d, dword[length]
mov eax, dword[r9d]
div r11d

add r10d, dword[lst+rax*4] ; addes the first half
add rax, 1 ; increments by one
add r10d, dword[lst+rax*4] ; adds the second half
dec r9d
add r10d, dword[lst+r9*4]; addes the last number into the reg

mov rax, 0
mov eax, dword[r10d]
div r12d
mov dword[estMed], eax








; *****************************************************************
;	Done, terminate program.

last:
	mov	rax, SYS_exit		; call call for exit (SYS_exit)
	mov	rdi, EXIT_SUCCESS	; return code of 0 (no error)
	syscall