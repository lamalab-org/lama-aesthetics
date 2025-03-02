# Lama-Aesthetics

[![Build status](https://img.shields.io/github/actions/workflow/status/lamalab-org/lama-aesthetics/main.yml?branch=main)](https://github.com/lamalab-org/lama-aesthetics/actions/workflows/main.yml?query=branch%3Amain)
[![Supported Python versions](https://img.shields.io/badge/python-3.9_%7C_3.10_%7C_3.11_%7C_3.12_%7C_3.13-blue?labelColor=grey&color=blue)](https://github.com/lamalab-org/lama-aesthetics/blob/main/pyproject.toml)
[![Docs](https://img.shields.io/badge/docs-gh--pages-blue)](https://lamalab-org.github.io/lama-aesthetics/)
[![License](https://img.shields.io/github/license/lamalab-org/lama-aesthetics)](https://img.shields.io/github/license/lamalab-org/lama-aesthetics)

Plotting styles and helpers by LamaLab

- **Github repository**: <https://github.com/lamalab-org/lama-aesthetics/>
- **Documentation** <https://lamalab-org.github.io/lama-aesthetics/>

## Getting started with your project

### 1. Create a New Repository

First, create a repository on GitHub with the same name as this project, and then run the following commands:

```bash
git init -b main
git add .
git commit -m "init commit"
git remote add origin git@github.com:lamalab-org/lama-aesthetics.git
git push -u origin main
```

### 2. Set Up Your Development Environment

Then, install the environment and the pre-commit hooks with

```bash
make install
```

This will also generate your `uv.lock` file

### 3. Run the pre-commit hooks

Initially, the CI/CD pipeline might be failing due to formatting issues. To resolve those run:

```bash
uv run pre-commit run -a
```

### 4. Commit the changes

Lastly, commit the changes made by the two steps above to your repository.

```bash
git add .
git commit -m 'Fix formatting issues'
git push origin main
```

You are now ready to start development on your project!

## Usage



Repository initiated with [lamalab-org/cookiecutter-uv](https://github.com/lamalab-org/cookiecutter-uv).
