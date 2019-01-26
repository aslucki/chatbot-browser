# chatbot-browser
Basic functionality of modern web browsers managed by google dialogflow chatbot  
as an interface for older adults.

# Description

## How to run locally

1. Build a Docker image:
`make build`

2. Start the application:
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

## DialogFlow API response for not recognized
```buildoutcfg
query_result {
  query_text: "feature learning"
  action: "input.unknown"
  parameters {
  }
  all_required_params_present: true
  fulfillment_text: "Możesz to powtórzyć?"
  fulfillment_messages {
    text {
      text: "Nie bardzo rozumiem."
    }
  }
  intent {
    name: "projects/test-agent-fb700/agent/intents/745f123c-c680-42fc-81d9-244352324cc7"
    display_name: "Default Fallback Intent"
    is_fallback: true
  }
  intent_detection_confidence: 1.0
  language_code: "pl"
}
```

## DialogFlow API response for recognized
```
query_result {
  query_text: "wiadomość"
  parameters {
    fields {
      key: "functions"
      value {
        string_value: "mail"
      }
    }
  }
  all_required_params_present: true
  fulfillment_text: "Rozumiem, otwieram skrzynkę mailową"
  fulfillment_messages {
    text {
      text: "Rozumiem, otwieram skrzynkę mailową"
    }
  }
  intent {
    name: "projects/test-agent-fb700/agent/intents/f4d7ee12-9b61-432e-8213-fe57ad957304"
    display_name: "start-action"
  }
  intent_detection_confidence: 0.550000011920929
  diagnostic_info {
    fields {
      key: "webhook_latency_ms"
      value {
        number_value: 128.0
      }
    }
  }
  language_code: "pl"
}
webhook_status {
  code: 3
  message: "Webhook call failed. Error: Failed to parse webhook JSON response: Cannot find field: success in message google.cloud.dialogflow.v2beta1.WebhookResponse."
}
```