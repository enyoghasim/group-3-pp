"""
Library Management System
=========================
A terminal-based library management system using Object-Oriented Programming.

Demonstrates:
    - Abstract base classes and abstract methods
    - Inheritance and method overriding (polymorphism)
    - Encapsulation via private attributes with property accessors
    - Error handling throughout user interaction
"""

from abc import ABC, abstractmethod
import os
import sys


# ---------------------------------------------------------------------------
# ANSI colour & style helpers (no external dependencies)
# ---------------------------------------------------------------------------
class Style:
    """ANSI escape codes for terminal colours and formatting."""

    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"

    # Foreground colours
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"

    # Background colours
    BG_BLUE = "\033[44m"

    # Cursor helpers
    HIDE_CURSOR = "\033[?25l"
    SHOW_CURSOR = "\033[?25h"
    CLEAR_LINE  = "\033[2K"

    @staticmethod
    def c(text: str, *codes: str) -> str:
        """Wrap *text* with one or more ANSI codes."""
        return "".join(codes) + text + Style.RESET

    @staticmethod
    def move_up(n: int = 1) -> str:
        """ANSI code to move cursor up *n* lines."""
        return f"\033[{n}A" if n else ""


# ---------------------------------------------------------------------------
# Arrow-key menu selector (cross-platform, no external dependencies)
# ---------------------------------------------------------------------------
def _read_key() -> str:
    """Read a single keypress from stdin (raw mode).

    Works on Windows (msvcrt) and Unix/macOS (tty + termios).
    Returns 'up', 'down', 'enter', or the character pressed.
    """
    if os.name == "nt":                         # ---- Windows ----
        import msvcrt
        ch = msvcrt.getch()
        if ch in (b"\r", b"\n"):
            return "enter"
        if ch in (b"\x00", b"\xe0"):            # special / arrow key prefix
            ch2 = msvcrt.getch()
            if ch2 == b"H":
                return "up"
            if ch2 == b"P":
                return "down"
            return "special"
        return ch.decode("utf-8", errors="replace")
    else:                                        # ---- Unix / macOS ----
        import tty
        import termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch in ("\r", "\n"):
                return "enter"
            if ch == "\x1b":                     # escape sequence
                seq = sys.stdin.read(2)
                if seq == "[A":
                    return "up"
                if seq == "[B":
                    return "down"
                return "esc"
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)


def arrow_menu(title: str, options: list[str]) -> int:
    """Display an interactive menu and return the selected index.

    The user navigates with ↑ / ↓ arrow keys and confirms with Enter.
    """
    selected = 0
    count = len(options)

    def _draw(first_draw: bool = False) -> None:
        """Render all menu options, highlighting the selected one."""
        if not first_draw:
            # Move cursor back up to overwrite previous render
            sys.stdout.write(Style.move_up(count))
        for i, opt in enumerate(options):
            sys.stdout.write(Style.CLEAR_LINE)
            if i == selected:
                line = Style.c(f"  ▸ {opt}", Style.BOLD, Style.CYAN)
            else:
                line = Style.DIM + f"    {opt}" + Style.RESET
            sys.stdout.write(line + "\n")
        sys.stdout.flush()

    # Print title and initial draw
    print(title)
    sys.stdout.write(Style.HIDE_CURSOR)
    _draw(first_draw=True)

    try:
        while True:
            key = _read_key()
            if key == "up":
                selected = (selected - 1) % count
            elif key == "down":
                selected = (selected + 1) % count
            elif key == "enter":
                break
            _draw()
    finally:
        sys.stdout.write(Style.SHOW_CURSOR)
        sys.stdout.flush()

    return selected


