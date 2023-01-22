# __Write documentation for your code with mkdocs__

## __Steps__

1. Create a new conda environment named `dev_docs`
2. Activate the environment
3. Install the Python packages `mkdocs`, `mkdocstrings`, `mkdocs-material`, `mkdocs-gen-files`, `mkdocs-literate-nav` and `mkdocs-section-index`
4. Create a new mkdocs project
5. Edit the `mkdocs.yml` file
6. Create the `docs/gen_ref_pages.py` file
7. Create the `src/project` folder
8. Create the `src/project/amet.py` file
9. Create the `src/project/dolor.py` file
10. Create the `src/project/__init__.py` file
11. Build the documentation
12. Serve the documentation
13. Create the `requirements.txt` file
14. Create the `environment.yml` file
15. Deactivate the environment
16. Create a new git repository
17. Add the files to the git repository
18. Commit the files to the git repository
19. Push the files to the git repository

## Code snippets

```bash
# Create a new conda environment and install the packages
conda create -n dev_docs python=3.8 -y
conda activate dev_docs
pip install mkdocs "mkdocstrings[python]" mkdocs-material mkdocs-gen-files mkdocs-literate-nav mkdocs-section-index
```

```bash
# Create a new mkdocs project
mkdocs new .
```

```yml
# Update the mkdocs.yml file

site_name: Calculation Docs

theme:
  name: "material"
nav:
# rest of the navigation...
- Code Reference: reference/ 
plugins:
- search  # 
- gen-files:
    scripts:
    - docs/gen_ref_pages.py
- literate-nav:
    nav_file: SUMMARY.md
- section-index
- mkdocstrings
```

```python
# Create and update docs/gen_ref_pages.py
"""Generate the code reference pages and navigation."""

from pathlib import Path

import mkdocs_gen_files

nav = mkdocs_gen_files.Nav()

for path in sorted(Path("src").rglob("*.py")):
    module_path = path.relative_to("src").with_suffix("")
    doc_path = path.relative_to("src").with_suffix(".md")
    full_doc_path = Path("reference", doc_path)
    parts = tuple(module_path.parts)
    if parts[-1] == "__init__":
        parts = parts[:-1]
        doc_path = doc_path.with_name("index.md")
        full_doc_path = full_doc_path.with_name("index.md")
    elif parts[-1] == "__main__":
        continue
    nav[parts] = doc_path.as_posix()
    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        ident = ".".join(parts)
        fd.write(f"::: src.{ident}")                                # src. is the root of the source code.
                                                                    # this you have to change to navigate the root of the package.
    mkdocs_gen_files.set_edit_path(full_doc_path, path)
with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
```

```python
# Create and update src/project/amet.py

def amet(name: str)->str:
    """Give a name

    Args:
        name (str): a name

    Returns:
        str: my name is name
    """
    output: str = f"My name is {name}."
    return output


class MyCalss:
    """This is my class"""
    def __init__(self, alpha: float = 0.5) -> None:
        """take alpha

        Args:
            alpha (float, optional): store alpha in self. Defaults to 0.5.
        """
        self.alpha: float = alpha
    def double_alpha(self) -> float:
        """double alpha

        Returns:
            float: double alpha
        """
        return 2 * self.alpha
```

```python
# Create and update src/project/dolor.py

def dolor():
    """Dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."""
    pass
```

```python
# Create and update src/project/__init__.py

"""This is project module"""
```

```bash
# Build the documentation
mkdocs build
```

```bash
# Serve the documentation
mkdocs serve
```


```bash
# Validate directory structure
.
├── docs
│   ├── gen_ref_pages.py
│   └── reference
│       └── project
│           ├── amet.md
│           └── dolor.md
├── mkdocs.yml
├── README.md
└── src
    └── project
        ├── amet.py
        ├── dolor.py
        └── __init__.py

5 directories, 8 files
```

```bash
# Freeze the environment
pip list --format=freeze > requirements.txt
```


```bash
# Create the environment.yml file
conda env export > environment.yml
```

```bash
# Deactivate the environment
conda deactivate
```


```bash
# Create a new git repository
git init
git add .
git commit -m "initial commit"
git branch -M develop
git remote add origin https://github.com/pandalearnstocode/mkdocs_demo.git
git push -u origin develop
```

## __References__

* [MKDocs for developers wiki](https://www.mkdocs.org/)
* [MKDocs material theme](https://squidfunk.github.io/mkdocs-material/)
* [MKdocstring for docstring parsing](https://mkdocstrings.github.io/)
* [MKdocstring recipes to automatically parse docstrings](https://mkdocstrings.github.io/recipes/)
* [autoDocstring - Python Docstring Generator](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring)
* [Demo repository](https://github.com/pandalearnstocode/mkdocs_demo)
