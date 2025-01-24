# Project code documentation

# Create and activate a Python virtual environment

# It is recommended to use a virtual environment to manage dependencies and
# avoid conflicts with system-installed packages. Follow these steps:

# Step 1: Create a virtual environment named 'venv'.
```shell
python3 -m venv ./venv
```

# Step 2: Activate the virtual environment:
# - On Linux/macOS:
```shell
source venv/bin/activate
```
# - On Windows (PowerShell):
```shell
.\venv\Scripts\Activate.ps1
```

---

# Install the requirements

# Install all the dependencies listed in the [`requirements.txt`](./requirements.txt) file.
# This ensures all necessary libraries and tools for the project are available.
```shell
pip install -r requirements.txt
```

---

# Set the `PYTHONPATH`

# The `PYTHONPATH` environment variable tells Python where to look for your modules.
# Setting this is important for Sphinx to locate your source code during documentation generation.

# Run the following command at the [root of the project](/):
```shell
export PYTHONPATH=../
```

---

# Set the test environment variables

# Some modules in the project require specific environment variables for testing.
# Use the `.env` file to set these variables automatically by running the following command:
```shell
export $(xargs < .env)
```
# Ensure your `.env` file is correctly formatted with `KEY=VALUE` pairs.

---

# Generate and read the documentation

# Use the `make` command to generate HTML documentation using Sphinx.
# Once generated, you can open the documentation in your web browser.

# Step 1: Generate HTML documentation.
```shell
make html
```

# Step 2: Open the generated documentation.
```shell
open ./build/html/index.html
```
# On Windows, use the following command instead:
```shell
start ./build/html/index.html
```