# ---------------------------------------------------------------------------
# Abstract base class
# ---------------------------------------------------------------------------
class Book(ABC):
    """Abstract base class representing a generic book.

    Attributes are kept private and exposed through read-only properties
    to enforce encapsulation.
    """

    def __init__(self, title: str, author: str, year: int) -> None:
        self.__title = title
        self.__author = author
        self.__year = year

    # --- read-only properties (encapsulation) ---

    @property
    def title(self) -> str:
        """Return the book title."""
        return self.__title

    @property
    def author(self) -> str:
        """Return the book author."""
        return self.__author

    @property
    def year(self) -> int:
        """Return the publication year."""
        return self.__year

    @abstractmethod
    def display_info(self) -> str:
        """Return a formatted string with full book details.

        Must be implemented by every concrete subclass.
        """

    @abstractmethod
    def book_type_label(self) -> str:
        """Return a coloured tag identifying the book type."""

    @abstractmethod
    def extra_detail(self) -> str:
        """Return a short string with the type-specific detail."""

    def __str__(self) -> str:
        return self.display_info()


# ---------------------------------------------------------------------------
# Concrete subclasses
# ---------------------------------------------------------------------------
class EBook(Book):
    """An electronic book with an associated file size."""

    def __init__(
        self, title: str, author: str, year: int, file_size_mb: float
    ) -> None:
        super().__init__(title, author, year)
        self.__file_size_mb = file_size_mb

    @property
    def file_size_mb(self) -> float:
        """Return the file size in megabytes."""
        return self.__file_size_mb

    def book_type_label(self) -> str:
        """Return a coloured type tag."""
        return Style.c(" EBook ", Style.BOLD, Style.CYAN)

    def extra_detail(self) -> str:
        """Return the type-specific detail string."""
        return f"{self.file_size_mb} MB"

    def display_info(self) -> str:
        return (
            f"{self.book_type_label()}  Title: {self.title} | "
            f"Author: {self.author} | Year: {self.year} | "
            f"Size: {self.extra_detail()}"
        )


class PrintedBook(Book):
    """A physical printed book with a page count."""

    def __init__(
        self, title: str, author: str, year: int, number_of_pages: int
    ) -> None:
        super().__init__(title, author, year)
        self.__number_of_pages = number_of_pages

    @property
    def number_of_pages(self) -> int:
        """Return the number of pages."""
        return self.__number_of_pages

    def book_type_label(self) -> str:
        """Return a coloured type tag."""
        return Style.c(" Print ", Style.BOLD, Style.YELLOW)

    def extra_detail(self) -> str:
        """Return the type-specific detail string."""
        return f"{self.number_of_pages} pp"

    def display_info(self) -> str:
        return (
            f"{self.book_type_label()}  Title: {self.title} | "
            f"Author: {self.author} | Year: {self.year} | "
            f"Pages: {self.extra_detail()}"
        )


