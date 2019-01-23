# chatbot-browser
Basic functionality of modern web browsers managed by google dialogflow chatbot  
as an interface for older adults.

# Description

## How to run locally

1. Build a Docker image:
`make build`

2. Start an application:
`make start_app`

You can also work in the development environment: 
`make dev`


# Notes
## Sample POST request from DialogFlow (raw)
```
{'originalDetectIntentRequest': {'payload': {}},
 'queryResult': {'allRequiredParamsPresent': True,
  'fulfillmentMessages': [{'text': {'text': ['Rozumiem, otwieram skrzynkę mailową']}}],
  'fulfillmentText': 'Rozumiem, otwieram skrzynkę mailową',
  'intent': {'displayName': 'start-action',
   'name': 'projects/test-agent-fb700/agent/intents/f4d7ee12-9b61-432e-8213-fe57ad957304'},
  'intentDetectionConfidence': 0.55,
  'languageCode': 'pl',
  'parameters': {'functions': 'mail'},
  'queryText': 'wiadomość'},
 'responseId': '2e6d5598-9924-4bf9-b7f7-58b96f0346dc',
 'session': 'projects/test-agent-fb700/agent/sessions/e9bd71e4-efa7-6296-9796-0ef70d7f4785'}
```