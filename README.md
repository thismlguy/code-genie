# code-genie
This library is your copilot for jupyter notebooks

Latest version: 0.4.0-dev0

## Documentation

- [Starter Notebook](https://code-genie.readthedocs.io/en/main/notebooks/Starter.html)
- [All Examples](https://code-genie.readthedocs.io/en/main/examples.html)
- [API Documentation](https://code-genie.readthedocs.io/en/main/api.html)

## Installation

```bash
pip install code_genie
```

## Access Token
You need your unique access token to use this library. You can get your access token
by signing up here [here](https://dodie819.preview.softr.app/?t=1682342288534)

## Usage

### Setting environment variables
On the top of your notebook, set an environment variable called `CODE_GENIE_TOKEN` as your access token. This can
be done in a couple of ways:

#### Using env magic
```
%env CODE_GENIE_TOKEN=xxxkeyxxx
```

#### Using dotenv
You can use the [python-dotenv](https://github.com/theskumar/python-dotenv) package.
```
from dotenv import load_dotenv
load_dotenv("path-to-.env-file")
```
