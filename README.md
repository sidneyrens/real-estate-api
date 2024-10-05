# real-estate-api
App for connecting clients and agents adding automation to real estate transactions

## Python API

In order to run the Python API, you need to have Python 3.8 or higher installed. 

### Windows
Please follow the instructions [here](https://www.python.org/downloads/) to install Python.

### MacOS

#### Requirements
Please follow the instructions [here](https://docs.python.org/3/using/mac.html#getting-and-installing-the-python-3-standard-library) to install Python, or if you use Homebrew, you can install it by running `brew install python`.

Validate the installation by running `python --version`. If you install through Homebrew, the command will be `python3 --version`. (Alternatively, you can alias your python3 installation to `python` in your shell by adding `alias python=/usr/local/bin/python3` to your `.zshrc` or `.bashrc` file.)

#### Installation
Create a virtual environment:
On Windows: `python -m venv venv`
On macOS/Linux: `python3 -m venv venv` || `python -m venv venv`

Activate the virtual environment:
On Windows: `venv\Scripts\activate`
On macOS/Linux: `source venv/bin/activate`
You can tell if the virtual environment is activated by the `(venv)` prefix in your terminal.

Install the dependencies:
1. Run `pip install -r requirements.txt`

#### Running the app
2. Run `python app.py`

*The Python API will run on port 5000.*

