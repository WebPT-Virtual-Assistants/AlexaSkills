
from __future__ import print_function

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_sessionAttributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_sessionAttributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some sessionAttributes we could
    add those here
    """

    session_sessionAttributes = {}
    card_title = "Welcome"
    speech_output = "Welcome Web PT skill, I can create objective notes."
    reprompt_text = "You can ask me to create objective notes."
    should_end_session = False
    return build_response(session_sessionAttributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def ask_for_patient_name(session, ct=None, so=None):
    """ If we wanted to initialize the session to have some sessionAttributes we could
    add those here
    """
    card_title = "The patient name is required"
    speech_output = "Can you please provide the patient name?"
    if ct and so:
        card_title = ct
        speech_output = so
    session_sessionAttributes = session['attributes']

    reprompt_text = ""
    should_end_session = False
    return build_response(session_sessionAttributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))



def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for using Web PT skill "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))



def set_data_in_session(intent, session):
    card_title = intent['name']
    session_sessionAttributes = {}
    if "attributes" in session:
        session_sessionAttributes = session['attributes']
    should_end_session = False
    reprompt_text = ""
    speech_output = "Got it"
    return build_response(session_sessionAttributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def cancel_note(intent, session):
    card_title = intent['name']
    session_sessionAttributes = {}
    should_end_session = True
    reprompt_text = ""
    speech_output = "Notes Canceled"
    return build_response(session_sessionAttributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def end_note(intent, session):
    card_title = intent['name']
    session_sessionAttributes = {}
    should_end_session = True
    reprompt_text = ""
    speech_output = "ending note"
    if 'attributes' in session:
        if 'PR' not in session['attributes']:
            return ask_for_patient_name(session)
        if 'PR' not in session['attributes']:
            return ask_for_patient_name(session,"PR value is required","Please provide PR value")
        if 'RR' not in session['attributes']:
            return ask_for_patient_name(session,"RR value is required","Please provide RR value")
        #if 'BP' not in session['attributes']:
            #return ask_for_patient_name(session,"BP value is required","Please provide BP value")
        if 'temp' not in session['attributes']:
            return ask_for_patient_name(session,"Temperature value is required","Please provide temperature value")
        for attr in session['attributes']:
            name = session['attributes'][attr]['name'] 
            value = session['attributes'][attr]['value']
            speech_output += name+" = "+value+", "
    return build_response(session_sessionAttributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


#for required slots       
def delegate():
    return build_response({},{"directives": [{  "type": "Dialog.Delegate"  }]})


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()

def checkForSlotValue(intent,slot):
    if slot in intent['slots']:
        if 'value' in intent['slots'][slot]:
            return True
    return False

def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """
    valueIntents = ["BPIntent","RRIntent","PRIntent","TempIntent"]

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    
    if intent_name == "EndObjectiveNotes":
       return end_note(intent,session)
    if intent_name == "CancelObjectiveNotes":
        return cancel_note(intent, session)

    # Dispatch to your skill's intent handlers
    if intent_name == "CreateObjectiveNotes":
        if 'attributes' not in session:
            session['attributes'] = {}
        add_slots_session(intent,session)
        return set_data_in_session(intent, session)
    if intent_name in valueIntents:
        if 'attributes' in session:
            add_slots_session(intent,session)
            if 'patientname' in session['attributes']:
                return set_data_in_session(intent,session)
            else:
                return ask_for_patient_name(session) 
        else:
            session['attributes'] = {}
            add_slots_session(intent,session)
            return ask_for_patient_name(session) 

    else:
        raise ValueError("Invalid intent")

def add_slots_session(intent,session):
    for slot_name in intent['slots']:
        slot = intent['slots'][slot_name]
        if 'resolutions' in slot:
            del slot['resolutions']
        session['attributes'][slot['name']] = slot

def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
