#!/bin/bash

MSG="$1"

JIRA_KEYS=("CP-" "TCAM-")

for key in ${JIRA_KEYS[@]}; do
    if [[ $msg == *"$key"* ]]; then
        exit 0
    fi
done
msg=${msg^^}

if [[ ${msg^^} == *"#NOJIRA"* ]]; then
    echo "#NOJIRA commit with the message -> " $MSG
    exit 0
fi

#At this point we know there is not key in the message, and we are going to fail the commit message
echo "Your commit message must contain the key of the jira project, for example CP-#### or TCAM-####. if is a NOJIRA then add #NOJIRA in the message"
exit 1

