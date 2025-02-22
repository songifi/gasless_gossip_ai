# Text Prediction Service ✍️

# Description

Text Prediction also known as "Next Sentence Prediction" is a text auto-completion system designed to anticipate the following sequence of words as users type.
The most common model adapted for the use case is the `google-bert/bert-base-uncased` model hosted on hugging face. (https://huggingface.co/google-bert/bert-base-uncased).
BERT is a transformers model pre-trained on a large corpus of English data. Fine-tuned versions specifically on NSP tasks may be adapted or the raw Bert model could be utilized depending on the suited performance degree. 

# Setup
 
 This project recommends the usage of **uv** because it is lightweight and a much faster package manager using a more advanced dependency resolution compared to **pip** and **poetry**. It is cross platform and combines the functionality of `pip`, `pip-tools` and `virtualenv` into one tool simplifying the python packaging workflow.
 
 Note: **Python** version >= 3.10

 To install on Linux/Mac

 ```bash
 curl -LsSf https://astral.sh/uv/install.sh | sh
 ```

 To install on Windows.

 ```bash
 powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
 ```

To install a specific Python version.

```bash
uv python install 3.10
```

To initialize package directory.

```bash
uv init text-prediction-service
```

To make typical directories **data**, **models**, **notebooks**.

```bash
mkdir data models notebooks
```

# Project Structure
```bash
text-generation-service/
|── data/
|── models/
|── notebooks/
│── src/
│   ├── __init__.py
│   ├── main.py
│── .venv/  # Virtual environment (hidden)
│── pyproject.toml
```

The `pyproject.toml` contains metadata about the project.

The `notebooks/`can be used to keep jupyter `.ipynb` experiments to validate usage in `.py` scripts.

You can add dependencies to your `pyproject.toml` with the `uv add` command. This will also update the lockfile and project environment. 

```bash
uv add ruff

#You can also specify a version constraint.

uv add 'ruff== 0.9.7'
```

Note: Ensure that you `cd sticker-generation-service` as you run the above commands.


# Library Requirements

**Core**

`torch` & `transformers`.