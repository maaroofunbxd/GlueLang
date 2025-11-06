#!/usr/bin/env python3
"""
GlueLang REPL - Python Edition
A clean, portable interactive shell for testing GlueLang commands
"""

import os
import sys
import subprocess
import tempfile
import signal
from pathlib import Path

# ANSI color codes
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[0;33m'
    BLUE = '\033[0;34m'
    MAGENTA = '\033[0;35m'
    CYAN = '\033[0;36m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_banner():
    """Print welcome banner"""
    print(f"{Colors.CYAN}{Colors.BOLD}")
    print("╔════════════════════════════════════════╗")
    print("║     GlueLang REPL v2.0 (Python)        ║")
    print("╚════════════════════════════════════════╝")
    print(f"{Colors.RESET}")
    print(f"{Colors.GREEN}Quick tips:{Colors.RESET}")
    print("  • Type GlueLang commands and press Enter")
    print("  • .help     - Show help")
    print("  • .examples - Show examples")
    print("  • .multi    - Multi-line mode (end with .end)")
    print("  • .exit     - Exit (or Ctrl+D, Ctrl+C)")
    print()

def print_help():
    """Print help message"""
    print(f"{Colors.YELLOW}GlueLang REPL Commands:{Colors.RESET}")
    print("  .help      - Show this help message")
    print("  .examples  - Show example GlueLang commands")
    print("  .multi     - Enter multi-line mode (end with .end)")
    print("  .clear     - Clear screen")
    print("  .exit      - Exit REPL")
    print()
    print("Just type any GlueLang command to execute it!")

def print_examples():
    """Print example commands"""
    print(f"{Colors.YELLOW}Example GlueLang Commands:{Colors.RESET}")
    print()
    print("1. Simple command:")
    print(f"   {Colors.CYAN}/bin/echo 'Hello, World!'{Colors.RESET}")
    print()
    print("2. Pipeline:")
    print(f"   {Colors.CYAN}/usr/bin/seq '1' '5' >>= /usr/bin/tac{Colors.RESET}")
    print()
    print("3. Store in variable:")
    print(f"   {Colors.CYAN}file f = /bin/echo 'test'{Colors.RESET}")
    print(f"   {Colors.CYAN}/bin/cat f{Colors.RESET}")
    print()
    print("4. While loop:")
    print(f"   {Colors.CYAN}import PATH{Colors.RESET}")
    print(f"   {Colors.CYAN}while{Colors.RESET}")
    print(f"   {Colors.CYAN}  str t = date '+%s' >>= awk '{{print $1%5}}'{Colors.RESET}")
    print(f"   {Colors.CYAN}  test t -ne 0{Colors.RESET}")
    print()
    print("See examples/ directory for more!")

def execute_glue(code, glue_bin):
    """Execute GlueLang code and return success status"""
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.glue', delete=False) as f:
            temp_file = f.name
            f.write(code)
        
        result = subprocess.run(
            [glue_bin, temp_file],
            capture_output=True,
            text=True
        )
        
        # Print stdout
        if result.stdout:
            print(result.stdout, end='')
        
        # Print stderr with color
        if result.stderr:
            if result.returncode != 0:
                print(f"{Colors.RED}Error:{Colors.RESET}", file=sys.stderr)
            else:
                print(f"{Colors.YELLOW}Warning:{Colors.RESET}", file=sys.stderr)
            print(result.stderr, end='', file=sys.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"{Colors.RED}Error executing: {e}{Colors.RESET}", file=sys.stderr)
        return False
    finally:
        try:
            os.unlink(temp_file)
        except:
            pass

def read_multiline():
    """Read multiple lines of input"""
    print(f"{Colors.YELLOW}Multi-line mode (type .end to execute, .cancel to abort){Colors.RESET}")
    lines = []
    line_num = 1
    
    try:
        while True:
            line = input(f"{Colors.GREEN}  {line_num}> {Colors.RESET}")
            if line == ".end":
                break
            elif line == ".cancel":
                print(f"{Colors.RED}Cancelled{Colors.RESET}")
                return None
            lines.append(line)
            line_num += 1
    except (EOFError, KeyboardInterrupt):
        print()
        return None
    
    return '\n'.join(lines)

def main():
    """Main REPL loop"""
    # Find glue binary
    script_dir = Path(__file__).parent
    glue_bin = script_dir / 'glue'
    
    if not glue_bin.exists() or not os.access(glue_bin, os.X_OK):
        print(f"{Colors.RED}Error: glue binary not found or not executable{Colors.RESET}")
        print("Run 'make' first to build GlueLang")
        sys.exit(1)
    
    glue_bin = str(glue_bin)
    
    # Setup signal handlers
    def signal_handler(sig, frame):
        print(f"\n{Colors.BLUE}Goodbye!{Colors.RESET}")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Print banner
    print_banner()
    
    # Main loop
    cmd_count = 1
    history = []
    
    # Try to use readline for history
    try:
        import readline
        readline.parse_and_bind('tab: complete')
    except ImportError:
        pass
    
    while True:
        try:
            # Read input
            prompt = f"{Colors.GREEN}glue[{cmd_count}]> {Colors.RESET}"
            user_input = input(prompt).strip()
            
            # Skip empty input
            if not user_input:
                continue
            
            # Handle special commands
            if user_input in ['.exit', '.quit', 'exit', 'quit']:
                print(f"{Colors.BLUE}Goodbye!{Colors.RESET}")
                break
            
            elif user_input in ['.help', 'help']:
                print_help()
                continue
            
            elif user_input == '.examples':
                print_examples()
                continue
            
            elif user_input == '.multi':
                multiline = read_multiline()
                if multiline:
                    user_input = multiline
                else:
                    continue
            
            elif user_input == '.clear':
                os.system('clear' if os.name != 'nt' else 'cls')
                continue
            
            elif user_input == '.history':
                print(f"{Colors.YELLOW}Command History:{Colors.RESET}")
                for i, cmd in enumerate(history[-20:], 1):
                    print(f"  {i:2d}  {cmd}")
                continue
            
            elif user_input.startswith('.'):
                print(f"{Colors.RED}Unknown command: {user_input}{Colors.RESET}")
                print("Type .help for available commands")
                continue
            
            # Add to history
            history.append(user_input)
            
            # Execute GlueLang code
            execute_glue(user_input, glue_bin)
            
            cmd_count += 1
            
        except EOFError:
            print()
            print(f"{Colors.BLUE}Goodbye!{Colors.RESET}")
            break
        except KeyboardInterrupt:
            print()
            continue

if __name__ == '__main__':
    main()

