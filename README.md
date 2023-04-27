# code-genie
This library is your copilot for jupyter notebooks

Latest version: 0.1.2

## Documentation

- [Started Notebook](https://code-genie.readthedocs.io/en/latest/notebooks/Starter.html)
- [All Exampples](https://code-genie.readthedocs.io/en/latest/examples.html)
- [API Documentation](https://code-genie.readthedocs.io/en/latest/api.html)

## Installation

```bash
pip install code-genie
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

#### Pandas data processing

Following is an example to get the number of missing values in each column of a dataframe.

```python
from code_genie import PandasGenie
genie = PandasGenie(instructions=[
    "create a new dataframe which contains the number of missing values in each column",
    "add a column to this dataframe representing the percentage of total points which are missing",
    "sort dataframe in descending order of number of missing items",
    "filter out columns which have no missing values"
    ])
df_missing = genie(df)
```
