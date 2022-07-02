// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
(REPEAT)
    @8191 // 32 * 256 places to fill
    D=A   // Copy the value to place it in a counter
    @0
    M=D   // Counter is set on R0
    (FILL)
        @0
        D=M // Get counter value
        @REPEAT
        D;JLT // check if counter is negative (meaning we reached the end)
        @1    // If it isnt, we compute in R1 the address  
        M=D   // R1 = COUNTER + OFFSET (16384)
        @16384
        D=A
        @1
        M=M+D
        
        @KBD  // check for keypress
        D=M
        @WHITE
        D;JEQ // Equal to zero will jump to white. 
        @1    // Didn't jump = Pressed a key
        D=M   // Take the required address and place a -1 for black
        A=D
        M=-1
        @BLACK
        0;JEQ
        (WHITE)
        @1    // Jumped, meaning nothing was pressed
        D=M
        A=D
        M=0   // Place a 0
        (BLACK)
        @0
        M=M-1      // decrement the counter
        @FILL      // repeat
        0;JMP

    @REPEAT // Loop infinitely
    0;JMP