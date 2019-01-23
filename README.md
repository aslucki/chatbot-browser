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
b'{\n  "responseId": "b71b3181-9715-42e0-b4e8-b1c118634447",\n
       "queryResult": {\n    "queryText": "wiadomo\xc5\x9b\xc4\x87",\n 
                             "parameters": {\n      "functions": "mail"\n    },\n
       "allRequiredParamsPresent": true,\n
       "fulfillmentText": "Rozumiem, otwieram skrzynk\xc4\x99 mailow\xc4\x85",\n
       "fulfillmentMessages": [{\n      "text": {\n        "text": ["Rozumiem, otwieram skrzynk\xc4\x99 mailow\xc4\x85"]\n      }\n    }],\n
       "intent": {\n      "name": "projects/test-agent-fb700/agent/intents/f4d7ee12-9b61-432e-8213-fe57ad957304",\n
                          "displayName": "start-action"\n    },\n
       "intentDetectionConfidence": 0.55,\n
       "languageCode": "pl"\n  },\n 
       "originalDetectIntentRequest": {\n    "payload": {\n    }\n  },\n
       "session": "projects/test-agent-fb700/agent/sessions/31cc02ba-ac66-2a92-7665-cdcb890a2453"\n}'
```