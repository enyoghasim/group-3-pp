# Library Management System (Terminal-Based, OOP)

A clean, cross-platform Python Library Management System built for OOP coursework.
It demonstrates abstraction, encapsulation, inheritance, polymorphism, and error handling using only the Python standard library.

---

## Quick Start

### 1) Run the app

```bash
python3 library_management.py
```

If `python3` is not available on your machine, use:

```bash
python library_management.py
```

### 2) Navigate

- Use **↑ / ↓** arrow keys to move in menus
- Press **Enter** to select
- Use **Back** options in submenus to return safely

---

## OS Compatibility

The app is designed to run across operating systems with no third-party package installation.

- **Windows:** uses standard-library `msvcrt` for arrow key reading
- **macOS / Linux:** uses standard-library `tty` + `termios`
- **Styling:** ANSI color output is enabled in code (including Windows support)

> Note: Arrow navigation works in regular terminals (PowerShell/CMD/Terminal/iTerm/Linux shells). Some limited IDE consoles may not fully support raw key input.

---

## Main Features

| Feature              | What it does                                              |
| -------------------- | --------------------------------------------------------- |
| Display all books    | Shows all books in a formatted, colorized table           |
| Add a book           | Adds either an `EBook` or `PrintedBook`                   |
| Delete a book        | Lets user select a book and remove it from the collection |
| Search by title      | Case-insensitive title matching                           |
| Hints / How it works | Shows a quick overview for first-time users               |
| Back navigation      | Available in relevant submenu flows                       |
| Input validation     | Prevents invalid numeric values for year/pages/file size  |

---

## Assignment Coverage Checklist

This section maps the assignment request directly to the implementation.

### Abstract class `Book`

- Implemented as an abstract base class using `ABC`
- Contains private attributes:
  - `__title`
  - `__author`
  - `__year`
- Declares abstract method `display_info()`

### Subclasses with extra attributes

- `EBook(Book)`
  - Extra private attribute: `__file_size_mb`
  - Overrides `display_info()`
- `PrintedBook(Book)`
  - Extra private attribute: `__number_of_pages`
  - Overrides `display_info()`

### Store multiple books in a list

- `Library` class manages `__books: list[Book]`
- Includes preloaded sample books at startup

### Display all books

- `Library.display_all_books()` prints all books in a formatted table

### Search by title

- `Library.search_by_title(query)` performs case-insensitive search

### Demonstrate polymorphism

- Methods like `display_info()`, `book_type_label()`, and `extra_detail()` are called through `Book` references
- Runtime behavior differs by actual object type (`EBook` vs `PrintedBook`)

### Proper encapsulation

- All core fields are private (`__name` style)
- Exposed through controlled read-only properties

### Error handling and clean documentation

- Numeric inputs validated with retry loops (`read_int`, `read_float`)
- Safe menu flow with Back options and graceful user messages
- File includes structured comments and docstrings

---

## System Design (High Level)

### Core classes

- **`Book` (abstract):** shared structure and interface for all book types
- **`EBook`:** book + file size metadata
- **`PrintedBook`:** book + page count metadata
- **`Library`:** collection manager (add, list, search, delete)
- **`Style`:** ANSI color and terminal cursor helpers

### Flow summary

1. App starts, enables terminal styling support, and preloads sample books
2. Home menu appears with arrow-key navigation
3. User selects actions: display, add, delete, search, or hints
4. Submenus support Back behavior

---

## Menu Guide

### Home menu

- `Display all books`
- `Add a book`
- `Delete a book`
- `Search by title`
- `Hints / How it works`
- `Exit`

### Add flow

- Select `EBook` or `PrintedBook`
- Enter common fields: title, author, year
- Enter type-specific field:
  - `EBook` → file size (MB)
  - `PrintedBook` → number of pages
- Includes `Back`

### Delete flow

- Shows current books as selectable options
- Select one to delete
- Includes `Back`

### Search flow

- Enter title text
- Empty input returns to main menu

---

## File Structure

```text
project/
├── library_management.py   # Main application source code
└── README.md               # Project documentation
```

---

## Notes for Group Members

- Keep the project dependency-free (standard library only)
- Preserve OOP structure (`Book` → subclasses → `Library` manager)
- If adding features, keep navigation consistent with arrow-key menu style
- Test in a real terminal for best arrow-key behavior

---

## Suggested Test Scenarios

1. Display preloaded books
2. Add one EBook and one PrintedBook
3. Search with upper/lower case variations
4. Delete a selected book and verify it is removed
5. Use Back options in all submenus
6. Open Hints and verify overview text appears

---

## Authoring Goal

This project is intentionally kept simple, readable, and well-documented so it can be presented clearly in an academic setting and easily maintained by a team.
