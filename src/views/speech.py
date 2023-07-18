import os
import azure.cognitiveservices.speech as speechsdk

from flask import Blueprint, render_template, request, jsonify, current_app
from datetime import datetime
from ..models.speech import Speech
from ..db import db


bp = Blueprint("speech", __name__, url_prefix="/speech")


@bp.route("/list", methods=["GET"], endpoint="list")
def list():
    page = request.args.get("page", 1, type=int)
    # load 20 speechs per page temporarily
    per_page = 30
    # speechs = db.paginate(
    #     select=db.select(Speech).order_by(Speech.created_at),
    #     page=page, per_page=per_page, count=True)
    speechs = Speech.query.order_by(
        Speech.created_at.desc()).paginate(page=page, per_page=per_page, count=True)
    return render_template("index.html", speechs=speechs)


@bp.route("/save", methods=["POST"])
def save():
    try:
        input_text = request.form.get("input-text")
        desc = request.form.get("input-desc")
        process(input_text, desc)
        print(current_app.static_folder)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "failed", "message": str(e)})


def process(input_text, desc):
    now = datetime.now().strftime("%y%m%d%H%M%S")

    if not desc:
        desc = input_text[:40] + "..."

    descs = desc.split()
    filename = "_".join(descs[:5])
    filename = f"{filename}_{now}.wav"

    relative_filepath = f"speech/{filename}"
    normalized_filepath = os.path.normpath(f"{current_app.static_folder}/{relative_filepath}")

    if not os.path.exists(f"{current_app.static_folder}{os.sep}speech"):
        os.makedirs(f"{current_app.static_folder}{os.sep}speech")

    speech_key, service_region = os.environ.get("MS_SPEECH_KEY"), os.environ.get("MS_SPEECH_REGION")
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # Set the voice name, refer to https://aka.ms/speech/voices/neural for full list.
    # speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"

    # Creates an audio configuration that points to an audio file.
    audio_config = speechsdk.audio.AudioOutputConfig(
        use_default_speaker=False, filename=normalized_filepath)

    # Creates a speech synthesizer using the default speaker as audio output.
    speech_synthesizer = speechsdk.SpeechSynthesizer(
        speech_config=speech_config, audio_config=audio_config)

    # Receives a text
    # text = input()
    text = input_text
    xml = make_xml(text)
    # xml = get_demo_en_xml()

    # Synthesizes the received text to speech. If use_default_speaker=True,
    # the speech is expected to be heard on the speaker with this line executed.
    # result = speech_synthesizer.speak_text_async(text).get()
    result = speech_synthesizer.speak_ssml_async(xml).get()

    # Checks result.
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized to speaker for text [{}]".format(text))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
        print("Did you update the subscription info?")

    # save to Speech model
    speech = Speech(user_id=1, filepath=relative_filepath, desc=desc, text=text)
    db.session.add(speech)
    db.session.commit()

    # if dont use AudioOutputConfig, use this code to save to file
    # stream = speechsdk.AudioDataStream(result)
    # stream.save_to_wav_file_async(f"{file_path}")


def make_xml(text, **kwargs):
    """Make SSML XML
    doc: https://learn.microsoft.com/zh-cn/azure/cognitive-services/speech-service/speech-synthesis-markup-voice

    Args:
        text: input text from user
        kwargs: dict

    Returns:
        str: xml
    """
    xml = '''
    <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"
        xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="{lang}">
        <voice name="{voice_name}">
            <mstts:express-as style="{voice_style}" >
                {text}
            </mstts:express-as>
        </voice>
    </speak>'''

    if "lang" not in kwargs:
        # en-US, zh-CN
        kwargs["lang"] = "en-US"

    if "voice_name" not in kwargs:
        kwargs["voice_name"] = "en-US-JennyNeural"

    if "voice_effect" not in kwargs:
        # eq_car, eq_telecomhp8k
        kwargs["voice_effect"] = "eq_car"

    if "voice_style" not in kwargs:
        # assistant, calm, chat, documentary-narration, friendly, gentle, empathetic
        # newscast, poetry-reading, sad, depressed, cheerful, serious, lyrical
        # excited, customerservice, envious, hopeful
        kwargs["voice_style"] = "chat"

    if "voice_role" not in kwargs:
        # Girl, YoungAdultFemale, OlderAdultFemale, SeniorAdultFemale
        # Boy, YoungAdultMale, OlderAdultMale, SeniorAdultMale
        kwargs["voice_role"] = "YoungAdultFemale"

    if "voice_rate" not in kwargs:
        # <prosody> tag
        # default, x-slow, slow, medium, fast, x-fast
        kwargs["voice_rate"] = "default"

    if "volume" not in kwargs:
        # <prosody> tag
        # default, silent, x-soft, soft, medium, loud, x-loud, +20.00%
        kwargs["volume"] = "default"

    table = str.maketrans({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;"
    })

    text = text.translate(table)
    kwargs["text"] = text

    return xml.format(**kwargs)


def get_demo_cn_xml():
    return '''
    <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"
        xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="zh-CN">
        <voice name="zh-CN-XiaomoNeural">
            女儿看见父亲走了进来，问道：
            <mstts:express-as role="YoungAdultFemale" style="calm">
                “您来的挺快的，怎么过来的？”
            </mstts:express-as>
            父亲放下手提包，说：
            <mstts:express-as role="OlderAdultMale" style="calm">
                “刚打车过来的，路上还挺顺畅。”
            </mstts:express-as>
        </voice>
    </speak>
    '''
