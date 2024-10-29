# Script Tools

## cleanup.py

The script cleanup.py will soft delete all active placements in the company of the user passed as a parameter

| Parameter        | Value (examples)                      | Description                          | Required |
|------------------|---------------------------------------|--------------------------------------|----------|
| --env            | "LOCAL", "DEV", "QA1", "QA2", "INT1"  | The env that is going to be used     | yes      |
| --dashboard_api  | https://managedev.siprocalads.com     | Root URI of the environment          | yes      |
| --dashboard_user | siprocal-data-automation@siprocal.com | User of the Dashboard API            | yes      |
| --dashboard_psw  |                                       | Password of the Dashboard API        | yes      |
| --placement_guid | P0FV027NM931V7VG13RR45GV74            | The optional placement to be deleted | NO       |

The following is the example code for the cleanup script to be executed in the folder automation/data
`

```
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

python scripts/data/cleanup.py --env=DEV --dashboard_api=https://managedev.siprocalads.com
--dashboard_user=siprocal-data-automation@siprocal.com --dashboard_psw=password
`
```


## generate_data_json.sh

generate_data_json.sh will copy test case json & placeholder files and upload to the env

| Parameter by number | Value (examples)                      | Description                      | Required |
|---------------------|---------------------------------------|----------------------------------|----------|
| 1                   | "LOCAL", "DEV", "QA1", "QA2", "INT1"  | The env that is going to be used | yes      |
| 2                   | siprocal-data-automation@siprocal.com | User of the Dashboard API        | yes      |
| 3                   | password                              | Password for the Dashboard API   | yes      |
| 4                   | https://managedev.siprocalads.com     | Root URI of the environment      | yes      |

Note this should be executed in the folder automation/data
