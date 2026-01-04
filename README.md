# Interactive Python Shell

This project implements a cross-platform shell environment that integrates a standard command-line interface with a graphical file browser. It uses a split-pane layout to provide simultaneous views of the file system and the terminal emulator.

The application handles both built-in shell commands (like `cd`, `ls`, `history`) and external system processes. It features a custom command execution engine capable of handling pipelines, standard output redirection, and history persistence compatible with standard shell environments.

### Technical Implementation

The codebase utilizes several specific implementation patterns to bridge the gap between a GUI event loop and linear shell command execution:

* **Standard Stream Redirection**: The [executor.py](./executor.py) module captures output from built-in commands by temporarily redirecting `sys.stdout` to an instance of `io.StringIO`. This allows internal Python functions to behave like system executables within the pipeline. [Documentation on io.StringIO](https://docs.python.org/3/library/io.html#io.StringIO).
* **Subprocess Pipelining**: External command chaining is handled by manually managing input/output buffers between `subprocess.run` calls. The output of one process is captured, decoded, and passed as the `input` argument to the next process in the chain. [Documentation on subprocess management](https://docs.python.org/3/library/subprocess.html).
* **Manual Tokenization**: rather than using `shlex`, [parser.py](./parser.py) implements a custom state-machine parser to handle nested quotes and escape characters, ensuring that arguments with spaces are preserved correctly during command execution.
* **Virtual Event Binding**: The [gui.py](./gui.py) relies heavily on Tkinter event bindings (`<Return>`, `<Double-1>`) to map user interactions to the `CommandExecutor` logic, keeping the UI responsive during command entry. [Documentation on Tkinter events](https://docs.python.org/3/library/tkinter.html#bindings-and-events).

### Technologies and Libraries

This project relies on the standard Python library, minimizing external dependencies to ensure portability.

* **[Tkinter](https://docs.python.org/3/library/tkinter.html)**: The standard Python interface to the Tcl/Tk GUI toolkit. It handles the windowing, widget rendering (Treeview, PanedWindow), and main event loop.
* **[Monaco Font](https://en.wikipedia.org/wiki/Monaco_(typeface))**: Detected and applied specifically for macOS environments in [config.py](./config.py) to maintain a native terminal aesthetic.
* **[Courier Font](https://en.wikipedia.org/wiki/Courier_(typeface))**: Used as the fallback monospace font for non-macOS platforms.
* **[OS Module](https://docs.python.org/3/library/os.html)**: Used extensively for filesystem traversal, environment variable access (`HISTFILE`, `PATH`), and process management.

### Project Structure

The project is structured as a flat Python package.

```text
.
├── commands.py
├── config.py
├── executor.py
├── gui.py
├── history_manager.py
├── main.py
└── parser.py
