You can also refer to
this [Confluence Wiki Page](https://beezag.jira.com/wiki/spaces/PT/pages/2984902684/How+To+Set+up+Delivery+Test+Automation)
for setting up the development environment.

# Delivery Automation

[Repository Docs - Delivery](https://beezag.jira.com/l/cp/1qAs2tXj)

## Installation

### Requirements

- Python 3.8.10
- [Pyenv](https://github.com/pyenv/pyenv)
- [Chrome WebDriver](https://googlechromelabs.github.io/chrome-for-testing/) (Use the same version that matches your OS and Chrome
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
pyenv virtualenv 3.8.10 c6-autodelivery
pyenv activate c6-autodelivery```

- Install the required Python modules
    - Before executing the following command ensure you are in automation/delivery folder

```shell
pip3 install -r requirements.txt
```

## Code formatting in IDE

We enforce formatting rules so it's highly recommended to setup your IDE to format your code on save, or at least on command from within your IDE

https://black.readthedocs.io/en/stable/integrations/editors.html

## Pre-Reqs for Execution:

Environment variables required to start to test cases

## IntelliJ Setup

While it's not a requirement to use IntelliJ, at the time of this writing a majority of the team does use it, so we're including some IntelliJ-specific notes here.

* When opening the project, it's recommended to open the delivery module only
* We must make intellij aware of our python dependencies
* Developers should configure their project settings to point to the python virtual environment created with `pyenv` above
	* File -> Project Structure
	* For SDK, follow instructions here to add `c6-autodelivery`:
		* https://www.jetbrains.com/help/idea/creating-virtual-environment.html#existing-virtual-environment

| Variable                       |                                  Description                                  |                                                              Optional |
|:-------------------------------|:-----------------------------------------------------------------------------:|----------------------------------------------------------------------:|
| DELIVERY_ROOT_URL              |         This is the root of delivery, example: http://localhost:8050          |                                                                    No |
| READ_LOG_STRATEGY              |      The possible options to read the logs are (OPEN_SEARCH,LOCAL, SSH)       |                                                                    No |
| DATA_FILE                      | The path to of the CSV file that has the map by case for uid of the placement |                                                                    No |
| DF_MEDIA_SERVER_URL            |                     This is the root path to asset server                     |                       Yes<br/>[Only required in media size targeting] |
| DSE_DASHBOARD_API              |                 This is the root path to dashboard api server                 |          Yes<br/>[Only required in cases using data from environment] |
| DSE_API_USER                   |                   This is the user to dashboard api server                    |          Yes<br/>[Only required in cases using data from environment] |
| DSE_API_PWD                    |               This is the password to the dashboard api server                |          Yes<br/>[Only required in cases using data from environment] |
| DSE_ENVIRONMENT                |                    This is the environment we are running                     | Yes<br/>[Only required in csv generation(csvGeneratorForDataFile.py)] |
| DF_NUMBER_OF_PROCESS_OF_PYTEST |       This is the number of process to run in tests to run in parallel        |                                      Yes[By default has 3 as a value] |

## Creating A New Test Case

We've put together a [guide to create a case](https://beezag.jira.com/wiki/spaces/PT/pages/2921070593/Automation+Framework+Delivery) in confluence.

---

## Execution in aws

```sh
    export READ_LOG_STRATEGY="OPEN_SEARCH"

    export AUTOMATION_ENVIRONMENT="dev1"

    export DELIVERY_ROOT_URL="https://deliverydev.siprocalads.com"

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
   vpc = case.vpc

Step 2: Scroll through the project menu and further down you will find the file 'run_tests.sh'. Select the file and go to line 21

pytest -n 3 --html=build/report.html --self-contained-html

now change that line to this

pytest -n 3 -m myTest --html=build/report.html --self-contained-html

#what this will do is, it will run the marked file(s).

```

### Alternative could be use properties by default

```sh
./run_tests_aws_{env}.sh
```

## Execution in local environment

```sh
./run_tests_local_env.sh
```

---

## Updating Geo Targeting Data File

The geo targeting tests use data/data-file-geoip.csv as their source of data for getting IP addresses, which will match
the expected targeting criteria.

When MaxMind is updated, this file should also be updated to match the new MaxMind data set.

Follow these steps to update the file

- Copy these 4 files from the MaxMind download into the scripts directory. Note the 1st two are CSV and the last 2 are
  MMDB files (they shouldn't be added to git)

```
GeoIP2-City-Blocks-IPv4.csv
GeoIP2-City-Locations-en.csv
GeoIP2-Connection-Type.mmdb
GeoIP2-ISP.mmdb
```

- Run the update script

```
pip install geoip2
python scripts/update_geo_ip_data_file.py

# This will take a few minutes to run (~3min on my machine)
# Watch for any ERROR messages
# The new file will be output to data/NEW-data-file-geoip.csv

diff data/data-file-geoip.csv data/NEW-data-file-geoip.csv
cp data/NEW-data-file-geoip.csv data/data-file-geoip.csv

# Now you should execute all of the tests against an environment that has the new MaxMind data
```

## Updating Liveramp

New/Existing test cases can use liveramp data. So, rather than adding segments individually for every test cases, a new
script(liveramp_data_sync_job.py) being added which will add/update all liveramp to aerospike and DB.
Files for device/Web segments and taxonomy being added in audience_targeting_files folder containing rows for being
added/updated through above-mentioned script.
Whenever a user wants to add segments or taxonomy data which will be further used in his test case, he need to add a new
row in respective file.

#### Setup Liveramp Job (locally)

```sh
    export S3_LIVERAMP_BUCKET_NAME=""
    export READ_LOG_OPEN_SEARCH_HOST="/tmp/liveramp"
    export LIVERAMP_BUCKET_SUB_FOLDER="upload"
```

Update below properties in Quartz.py file

- QUARTZ_HOST: localhost
- QUARTZ_PORT: 8030
  Now, you are ready to use liveramp_data_sync Job to execute liveramp data in local environment.

## Download And Generate Test Data CSV File Locally

To generate the Test Data CSV file for a specific environment for local development and testing, set the following
Environmental Variables, e.g., for dev environment:

```sh
    export DSE_ENVIRONMENT="dev"
    export DSE_DASHBOARD_API="https://managedev.altitude-arena.com"
    export DSE_API_USER="siprocal-delivery-automation@siprocal.com"
    export DSE_API_PWD="XXXXXXXXXX"
```
Run the Python script delivery/csvGeneratorForDataFile.py.

## Generate Bidder Data File Locally

To generate the Bidder Data file for a specific environment for local development and testing, set the following
Environmental Variables, e.g., for dev environment:

```sh
    export DSE_ENVIRONMENT="dev"
    export DSE_DASHBOARD_API="https://managedev.altitude-arena.com"
    export DSE_API_USER="siprocal-delivery-automation@siprocal.com"
    export DSE_API_PWD="XXXXXXXXXX"
```
Run the Python script delivery/generate_bidder_data_file.py.