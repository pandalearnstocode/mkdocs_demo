# __Write documentation for your code with `mkdocs`__

## __Docstring parsing using `mkdicstring`__

01. Create a new conda environment and install the packages
02. Activate the environment
03. Install the Python packages `mkdocs`, `mkdocstrings`, `mkdocs-material`, `mkdocs-gen-files`, `mkdocs-literate-nav` and `mkdocs-section-index`
04. Create a new mkdocs project
05. Edit the `mkdocs.yml` file
06. Create the `docs/gen_ref_pages.py` file
07. Create the `src/project` folder
08. Create the `src/project/amet.py` file
09. Create the `src/project/dolor.py` file
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


##### __Create a new conda environment and install the packages__

```bash
conda create -n dev_docs python=3.8 -y
conda activate dev_docs
pip install mkdocs "mkdocstrings[python]" mkdocs-material mkdocs-gen-files mkdocs-literate-nav mkdocs-section-index
```

##### __Create a new mkdocs project__

```bash
mkdocs new .
mkdocs serve
```

##### __Update MKDocs theme__

```yml
site_name: Calculation Docs
theme:
  name: "material"
```

```bash
mkdocs serve
```

##### __Update `mkdocs.yml` for automatic docstring parsing__


```yml
site_name: Calculation Docs
theme:
  name: "material"
nav:
- Code Reference: reference/ 
plugins:
- search
- gen-files:
    scripts:
    - docs/gen_ref_pages.py
- literate-nav:
    nav_file: SUMMARY.md
- section-index
- mkdocstrings
```

##### __Create and update `docs/gen_ref_pages.py`__

```python
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

##### __Create and update `src/project/amet.py`__

```python

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

##### __Create and update `src/project/dolor.py`__

```python
def dolor():
    """Dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."""
    pass
```

##### __Create and update `src/project/__init__.py`__

```python
"""This is project module"""
```

##### __Build and serve wiki__

```bash
mkdocs build
```

```bash
mkdocs serve
```

##### __Directory structure of the wiki__

```bash
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

##### __Save dependencies as `requirements.txt` & `environment.yml`__

```bash
pip list --format=freeze > requirements.txt
conda env export > environment.yml
conda deactivate
```


##### __Push code to GitHub__

```bash
git init
git add .
git commit -m "initial commit"
git branch -M develop
git remote add origin https://github.com/pandalearnstocode/mkdocs_demo.git
git push -u origin develop
```

## __Manage document version `mike`__

01. Install Poetry and add poetry path in `~/.bashrc` and validate with `poetry --version`
02. Create poetry project
03. Add and install dependencies
04. Extract version from `pyproject.toml` and make inital release
05. Push files to gh-pages branch
06. bump version
07. Push files to gh-pages branch
08. Add github action to build and deploy documentation
09. Bump version
10. Push files to develop branch
11. Validate version changes in github pages

### __Install Poetry__

```bash
# Install poetry
curl -sSL https://install.python-poetry.org | python3 -
nano ~/.bashrc
export PATH="/home/pandalearnstocode/.local/bin:$PATH"
source ~/.bashrc
poetry --version
```

### __Create a new poetry project__

```bash
poetry init
poetry add toml-cli mike
```

##### __Update `mkdocs.yml`__

```yml
site_name: My Docs
theme:
  name: material
extra:
  version:
    provider: mike
```

##### __Extract library version and publish inital release in GitHub pages__

```bash
version=$(toml get --toml-path pyproject.toml tool.poetry.version)
echo "${version}"
mike deploy --push --update-aliases ${version} latest
mike set-default --push latest
```

##### __Update library version and publish subsequent release__

```bash
poetry version patch
version=$(toml get --toml-path pyproject.toml tool.poetry.version)
echo "${version}"
mike deploy --push --update-aliases ${version} latest
```

## __Build and publish developers wiki with `mike`, `poetry` and `GitHub actions`__

##### __Create required github actions file__

Create a new github file here `.github/workflows/build-wiki.yml`.

##### __Update `build-wiki.yml`__

```yml
name: ci 
on:
  push:
    branches:
      - develop
permissions:
  contents: write
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
            fetch-depth: 0
      - name: Install Poetry
        run: |
          pipx install poetry
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
          cache: poetry
      - name: Set Poetry environment
        run: |
          poetry env use 3.9
      - name: Install dependencies
        run: |
          poetry install --no-root
      - name: Deployment setup
        run: |
          git config user.name github-actions
          git config user.email github-actions@github.com 
      - name: Deploy document
        run: |
          RELEASE_VERSION=$(poetry run toml get --toml-path pyproject.toml tool.poetry.version)
          poetry run mike deploy --push --update-aliases ${RELEASE_VERSION} latest
```


```bash
cd docs
mkdir stylesheets
mkdir javascripts
cd stylesheets
touch extra.css
cd ../javascripts
touch extra.js
```

```yml
extra_css:
  - stylesheets/extra.css
extra_javascript:
  - javascripts/extra.js
```



```css
@media only screen and (min-width: 76.25em) {
    .md-main__inner {
      max-width: none;
    }
    .md-sidebar--primary {
      left: 0;
    }
    .md-sidebar--secondary {
      right: 0;
      margin-left: 0;
      -webkit-transform: none;
      transform: none;   
    }
  }
```

```bash
poetry add mkdocs-enumerate-headings-plugin mkdocs-git-authors-plugin mkdocs-git-revision-date-localized-plugin
```

```yml
plugins:
- search
- gen-files:
    scripts:
    - docs/gen_ref_pages.py
- literate-nav:
    nav_file: SUMMARY.md
- section-index
- mkdocstrings
- enumerate-headings
- git-authors
```


Create `docs/images/logo.png` and update `mkdocs.yml` with

```yml
theme:
  name: "material"
  logo: 'images/logo.png'
```
## __References__

* [MKDocs for developers wiki](https://www.mkdocs.org/)
* [MKDocs material theme](https://squidfunk.github.io/mkdocs-material/)
* [MKdocstring for docstring parsing](https://mkdocstrings.github.io/)
* [MKdocstring recipes to automatically parse docstrings](https://mkdocstrings.github.io/recipes/)
* [autoDocstring - Python Docstring Generator](https://marketplace.visualstudio.com/items?itemName=njpwerner.autodocstring)
* [Demo repository](https://github.com/pandalearnstocode/mkdocs_demo)
* [How To Install Poetry to Manage Python Dependencies on Ubuntu 22.04](https://www.digitalocean.com/community/tutorials/how-to-install-poetry-to-manage-python-dependencies-on-ubuntu-22-04)
* [Setting up versioning](https://squidfunk.github.io/mkdocs-material/setup/setting-up-versioning/#versioning)
* [Demo: How to set up versioning](https://github.com/squidfunk/mkdocs-material-example-versioning)
* [How do I set a variable to the output of a command in Bash?](https://stackoverflow.com/questions/4651437/how-do-i-set-a-variable-to-the-output-of-a-command-in-bash)
* [Command line interface to read and write keys/values to/from toml files](https://pypi.org/project/toml-cli/)
* [Manage multiple versions of your MkDocs-powered documentation](https://pypi.org/project/mike/)
* [Releasing and versioning](https://py-pkgs.org/07-releasing-versioning.html)
* [Sample mike deploy pipeline](https://github.com/SatelCreative/spylib/blob/main/.github/workflows/docs.yml)
* [Poetry cache GitHub actions](https://gist.github.com/gh640/233a6daf68e9e937115371c0ecd39c61)
* [Adding assets to MKDocs material theme](https://squidfunk.github.io/mkdocs-material/customization/)