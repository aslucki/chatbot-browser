import dialogflow_v2 as dialogflow


class DialogFlowAPIManager:

    def __init__(self, project_id, language_code):
        self.__project_id = project_id
        self.__language_code = language_code

    def get_answer(self, query):

        intent = None

        if query == "":
            answer = "Możesz napisać swoimi słowami, tochę rozumiem."
        else:
            confidence, intent, answer, _ =\
                self.__detect_intent_texts('3231313', query)
            print(intent)

        return intent, answer

    def __detect_intent_texts(self, session_id, text):
        """Returns the result of detect intent with texts as inputs.

        Using the same `session_id` between requests allows continuation
        of the conversation."""

        session_client = dialogflow.SessionsClient()

        session = session_client.session_path(self.__project_id, session_id)

        text_input = dialogflow.types.TextInput(
            text=text, language_code=self.__language_code)

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
