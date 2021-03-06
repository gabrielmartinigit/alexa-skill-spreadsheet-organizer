# -*- coding: utf-8 -*-

import logging
import os

import ask_sdk_core.utils as ask_utils
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler

from spreadsheet import Spreadsheet
from datetime import datetime
import pytz

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

spreadsheet = Spreadsheet(
    os.environ['GOOGLESPREADSHEETID'],
    os.environ['SPREADSHEETRANGE']
)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speak_output = "Olá! Posso te ajudar com sua dieta! Me peça alguma coisa, por exemplo, adicionar uma refeição."

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .response
        )


class ReadLastMealIntentHandler(AbstractRequestHandler):
    """Handler for ReadLastMeal Intent."""

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ReadLastMeal")(handler_input)

    def handle(self, handler_input):
        last_meal = spreadsheet.get_last_row()
        data = last_meal[0]
        meal = last_meal[1]
        hour = last_meal[3]
        food = last_meal[4]

        speak_output = f"Sua última refeição foi {meal} no dia {data} às {hour}. Você comeu {food}"

        return (
            handler_input.response_builder
            .speak(speak_output)
            .response
        )


class AddMealIntentHandler(AbstractRequestHandler):
    """Handler for AddMeal Intent."""

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AddMeal")(handler_input)

    def handle(self, handler_input):
        # Get Alexa slots values
        slots = handler_input.request_envelope.request.intent.slots
        meal = slots['meal'].value
        food = slots['food'].value
        local = slots['local'].value
        today = datetime.today().strftime("%d/%m/%Y")
        timezone = pytz.timezone("America/Sao_Paulo")
        current_time = datetime.now(timezone).strftime("%H:%M")

        spreadsheet.create_row(
            today,
            meal,
            local,
            current_time,
            food,
            'N/A',
            'N/A'
        )

        speak_output = "Sua refeição foi adicionada!"

        return (
            handler_input.response_builder
            .speak(speak_output)
            .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = "Posso te ajudar a organizar sua dieta! Me pergunte, qual a minha última refeição."

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        speak_output = "Tchau!"

        return (
            handler_input.response_builder
            .speak(speak_output)
            .response
        )


class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, não entendi."
        reprompt = "Pode repetir?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # Any cleanup logic goes here.
        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """

    def can_handle(self, handler_input):
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
            .speak(speak_output)
            # .ask("add a reprompt if you want to keep the session open for the user to respond")
            .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """

    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        logger.error(exception, exc_info=True)

        speak_output = "Desculpe, Tive um problema. Pode me perguntar novamente?"

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(ReadLastMealIntentHandler())
sb.add_request_handler(AddMealIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
# make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers
sb.add_request_handler(IntentReflectorHandler())

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