# ---------------------------------------------------------------------------
# Library — stores and manages a collection of books
# ---------------------------------------------------------------------------
class Library:
    """Manages a list of Book objects.

    Provides methods to add books, display all books, and search by title.
    """

    def __init__(self) -> None:
        self.__books: list[Book] = []

    def add_book(self, book: Book) -> None:
        """Add a book to the library collection."""
        self.__books.append(book)

    def list_books(self) -> list[Book]:
        """Return a shallow copy of all books in the library."""
        return self.__books.copy()

    def delete_book_by_index(self, index: int) -> Book:
        """Delete and return a book by zero-based index.

        Raises IndexError if the index is out of range.
        """
        return self.__books.pop(index)

    # ---- table formatting helpers ----

    @staticmethod
    def _visible_len(text: str) -> int:
        """Return the length of *text* ignoring ANSI escape sequences."""
        import re
        return len(re.sub(r"\033\[[0-9;]*m", "", text))

    @staticmethod
    def _pad(text: str, width: int) -> str:
        """Pad *text* to *width* visible characters (ANSI-aware)."""
        import re
        visible = len(re.sub(r"\033\[[0-9;]*m", "", text))
        return text + " " * max(0, width - visible)

    def _print_table(self, books: list["Book"]) -> None:
        """Print *books* in a neat, coloured table."""
        # Build rows: (#, Type, Title, Author, Year, Extra)
        rows: list[tuple[str, str, str, str, str, str]] = []
        for i, book in enumerate(books, start=1):
            rows.append((
                str(i),
                book.book_type_label(),
                book.title,
                book.author,
                str(book.year),
                book.extra_detail(),
            ))

        # Column headers
        headers = ("#", "Type", "Title", "Author", "Year", "Detail")

        # Compute column widths (max of header vs data, ANSI-aware)
        widths = [len(h) for h in headers]
        for row in rows:
            for col, cell in enumerate(row):
                widths[col] = max(widths[col], self._visible_len(cell))

        # Separator line
        sep = Style.DIM + "─" + "─┬─".join("─" * w for w in widths) + "─" + Style.RESET

        # Header row
        hdr_cells = [
            Style.c(h.ljust(widths[ci]), Style.BOLD, Style.GREEN)
            for ci, h in enumerate(headers)
        ]
        hdr_line = " " + " │ ".join(hdr_cells) + " "

        print()
        print(Style.c(" 📚  Library Collection ", Style.BOLD, Style.MAGENTA))
        print(sep)
        print(hdr_line)
        print(sep)

        # Data rows
        for row in rows:
            cells = [self._pad(cell, widths[ci]) for ci, cell in enumerate(row)]
            print(" " + " │ ".join(cells) + " ")

        print(sep)
        print(Style.DIM + f"  {len(books)} book(s) total" + Style.RESET)
        print()

    def display_all_books(self) -> None:
        """Print every book using polymorphic display_info() calls."""
        if not self.__books:
            print(Style.c("\n  The library is empty.\n", Style.YELLOW))
            return
        self._print_table(self.__books)

    def search_by_title(self, query: str) -> list[Book]:
        """Return books whose title contains the query (case-insensitive)."""
        query_lower = query.lower()
        return [
            book for book in self.__books
            if query_lower in book.title.lower()
        ]


# ---------------------------------------------------------------------------
# Helper — input validation
# ---------------------------------------------------------------------------
def read_int(prompt: str) -> int:
    """Prompt the user until a valid integer is entered."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("  Invalid input. Please enter a whole number.")


def read_float(prompt: str) -> float:
    """Prompt the user until a valid float is entered."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("  Invalid input. Please enter a number.")


# ---------------------------------------------------------------------------
# Menu actions
# ---------------------------------------------------------------------------
def add_book_menu(library: Library) -> None:
    """Walk the user through adding a new book."""
    print(Style.DIM + "  Use ↑/↓ and Enter. Select Back to return." + Style.RESET)
    book_type = arrow_menu(
        Style.c("\n  Select book type:", Style.BOLD, Style.MAGENTA),
        ["📱  EBook", "📕  Printed Book", "↩️  Back"],
    )

    if book_type == 2:
        print(Style.c("  Back to main menu.\n", Style.YELLOW))
        return

    title  = input(Style.c("  ▸ ", Style.GREEN) + "Title : ").strip()
    author = input(Style.c("  ▸ ", Style.GREEN) + "Author: ").strip()
    year   = read_int(Style.c("  ▸ ", Style.GREEN) + "Year  : ")

    if book_type == 0:
        file_size = read_float(Style.c("  ▸ ", Style.GREEN) + "File size (MB): ")
        library.add_book(EBook(title, author, year, file_size))
    else:
        pages = read_int(Style.c("  ▸ ", Style.GREEN) + "Number of pages: ")
        library.add_book(PrintedBook(title, author, year, pages))

    print(Style.c(f'  ✓ "{title}" added successfully.', Style.GREEN))


def search_menu(library: Library) -> None:
    """Search for books by title and display matching results."""
    print(Style.DIM + "  Press Enter on empty input to go back." + Style.RESET)
    query = input(
        Style.c("\n  🔍 ", Style.CYAN) + "Enter title to search (or press Enter to go back): "
    ).strip()
    if not query:
        print(Style.c("  Back to main menu.\n", Style.YELLOW))
        return

    results = library.search_by_title(query)
    if results:
        library._print_table(results)
    else:
        print(Style.c("  No books found matching that title.", Style.YELLOW))
        print()


