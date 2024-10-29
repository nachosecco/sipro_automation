# Data Pipeline Regression Framework

## Overview
The Data Pipeline Regression Framework is designed to assist developers and testers in creating regression test cases for data pipelines. This framework provides tools and utilities to set up, execute, and validate data pipeline processes, ensuring data integrity and correctness across different stages of the pipeline.

## Features
- **Easy Test Case Creation**: Simplifies the creation of regression test cases for data pipelines.
- **Integration with Druid and Athena**: Provides built-in support for querying and validating data in Druid and Athena.
- **Mock Data Setup**: Allows for the setup of mock data to simulate various scenarios.
- **Logging and Reporting**: Includes logging capabilities to track test execution and results.

## Getting Started
### Prerequisites
- Python
- pip (Python package installer)
- Please take a look at `requirements.txt` for the required Python packages.

### Environment variables
```shell
DPR_PATH_CASE_EVENTS=cases/basic
DPR_EXECUTION_ID=1
DPR_PATH_CSV=build/data/case_placements.csv
DSE_API_PWD=xxxxx
DSE_API_USER=xxxx@column6.com
DSE_DASHBOARD_API=https://managedev.siprocalads.com
DSE_ENVIRONMENT=dev
```

### Setup
To set up a test case, follow the structure of the provided example `test_example_opportunity_and_impression.py`.  

In that example:
* A `Case` object is created with the name `example_of_opportunity_and_impression`.
* Delivery parameters are set up, including the `content_series`.
* An `event_coordinator` is created to manage the delivery events.
* The `call_delivery` method is used to simulate delivery events.
* Each event calls the `call_impression` method to simulate impressions.
* Logging is used to track the total number of events and the date-time range.

You can create your own test cases by copying and pasting the provided example test and modifying it to suit your specific requirements.

### Asserting

#### Asserting in Druid
To assert in Druid, you can use the `DruidAsserter` class. Below is an example of how to perform assertions in Druid:
```python
druid_asserter_network = case.assert_in_druid().network()
druid_asserter_network.query_of_sum_metrics_and_dimensions_with_single_row_equals_to(
        [NetworkMetricsDruid.OPPORTUNITY, CommonMetricsDruid.IMPRESSION],
        [],  # no dimension
        [expected_opportunities, expected_impressions],
    )
```
#### Asserting in Athena
To assert in Athena, you can use the `AthenaAsserter` class. Below is an example of how to perform assertions in Athena:
```python
athena_asserter = case.assert_in_athena()
athena_asserter.opportunity().query_of_count_equals_to(expected_opportunities)
athena_asserter.impression().query_of_count_equals_to(expected_impressions)
```

### Jenkins 🔥
The ultimate goal is to run the regression tests in Jenkins. The following Jenkins jobs have been created to run the regression tests:

* dev: https://jenkins-cloud.rowdy.cc/job/dev/job/datapipeline-regression/
* qa1: https://jenkins-cloud.rowdy.cc/job/qa1/job/datapipeline-regression/
* qa2: https://jenkins-cloud.rowdy.cc/job/qa2/job/datapipeline-regression/

Press **Build with Parameters** to run the regression tests. In the field **BRANCH**
you can specify the branch you want to run the tests on. The default is `master`. Then hit the Build button ▶️.
