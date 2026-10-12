import argparse


def interpret_brainfuck(code, brainfuckDebug):
  # Filtrating brainfuck commands
  code = "".join([c for c in code if c in "><+-.,[]"])

  memory = [0] * 30000  # Replicating brainfuck memory
  ptr = 0  # Pointer of memory
  ip = 0  # Instruction Pointer (brainfuck current instruction)

  # Pre-calculating the squared parenthesis
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
      ptr += 1  # adding value into current memory cell
    elif cmd == "<":
      ptr -= 1  # removing value into current memory cell
    elif cmd == "+":
      memory[ptr] = (memory[ptr] + 1) % 256  # Handling 8 bit overflow
    elif cmd == "-":
      memory[ptr] = (memory[ptr] - 1) % 256
    elif cmd == ".":
      output.append(chr(memory[ptr]))  # Converting the cell value in ASCII and printing it
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
  while i < 600: # Showing only 600 hundred cells for IDE limit 
    brainfuckDebug.append(memory[i])
    i += 1
  return "".join(output)

def createParser(parser):

    # Creating mutually exclusive group: the user has to insert 0 --file 0 --text
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-f", "--file", help="file containing Brainfuck code"
    )
    group.add_argument(
        "-t", "--text", help="Passing a brainfuck string"
    )

    # Adding an optional flag for debug
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Show memory final dump",
    )

    parser.add_argument(
        "-sd",
        "--save-debug",
        action="store_true",
        help="Saving memory final dump in memory in the file 'finalDump.txt'",
    )

def getcode(args):
    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            print(f"Error: file '{args.file}' not found")
            return ""
    elif args.text:
        return args.text
    return ""

def printDebug(args, brainfuck_debug):
    # Show only when there is the arg -d or --debug | -sd --save--debug
    if args.debug:
        print("\nMemory final dump (Console):")
        i = 0
        while i < len(brainfuck_debug):
            print("%03d" % brainfuck_debug[i], end=" ")
            i += 1
            if i % 12 == 0:
                print()
    if args.save_debug:
        try:
            with open("final_dump.txt", "w", encoding="utf-8") as dump_file:
                dump_file.write("Memory final dump:\n")
                i = 0
                while i < len(brainfuck_debug):
                    dump_file.write("%03d " % brainfuck_debug[i])
                    i += 1
                    if i % 12 == 0:
                        dump_file.write("\n")
            print("\n[Success] Successfully saved memory final dump in 'final_dump.txt'.")
        except IOError:
            print("\n[Error] Can't write in 'final_dump.txt'.")
def main():
  # Configuring cmd argument parser
  parser = argparse.ArgumentParser(description="Brainfuck interpreter in python")
  createParser(parser)

  #Setting args from parser
  args = parser.parse_args()

  # Getting the code based on argument passed
  code = getcode(args)

  # Executing interpreter
  brainfuck_debug = []
  res = interpret_brainfuck(code, brainfuck_debug)

  print("Output:", res)

  #Printing debug
  printDebug(args, brainfuck_debug)

if __name__ == "__main__":
  main()
