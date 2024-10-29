[Repository Docs - RTB](https://beezag.jira.com/wiki/spaces/PT/pages/3072589837/RTB+Bidder)

## Important


# Setup instructions
```
pyenv local 3.8.10
pyenv virtualenv 3.8.10 c6-autortb
pyenv activate c6-autortb
pip3 install -r requirements.txt
```


# Running Tests
```
Set necessary environment variables
  Source one of the config files e.g. local.env

Run All Tests
./run_tests.sh


Run a Single Test
Add @pytest.mark.<some value> annotation to the test
./run_tests.sh mark:<some value>
```

# Notes
```
RTBRT as a prefix for the environment variables stands for Rtb Testing
```
