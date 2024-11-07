# Project code documentation

# Create and activate a Python virtual environment

It is recommended to use a virtual environment to manage dependencies. You can create and activate a virtual environment as follows:

Create a virtual environment named 'venv':
```shell
python -m venv ./venv
```

Activate the virtual environment:

```shell
source venv/bin/activate
```

# Install the requirements

Install the necessary packages listed in the [`requirements.txt`](/docs/requirements.txt) file:

```shell
pip install -r requirements.txt
```

# Set the `PYTHONPATH`

Ensure the `PYTHONPATH` is set to include your source directory. This is important for Sphinx to locate your modules.

Run the following command at the [root of the project](/).
```shell
export PYTHONPATH=../
```


# Set the test environment variables

Set the test environment variables needed in certain modules.

```shell
export $(xargs < .env)
```

# Generate and read the documentation

Use the `make` command to generate HTML documentation with Sphinx. You can read the documentation by accessing to the `docs/build/html/index.html` file:

```shell
make html
open ./build/html/index.html
```