def delete_book_menu(library: Library) -> None:
    """Delete one book using arrow-key selection."""
    books = library.list_books()
    if not books:
        print(Style.c("\n  No books to delete. The library is empty.\n", Style.YELLOW))
        return

    print(Style.DIM + "  Use ↑/↓ and Enter. Select Back to return." + Style.RESET)

    options = [
        f"{book.title} — {book.author} ({book.year})"
        for book in books
    ]
    options.append("↩️  Back")

    selected = arrow_menu(
        Style.c("\n  Select a book to delete:", Style.BOLD, Style.RED),
        options,
    )

    if selected == len(options) - 1:
        print(Style.c("  Back to main menu.\n", Style.YELLOW))
        return

    removed = library.delete_book_by_index(selected)
    print(Style.c(
        f'  ✓ Deleted "{removed.title}" by {removed.author}.\n',
        Style.GREEN,
    ))


def hints_menu() -> None:
    """Show a basic overview of how the system works."""
    print(Style.c("\n  💡 System Hints", Style.BOLD, Style.MAGENTA))
    print(Style.DIM + "  Overview:" + Style.RESET)
    print("    • Store books as EBook or Printed Book objects")
    print("    • Use arrow keys (↑/↓) to move through menu options")
    print("    • Press Enter to select an option")
    print("    • Add, view, search, and delete books from the library")
    print("    • Use 'Back' in submenus to return safely")

    print(Style.DIM + "\n  Features:" + Style.RESET)
    print("    • Display all books in a formatted table")
    print("    • Search by title (case-insensitive)")
    print("    • Delete a selected book from the collection")
    print()


# ---------------------------------------------------------------------------
# Main program loop
# ---------------------------------------------------------------------------
def main() -> None:
    """Entry point — runs the interactive menu loop."""
    # Enable ANSI colour support on Windows 10+
    if os.name == "nt":
        os.system("")

    library = Library()

    # Pre-loaded sample books so the library isn't empty on first run
    library.add_book(EBook("Clean Code", "Robert C. Martin", 2008, 4.5))
    library.add_book(PrintedBook("The Pragmatic Programmer", "Andy Hunt", 1999, 352))
    library.add_book(EBook("Python Crash Course", "Eric Matthes", 2015, 8.2))
    library.add_book(PrintedBook("Design Patterns", "Gang of Four", 1994, 395))

    banner = Style.c(
        " 📖  Library Management System ", Style.BOLD, Style.MAGENTA
    )
    line = Style.DIM + "─" * 40 + Style.RESET
    print(f"\n{line}")
    print(f"  {banner}")
    print(f"{line}\n")

    if os.name == "nt":
        os_hint = "Windows: use ↑/↓ keys in CMD/PowerShell, then Enter"
    elif os.name == "posix":
        os_hint = "macOS/Linux: use ↑/↓ keys in Terminal, then Enter"
    else:
        os_hint = "Use ↑/↓ keys to navigate and Enter to select"

    print(Style.c("  Home usage hint:", Style.BOLD, Style.CYAN))
    print(Style.DIM + f"  {os_hint}" + Style.RESET)
    print(Style.DIM + "  Open 'Hints / How it works' for a quick overview.\n" + Style.RESET)

    menu_options = [
        "📚  Display all books",
        "➕  Add a book",
        "🗑️  Delete a book",
        "🔍  Search by title",
        "💡  Hints / How it works",
        "🚪  Exit",
    ]

    while True:
        choice = arrow_menu(
            Style.c("  Choose an action:", Style.BOLD, Style.GREEN),
            menu_options,
        )

        if choice == 0:
            library.display_all_books()
        elif choice == 1:
            add_book_menu(library)
        elif choice == 2:
            delete_book_menu(library)
        elif choice == 3:
            search_menu(library)
        elif choice == 4:
            hints_menu()
        elif choice == 5:
            print(Style.c("\n  👋 Goodbye!\n", Style.MAGENTA, Style.BOLD))
            break


if __name__ == "__main__":
    main()
