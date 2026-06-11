import sys

# High-tech cyber colors
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

CYAN = "\033[36m"
MAGENTA = "\033[35m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
GRAY = "\033[90m"

# Safe terminal reconfiguration for UTF-8
try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

def print_banner():
    banner = f"""
{CYAN}    __    __  __ _   __ ___  ____ 
   / /   / / / // | / //   |/ __ \\
  / /   / / / //  |/ // /| // /_/ /
 / /___/ /_/ // /|  // ___// _, _/ 
/_____/\\____//_/ |_//_/  |_/_/ |_| {RESET} {GRAY}v0.1.2{RESET}
{DIM}================================================={RESET}
{CYAN}{BOLD}>> AI-Powered High-Tech API Testing Framework{RESET}
"""
    print(banner)

def success(msg):
    try:
        print(f"{GREEN}{BOLD}✔{RESET} {msg}")
    except UnicodeEncodeError:
        print(f"{GREEN}[OK]{RESET} {msg}")

def error(msg):
    try:
        print(f"{RED}{BOLD}✖{RESET} {msg}")
    except UnicodeEncodeError:
        print(f"{RED}[ERROR]{RESET} {msg}")

def info(msg):
    try:
        print(f"{BLUE}{BOLD}→{RESET} {msg}")
    except UnicodeEncodeError:
        print(f"{BLUE}->{RESET} {msg}")

def warn(msg):
    try:
        print(f"{YELLOW}{BOLD}⚠{RESET} {msg}")
    except UnicodeEncodeError:
        print(f"{YELLOW}[WARN]{RESET} {msg}")

def print_panel(title, content_lines, border_color=CYAN):
    # Determine max length
    max_len = len(title)
    for line in content_lines:
        # Clean colors for length check
        clean_line = line
        for c in [RESET, BOLD, DIM, CYAN, MAGENTA, GREEN, RED, YELLOW, BLUE, GRAY]:
            clean_line = clean_line.replace(c, "")
        max_len = max(max_len, len(clean_line))

    width = max_len + 4
    
    # Draw top border
    try:
        top = f"┌── {title} " + "─" * (width - len(title) - 5) + "┐"
        print(f"{border_color}{top}{RESET}")
    except UnicodeEncodeError:
        print(f"{border_color}+-- {title} " + "-" * (width - len(title) - 5) + "+{RESET}")

    for line in content_lines:
        clean_line = line
        for c in [RESET, BOLD, DIM, CYAN, MAGENTA, GREEN, RED, YELLOW, BLUE, GRAY]:
            clean_line = clean_line.replace(c, "")
        padding = " " * (width - len(clean_line) - 2)
        try:
            print(f"{border_color}│{RESET} {line}{padding} {border_color}│{RESET}")
        except UnicodeEncodeError:
            print(f"{border_color}|{RESET} {line}{padding} {border_color}|{RESET}")

    try:
        bottom = "└" + "─" * (width - 1) + "┘"
        print(f"{border_color}{bottom}{RESET}")
    except UnicodeEncodeError:
        print(f"{border_color}+" + "-" * (width - 1) + "+{RESET}")

def print_table(headers, rows):
    if not rows:
        return
    # Calculate column widths
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            # Clean colors for length check
            clean_val = str(val)
            for c in [RESET, BOLD, DIM, CYAN, MAGENTA, GREEN, RED, YELLOW, BLUE, GRAY]:
                clean_val = clean_val.replace(c, "")
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], len(clean_val))
            else:
                col_widths.append(len(clean_val))

    # Print top border
    try:
        top_border = "┌" + "┬".join("─" * (w + 2) for w in col_widths) + "┐"
        print(f"{GRAY}{top_border}{RESET}")
    except UnicodeEncodeError:
        print(f"{GRAY}+" + "+".join("-" * (w + 2) for w in col_widths) + "+{RESET}")

    # Print headers
    header_str = ""
    for i, h in enumerate(headers):
        header_str += f"│ {CYAN}{BOLD}{h:<{col_widths[i]}}{RESET} "
    try:
        header_str += "│"
        print(header_str)
    except UnicodeEncodeError:
        header_str = header_str.replace("│", "|")
        print(header_str)

    # Print divider
    try:
        div_border = "├" + "┼".join("─" * (w + 2) for w in col_widths) + "┤"
        print(f"{GRAY}{div_border}{RESET}")
    except UnicodeEncodeError:
        print(f"{GRAY}+" + "+".join("-" * (w + 2) for w in col_widths) + "+{RESET}")

    # Print rows
    for row in rows:
        row_str = ""
        for i, val in enumerate(row):
            str_val = str(val)
            clean_val = str_val
            for c in [RESET, BOLD, DIM, CYAN, MAGENTA, GREEN, RED, YELLOW, BLUE, GRAY]:
                clean_val = clean_val.replace(c, "")
            # Pad value accounting for ANSI escapes in str_val
            pad_len = col_widths[i] - len(clean_val)
            row_str += f"│ {str_val}{' ' * pad_len} "
        try:
            row_str += "│"
            print(row_str)
        except UnicodeEncodeError:
            row_str = row_str.replace("│", "|")
            print(row_str)

    # Print bottom border
    try:
        bottom_border = "└" + "┴".join("─" * (w + 2) for w in col_widths) + "┘"
        print(f"{GRAY}{bottom_border}{RESET}")
    except UnicodeEncodeError:
        print(f"{GRAY}+" + "+".join("-" * (w + 2) for w in col_widths) + "+{RESET}")

def print_progress_bar(current, total, bar_length=30):
    fraction = current / total
    arrow = "█" * int(fraction * bar_length)
    spaces = " " * (bar_length - len(arrow))
    percent = int(fraction * 100)
    try:
        sys.stdout.write(f"\r{GRAY}[{CYAN}{arrow}{spaces}{GRAY}] {CYAN}{percent}%{RESET} ({current}/{total})")
        sys.stdout.flush()
    except UnicodeEncodeError:
        arrow_alt = "=" * int(fraction * bar_length)
        sys.stdout.write(f"\r[{arrow_alt}{spaces}] {percent}% ({current}/{total})")
        sys.stdout.flush()
    if current == total:
        print()