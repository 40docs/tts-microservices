from config import SPEECH_KEY, SPEECH_REGION, VOICE, OUTPUT_DIR
import azure.cognitiveservices.speech as speechsdk

OUTPUT_DIR.mkdir(exist_ok=True)

def synthesize(text: str, filename: str = "output") -> str:
    audio_path = OUTPUT_DIR / f"{filename}.mp3"

    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    speech_config.speech_synthesis_voice_name = VOICE
    speech_config.set_speech_synthesis_output_format(
        speechsdk.SpeechSynthesisOutputFormat.Audio48Khz192KBitRateStereoMp3
    )

    audio_config = speechsdk.audio.AudioOutputConfig(filename=str(audio_path))
    synthesizer = speechsdk.SpeechSynthesizer(speech_config, audio_config)

    result = synthesizer.speak_text_async(text).get()
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return str(audio_path)
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation = result.cancellation_details
        raise RuntimeError(f"TTS failed: {cancellation.reason} - {cancellation.error_details}")
