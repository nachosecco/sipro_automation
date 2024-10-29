[Repository Docs - Dashboard](https://beezag.jira.com/l/cp/UNPPH4uo)

# How to install:

Install latest node and npm stable versions
(https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)

Install npm modules

```
$ npm install
```

## How to open and run Cypress test cases:

### Environment Variables

Cypress interacts with the UI the way a real user would. For this reason, we need to tell Cypress which users to login as when running tests.

Each environment should have two users setup to run automation tests:

1. uiUser - The main test user. This user is isolated to a special company we use to run the majority of dashboard regression tests
2. globalUser - We have some features that are only available to "global" users, which must be members of the "primary" company. We should only use this user for testing when necessary.

We use environment variables to make Cypress aware of the credentials for these users. There are many ways to set env variables, such as:

```
$ export cypress_uiUser={USER}
$ export cypress_uiPassword={PASSWORD}
$ export cypress_globalUser={USER}
$ export cypress_globalPassword={PASSWORD}
```

NOTE: The login information for the automation user for remote environments can be found in AWS Secret Manager. This can be useful when trying to reproduce and debug test failures.

### Interactive mode

In order to open the Cypress UI to run tests in interactive mode, use the following command:

```
$ npx cypress open
```

1. Select e2e Testing from the Cypress UI
2. From there we can use the Cypress UI to filter and run spec files when developing and debugging

#### Remote Environments:

In order to connect to remote environments, we can specify the environment:

```
$ npx cypress open --env name=qa1
```

### Single Run

In order to perform a single run of Cypress tests, use the following command:

```
$ npx cypress run
```

#### Remote Environments

In order to connect to remote environments, we can specify the environment (just like interactive mode)

```
$ npx cypress run --env name=qa1
```

There are many flags we can pass to Cypress, e.g. to filter specs based on glob patterns:

```
$ npx cypress run --spec {PATH_TO_SPEC_FILE}
```

-   Flags are documented here: https://docs.cypress.io/guides/guides/command-line#cypress-run

### Parallel Run

It can be much faster to run the tests in multiple threads using cypress-parallel. Parallel runs are turned on by default for our remote builds via jenkinsfile. In order to run locally, use:

```
$ npm run cy:run:parallel
```

In order to change the environment, or number of threads, we can use npm to pass flags that override the default flags (note the extra `--`):

```
<!-- Will run in qa1 with only 2 threads  -->
$ npm run cy:run:parallel -- -a '\"--env name=qa1\"' -t 2
```

#### Parallel Run Report Generation

When running tests in parallel, we are forced to manually clean up and generate report files.

-   First delete any previously generated cypress reports:
    -   `npm run clean`
-   Next run cypress in parallel mode:
    -   `npm run cy:run:parallel`
-   Generate a summary html report based on the individual spec file json reports
    -   `npm run generate-report`

Our default `npm test` command combines the above three commands into a single command to properly generate reports for a local test run.

## Cypress Grep and Flake Detection

We can use [cypress-grep](https://www.npmjs.com/package/@cypress/grep) to run specific tests in isolation:

```
$ npm run cy:grep -- --env name={ENVIRONMENT},grep={GREP_PATTERN}
```

For instance, to run only the "Valid login"

```
$ npm run cy:grep -- --env name=local,grep="Valid login"
```

Optionally, to make things even faster we can filter just within a given spec file e.g. `login.spec.js`

```
$ npm run cy:grep -- --env name=local,grep="Valid login" --spec cypress/tests/ui/login/login.spec.js
```

### Flake Detection

cypress-grep has a "burn" feature that allows us to run the same test N number of times. This is very useful for determining if a test is flaky (i.e. sometimes passes/sometimes fails when run multiple times)

```
$ npm run cy:grep -- --env name={ENVIRONMENT},grep={GREP_PATTERN},burn={N}
```

For example, to run the "Valid login" test 10 times:

```
$ npm run cy:grep -- --env name=local,grep="Valid login",burn=10
```

We have a jenkins job for each remote environment that allows us to use cypress-grep and the burn parameter to detect flakes.

## Local Configuration

The config folder contains environment-specific configuration.

-   baseUrl: Base URL for UI
-   dashboardApi: Base URL for the API backend that the UI connects to
-   auth: URL for the actual API endpoint that provides authorization tokens
-   inventoryRouter: Base URL for the inventory router API that the UI connects to
-   credentials for uiUser and globalUser are documented above

FIRST TIME SETUP: To run test against a local environment, use one of the existing config files as a template to create a `local.json` file in the config folder and replace the `{{variable}}` with the relevant information. `local.json` files are in our `.gitignore` so that we can make changes without worrying about affecting others.

```json
{
	"baseUrl": "{{baseUrl}}",
	"env": {
		"dashboardApi": "{{dashboardApi}}",
		"auth": "{{authEndpoint}}",
		"inventoryRouter": "{{inventoryRouterEndpoint}}"
		// Credentials are optional. These can be set through standard environment variables as documented above
		// "uiUser": "{{testUserName}}",
		// "uiPassword": "{{testUserPassword}}",
		// "globalUser": "{{testGlobalUser}}",
		// "globalPassword": "{{testUserPassword}}",
	}
}
```

> For further details go to: https://docs.cypress.io/api/api/table-of-contents.html
