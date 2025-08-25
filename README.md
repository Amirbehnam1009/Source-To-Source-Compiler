# ⚙️ Source-to-Source Compiler

A source-to-source compiler that translates a **custom high-level programming language** (defined by grammar rules) into **C code**.  
Built using **Python** and **PLY (Python Lex-Yacc)**. 🚀

---

## 📖 Overview
This project implements a **compiler** for a custom-designed language as part of a **Compiler Design course project** at Amirkabir University of Technology.  

The compiler:
- Performs **lexical, syntax, and semantic analysis**.
- Translates programs written in the custom language into **C code**.
- Handles control structures (`if`, `while`, `switch-case`), arithmetic and relational operators, variable declarations, and print statements.
- Resolves **dangling else ambiguity** using the **nearest-if rule**.
- Generates **type-checked intermediate C code** with temporary variables and labels.

---

## 📝 Grammar (Simplified)
The source language is defined by the following grammar (subset shown):
``` bash
<program> ::= program <identifier> <declarations> <compound-statement>

<declarations> ::= var <declaration-list> | <empty>

<statement> ::= <identifier> := <expression>
| if <expression> then <statement> [else <statement>]
| while <expression> do <statement>
| print ( <expression> )
| switch <expression> of <cases> <default-case> done
| <compound-statement>
```


- **Data types**: `int`, `real`  
- **Operators**: Arithmetic (`+`, `-`, `*`, `/`, `mod`), Relational (`<`, `>`, `=`, `<>`, `<=`, `>=`), Logical (`and`, `or`, `not`)  
- **Keywords**: `program`, `var`, `begin`, `end`, `if`, `then`, `else`, `while`, `do`, `print`, `switch`, `case`, `default`, `done`

---

## 🏗️ Features
✅ **Lexical Analysis** → Recognizes identifiers, numbers, operators, and keywords  
✅ **Syntax Analysis** → Parses according to the defined grammar using PLY (Yacc)  
✅ **Semantic Analysis** → Type checking, scope rules, and error detection  
✅ **Code Generation** → Outputs valid **C code** in the following structure:

``` bash
#include <stdio.h>
int iid_1, iid_2, ...;
float fid_1, fid_2, ...;
int temp_int_1, temp_int_2, ...;
float temp_float_1, temp_float_2, ...;

int main() {
    statement_1;
label_1: statement_2;
    ...
    return 0;
}
```

* Supports goto labels for flow control.

* Temporary variables are auto-generated for intermediate computations.

* Prints integers using printf("%d\n", x);.

  ## 📂 Project Structure
``` bash
  📦 Source-To-Source-Compiler
 ┣ 📜 lexer.py         # Lexical analyzer using PLY
 ┣ 📜 parser.py        # Syntax analyzer (Yacc rules)
 ┣ 📜 semantic.py      # Type checking & semantic analysis
 ┣ 📜 codegen.py       # Code generation module (outputs C code)
 ┣ 📜 main.py          # Entry point to run the compiler
 ┣ 📜 examples/        # Example input programs in custom language
 ┣ 📜 outputs/         # Generated C code
 ┗ 📜 README.md        # Project documentation
```
## ▶️ How to Run

1. Clone the repository:
``` bash
git clone https://github.com/Amirbehnam1009/Source-To-Source-Compiler.git
cd Source-To-Source-Compiler
```

2. Install dependencies:
``` bash
pip install ply
```

3. Run the compiler on an example file:

``` bash
python main.py examples/sample.src
```

4. The generated C code will be saved in the outputs/ folder:
``` bash
gcc outputs/sample.c -o sample
./sample
```
## 📌 Example

### Input (custom language):
``` bash
 program test
var x, y : int;
begin
    x := 5;
    y := 10;
    if x < y then
        print(x)
    else
        print(y);
end
```

### Output (C code):
``` bash
#include <stdio.h>
int x, y;
int temp_int_1;

int main() {
    x = 5;
    y = 10;
    if (x < y) goto L1;
    goto L2;
L1: printf("%d\n", x);
    goto L3;
L2: printf("%d\n", y);
L3: ;
    return 0;
}
```
## 📊 Comparison & Notes

* Ambiguity handling: Resolved dangling else with nearest-if strategy.

* Type system: Ensures integers and reals are used consistently in operations.

* Error handling: Detects type mismatch, undeclared variables, and syntax errors.

* Extensibility: The grammar and code generation rules can be extended for more features.

## 🤝 Contributing

* Contributions are welcome! You can:

* Add new language constructs

* Improve error messages

* Enhance optimization in code generation

## 📜 License

This project is licensed under the MIT License.
