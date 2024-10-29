# Router Regression Automation

## Installation

### Requirements

- Python 3.8.10
- [Pyenv](https://github.com/pyenv/pyenv)
- [Chrome WebDriver](https://chromedriver.chromium.org/downloads) (Use the same version that matches your OS and Chrome
  version)
- Google Chrome


- Install **pre-commit**

```shell
pip install pre-commit
pre-commit install
```

The bash **install.sh** should install those requirements.

<br>Note:<br>
If **install.sh** fails please try to install the required components manually. Look at the install.sh file content for
details.
<br><br>

### For Mac Users

install.sh doesn't work for Mac. Follow these steps to complete the installation:

- Use this link to install [Pyenv](https://github.com/pyenv/pyenv#homebrew-in-macos)
    - You can use Homebrew to install Pyenv. Then depending on which shell environment you use (Bash or Zsh), remember
      to [set up your shell environment](https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv)
- Install Python 3.8.10 using

```shell
pyenv install 3.8.10
```

- To install Chrome WebDriver
    - [Download](https://chromedriver.chromium.org/downloads) and install the Mac WebDriver version that matches the
      Chrome version installed on your computer.
    - Unzip chromedriver and move it to /usr/local/bin directory. And run the following command so that MacOS can verify
      the app.

```shell
mv ~/Downloads/chromedriver /usr/local/bin
cd /usr/local/bin
xattr -d com.apple.quarantine chromedriver
```

- Setup virtualenv

```shell
brew install pyenv-virtualenv
pyenv local 3.8.10
pyenv virtualenv 3.8.10 routers
pyenv activate routers```

- Install the required Python modules
    - Before executing the following command ensure you are in automation/router folder

```shell
pip3 install -r requirements.txt
```

## Pre-Reqs for Execution:

Environment variables required to start to test cases

| Variable                       |                                  Description                                  |                                                              Optional |
|:-------------------------------|:-----------------------------------------------------------------------------:|----------------------------------------------------------------------:|
| RS_URL                         |          This is the root of router, example: http://localhost:8111           |                                                                    No |
| READ_LOG_STRATEGY              |         The possible options to read the logs are (OPEN_SEARCH,LOCAL)         |                                                                    No |
| READ_LOG_OPEN_SEARCH_HOST      |        The host of the kibana open search, example kibana-dev.rowdy.cc        |               Yes[ only required if READ_LOG_STRATEGY is OPEN_SEARCH] |
| RS_DATA_FILE                   | The path to of the CSV file that has the map by case for uid of the placement |                                                                    No |
| RS_DASHBOARD_API               |                 This is the root path to dashboard api server                 |          Yes<br/>[Only required in cases using data from environment] |
| RS_API_USER                    |                   This is the user to dashboard api server                    |          Yes<br/>[Only required in cases using data from environment] |
| RS_API_PWD                     |               This is the password to the dashboard api server                |          Yes<br/>[Only required in cases using data from environment] |
| RS_ENVIRONMENT                 |                    This is the environment we are running                     | Yes<br/>[Only required in csv generation(csvGeneratorForDataFile.py)] |
| RS_NUMBER_OF_PROCESS_OF_PYTEST |       This is the number of process to run in tests to run in parallel        |                                      Yes[By default has 3 as a value] |

## Execution in aws

```sh
    export READ_LOG_STRATEGY="OPEN_SEARCH"

    export RS_ENVIRONMENT="dev1"

    export RS_URL="https://routerdev.altitude-arena.com"

    export READ_LOG_OPEN_SEARCH_HOST="vpc-c6-dev-es-uw2-logs-dlfqhljpdvbm62vc4qfbsnckji.us-west-2.es.amazonaws.com"

    ./run_test.sh

```

### Use of the “MARKERS“ in the automation framework.

```sh
Step 1: Using any python IDE open the file which you want to run, just above the method you will be required to add @pytest.mark.<any name>, now to make this work
you will have to import the pytest package.

for example:
@pytest.mark.regression
@pytest.mark.myTest
def test_missing_latitude():
   case = Case("test_missing_latitude")


```

### Alternative could be use properties by default

```sh
./run_tests_aws_{env}.sh
```

## Execution in local environment

```sh
./run_tests_local_env.sh
```

## Code formatting in IDE

https://black.readthedocs.io/en/stable/integrations/editors.html


## Ide Configuration

Router uses Delivery as a python library (module)
that means we have to configure the IDE to add the delivery as a module

for example for IDEA (or pyCharm)
option 1 = In the project structure you can add the delivery folder in the classpath
option 2 = configure as a second module as root source
