# Control Model

Minimum operational controls:

## Global
- pause bridge replies
- resume bridge replies
- check status

## Per contact
- assume/take over a phone number
- release a phone number

## State files
Use simple JSON files for:
- control state
- lead state

## Logging
Log every important decision, especially:
- blocked existing customer/patient
- blocked by global pause
- blocked by manual override
- allowed by activation phrase
- allowed by new contact
- allowed by existing lead
