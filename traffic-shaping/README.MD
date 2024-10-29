## Airflow DAGs Automation Test

This guide explains how to execute the Airflow DAGs automation tests.

### Prerequisites

- Ensure you have `pytest` installed. If not, you can install it using `pip`:
  ```sh
  pip install pytest
  ```
- Get an AWS token to interact with aws services, use the following command. This token gets expired in 1 hour.
  ```sh
  okta-awscli --okta-profile non-prod
  ```

- Execute following command to make run_tests.sh executable:
  ```sh
  chmod +x scripts/run_tests.sh
  ```

### Running Tests

To run the test case for regression, use the following command:

```sh
# Runs the test cases with default values for regression against dev environment
./scripts/run_tests.sh
```

```sh
# Runs the test cases for regression against dev environment
./scripts/run_tests.sh -m regression -env dev
```

