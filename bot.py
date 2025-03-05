from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount
import azure.cognitiveservices.speech as speechsdk

# Speech 
SPEECH_KEY = "3c358ec45fdc4e6daeecb7a30002a9df"
SPEECH_REGION = "westus2"

def recognize_speech():
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    audio_config = speechsdk.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Say something...")
    result = speech_recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return "Sorry, I didn't understand."
    elif result.reason == speechsdk.ResultReason.Canceled:
        return "Speech recognition canceled."

class VoiceBot(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        recognized_text = recognize_speech()
        await turn_context.send_activity(MessageFactory.text(f"You said: {recognized_text}"))

    async def on_members_added_activity(self, members_added, turn_context: TurnContext):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello! Say something and I'll recognize it.")

