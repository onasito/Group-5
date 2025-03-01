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

section .text
global _start
_start:

mov ecx, dword[length]      ; Load length into ecx (counter)
mov rsi, 0                  ; Initialize index to 0
mov eax, dword[lst+rsi*4]   ; Load first element to eax for min and max comparison
mov dword[lstMin], eax      ; Initialize lstMin with the first element
mov r9d, eax                ; Initialize lstMax with the first element
mov r10d, 0                 ; Initialize sum to 0

lp:
    ; Add current element to sum
    add r10d, dword[lst+rsi*4]

    ; Update min if current element is smaller
    cmp eax, dword[lst+rsi*4]
    jbe skipMin
    mov eax, dword[lst+rsi*4]
    mov dword[lstMin], eax
skipMin:

    ; Update max if current element is larger
    cmp r9d, dword[lst+rsi*4]
    jae skipMax
    mov r9d, dword[lst+rsi*4]
    mov dword[lstMax], r9d
skipMax:

    inc rsi                   ; Increment index
    loop lp                    ; Loop until ecx reaches 0

; Store the sum of the list
mov dword[lstSum], r10d

; Calculate average (sum / length)
mov eax, dword[lstSum]
mov ebx, dword[length]      ; Load length into ebx
div ebx                     ; Divide sum by length
mov dword[lstAve], eax      ; Store average in lstAve

; Calculate median estimate (simple approximation)
mov r10d, dword[lst]
mov r11d, dword[length]
mov r12d, 2

; Add first half of the elements for the median
mov r9d, dword[length]      ; Reload length into r9d for the median calculation
mov eax, r9d
div r12d                    ; Divide by 2 to get the midpoint
add r10d, dword[lst+rax*4]  ; Add the middle element(s)

; Calculate the median estimate
mov eax, r10d
div r12d
mov dword[estMed], eax      ; Store estimated median in estMed

; Terminate program
mov rax, SYS_exit
mov rdi, EXIT_SUCCESS
syscall
