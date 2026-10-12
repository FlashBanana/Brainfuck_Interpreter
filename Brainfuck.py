def interpret_brainfuck(code,brainfuckDebug):
    # Filtrating brainfuck commands
    code = "".join([c for c in code if c in "><+-.,[]"])
    
    memory = [0] * 30000  # Replicating brainfuck memory
    ptr = 0               # Pointer of memory
    ip = 0                # Instruction Pointer (brainfuck current instruction)
    
    # Pre-calculating the square parenthesis
    jump_map = {}
    stack = []
    for i, cmd in enumerate(code):
        if cmd == "[":
            stack.append(i)
        elif cmd == "]":
            start = stack.pop()
            jump_map[start] = i
            jump_map[i] = start
            
    output = []
    
    while ip < len(code):
        cmd = code[ip]
        
        if cmd == ">":
            ptr += 1 # adding value into current memory cell
        elif cmd == "<":
            ptr -= 1 # removing value into current memory cell
        elif cmd == "+":
            memory[ptr] = (memory[ptr] + 1) % 256  # Handling 8 bit overflow
        elif cmd == "-":
            memory[ptr] = (memory[ptr] - 1) % 256
        elif cmd == ".":
            output.append(chr(memory[ptr])) # Converting the cell value in ASCII and printing it
        elif cmd == ",":
            val = input("Input required: ")
            memory[ptr] = ord(val[0]) if val else 0
        elif cmd == "[":
            if memory[ptr] == 0:
                ip = jump_map[ip]
        elif cmd == "]":
            if memory[ptr] != 0:
                ip = jump_map[ip]
                
        ip += 1

    i = 0
    while i < 100:
        brainfuckDebug.append(memory[i])
        i += 1
    return "".join(output)

brainfuckDebug = []

brainfuckCode = """+++++++++++[>++++++<-]>++.
>++++[>++++++++<-]->[>+++<-]>+.
<++++++[>++<-]>+.
-----.
----.
+++++++.
-------.
>++++++++[>++++<-]>.
++++++[>++<-]>+.
-------------[>+<--]>[>+++<-]>+.
++++++++.
++++++.
+++.
---------.
+++++.
+.-[>+<--]>---------."""

res = interpret_brainfuck(brainfuckCode,brainfuckDebug)
print("Output:", res)
i = 0
print("\nMemory final dump: ",) # Printing memory
while i < len(brainfuckDebug):
    print("%03d" % brainfuckDebug[i],end=" ")
    i += 1
    if i % 12 == 0:
        print()
