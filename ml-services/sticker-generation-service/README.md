# Sticker Generation Service 🎨 📌

<p align="center">
  <img src= "iron_man_with_hat.png" width="300" height="300 ali >

  <h5 align="center">"Iron man wearing a cowboy hat" </h5>
</p>


# Features
 - Text Prompt Input: Users can input textual prompts to generate images.
 - Stable Diffusion Model: This project would utilize the Stable Diffusion XL model for high-quality image generation. 
   [Stability AI] (https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0)
 - Sticker Creation: Converts generates images into stickers with customizable overlays.

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
uv init sticker-generation-service
```

To make typical directories **data**, **models**, **notebooks**.

```bash
mkdir data models notebooks
```

# Project Structure
```bash
sticker-generation-service/
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

 `torch`,  `transformers`, `diffusers`





