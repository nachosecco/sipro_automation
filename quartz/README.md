[Repository Docs - Quartz](https://beezag.jira.com/l/cp/1Nh0Fdiq)

## Important
- Multiple tests for the same Quartz job shouldn't be run in parallel. Tests of different Quartz jobs could run in parallel.


# Setup instructions
```
pyenv local 3.8.10
pyenv virtualenv 3.8.10 c6-autoquartz
pyenv activate c6-autoquartz
pip3 install -r requirements.txt
```

# Connecting to AWS from your Local Environment
```
-- Follow these steps to set up okta-awscli:  https://beezag.jira.com/wiki/spaces/PT/pages/2958426122/Connect+to+awscli+using+okta

# Get AWS temporary credentials
# NOTE: These will expire periodically, so you will need to rerun this command to get fresh credentials
okta-awscli --okta-profile <PROFILE NAME HERE> --profile <PROFILE NAME HERE>

# Export the AWS_PROFILE so all connections to AWS will know to use the temp credentials
export AWS_PROFILE=<PROFILE NAME HERE>

Note: The export is session specific, so be sure you run the export in the same terminal as you are running the tests
```

# Job specific setup
### Before running any job
```
# Source (or manually export) the test config
. local.env
```
## Liveramp Jobs
```
# These tests can either be run using the local file system or an S3 bucket.
# You need to have the tests and the Quartz service configured the same way.
#
# To run using a local file system, set the QRT_LOCAL_LIVERAMP_FOLDER environment variable
# To run using S3, leave QRT_LOCAL_LIVERAMP_FOLDER unset and set QRT_S3_LIVERAMP_BUCKET_NAME
# See above for how to connect to AWS from your local environment
#
# Running locally is much faster, but it is a good idea to test with S3 too before opening a PR.
```

### AudienceSegment1stPartyJob

```
# Run the AudienceSegment1stPartyJob tests
pytest -W ignore::DeprecationWarning:invoke.loader -k 'test_audience_segment_1st_party_job'
```

### AudienceSegment3rdPartyJob
```
# Run the AudienceSegment3rdPartyJob tests
pytest -W ignore::DeprecationWarning:invoke.loader -k 'test_audience_segment_3rd_party_job'
```

### AudienceSegmentTaxonomyJob
```
# Run the AudienceSegmentTaxanomyJob tests
pytest -W ignore::DeprecationWarning:invoke.loader -k 'test_audience_segment_taxonomy_job'
```
## IVT Data Ingestion Jobs
```
# These tests can either be run using the local file system or an SFTP.
# You need to have the tests and the Quartz service configured the same way.
#
# To run using a local file system, set the QRT_LOCAL_LIVERAMP_FOLDER environment variable
# To run using SFTP, leave QRT_IVT_LOCAL_FOLDER= unset and set QRT_SFTP_* properties
```
### IngestIPv4DatafeedJob
```
# Run the IngestIPv4DatafeedJob tests
pytest -W ignore::DeprecationWarning:invoke.loader -k 'test_ivt_ip4_datafeed_job'
```

### IngestIPv6DatafeedJob
```
# Run the IngestIPv6DatafeedJob tests
pytest -W ignore::DeprecationWarning:invoke.loader -k 'test_ivt_ip6_datafeed_job'
```

### IngestOTTDatafeedJob
```
# Run the IngestOTTDatafeedJob tests
pytest -W ignore::DeprecationWarning:invoke.loader -k 'test_ivt_ott_datafeed_job'
```

### IngestUserAgentDatafeedJob
```
# Run the IngestUserAgentDatafeedJob tests
pytest -W ignore::DeprecationWarning:invoke.loader -k 'test_ivt_ua_datafeed_job'
```

# Running Tests
```
Set necessary environment variables
  Source one of the config files e.g. local.env

Run All Tests
./run_tests.sh

Run Tests From a Particular File
./run_tests.sh file:test_audience_segment_3rd_party_job

Run a Single Test
Add @pytest.mark.<some value> annotation to the test
./run_tests.sh mark:<some value>
```
# Notes
```
QRT as a prefix for the environment variables stands for Quartz Regression Testing
```
# Resolution of issues while running test
1. If you encounter error "ImportError while importing test module", then try running jobs
```
python -m pytest -W ignore::DeprecationWarning:invoke.loader -k 'test_ivt_ip6_datafeed_job'
```