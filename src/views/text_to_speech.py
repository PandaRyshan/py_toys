# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root
# for full license information.

# <code>
import os
import azure.cognitiveservices.speech as speechsdk

from flask import Blueprint, request, jsonify


bp = Blueprint("ms", __name__, url_prefix="/ms")


@bp.route("/start", methods=["POST"])
def start():
    input_text = request.form.get("input-text")
    print(input_text)
    process(input_text)
    return jsonify({"message": "success"})


def process(input_text):
    # Creates an instance of a speech config with specified subscription key and
    # service region.
    # Replace with your own subscription key and service region (e.g., "westus").
    speech_key, service_region = os.environ.get("MS_SPEECH_KEY"), os.environ.get("MS_SPEECH_REGION")
    print(speech_key, service_region)
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # Set the voice name, refer to https://aka.ms/speech/voices/neural for full list.
    speech_config.speech_synthesis_voice_name = "en-US-AriaNeural"

    # Creates a speech synthesizer using the default speaker as audio output.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    # Receives a text from console input.
    # text = input()
    print("Type some text that you want to speak...")
    text = input_text

    # Synthesizes the received text to speech.
    # The synthesized speech is expected to be heard on the speaker with this line executed.
    result = speech_synthesizer.speak_text_async(text).get()

    # Checks result.
    # if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    #     print("Speech synthesized to speaker for text [{}]".format(text))
    # elif result.reason == speechsdk.ResultReason.Canceled:
    #     cancellation_details = result.cancellation_details
    #     print("Speech synthesis canceled: {}".format(cancellation_details.reason))
    #     if cancellation_details.reason == speechsdk.CancellationReason.Error:
    #         if cancellation_details.error_details:
    #             print("Error details: {}".format(cancellation_details.error_details))
    #     print("Did you update the subscription info?")

    stream = speechsdk.AudioDataStream(result)
    stream.save_to_wav_file("output.wav")
    # </code>
