import dialogflow_v2 as dialogflow


def prepare_answer(confidence, intent, answer, is_fallback) -> str:
    if is_fallback:
        text = answer
    else:
        text = 'Jestem na {}% pewien, że pytałeś o ' \
               '{}. {}'.format(confidence, intent, answer)

    return text


def detect_intent_texts(project_id, session_id, text, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    text_input = dialogflow.types.TextInput(
        text=text, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)

    confidence = response.query_result.intent_detection_confidence
    intent_name = response.query_result.intent.display_name
    answer = response.query_result.fulfillment_text

    is_fallback = False
    try:
        is_fallback = response.query_result.intent.is_fallback
    except KeyError:
        pass

    return round(confidence*100), intent_name, answer, is_fallback
