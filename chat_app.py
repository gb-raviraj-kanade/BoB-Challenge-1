from io import BytesIO
import os
from uuid import uuid4
import chainlit as cl
from chainlit.input_widget import Select
from chainlit.element import ElementBased
import phoenix as px
import llama_index.core
from pydub import AudioSegment

from app.agent_chat import Agent
from app.azure_utils.speech import speech_to_text
from app.config import AzureLanguages, Config

px.launch_app()
llama_index.core.set_global_handler("arize_phoenix")
audio_dir = "audio"

@cl.on_chat_start
async def start():
    settings =  await cl.ChatSettings(
        [
            Select(
                    id="User",
                    label="User",
                    values=["Customer1", "Customer2", "Customer3", "Customer4", "Customer5", 
                            "Customer6", "Customer7", "Customer8", "Customer9", "Customer10"],
                    initial_index=0,
                ),
            Select(
                id="Language",
                label="Voice Language",
                values=["English", "Hindi", "Bengali", "Gujarati", "Kannada", "Malayalam", 
                        "Marathi", "Punjabi", "Tamil", "Telugu", "Urdu"],
                initial_index=0,
            )
        ]
    ).send()

    agent = Agent(settings["User"])
    cl.user_session.set("agent", agent)
    cl.user_session.set("language", settings["Language"])

    start_message = await cl.Message(
        author="Assistant", content=Config.GreetingMessage.format(CustomerName=settings["User"])
    ).send()
    cl.user_session.set("start_message", start_message)

@cl.on_settings_update
async def setup_agent(settings):
    print("on_settings_update", settings)
    agent = Agent(settings["User"])
    cl.user_session.set("agent", agent)
    cl.user_session.set("language", settings["Language"])
    start_message = cl.user_session.get("start_message")
    start_message.content = Config.GreetingMessage.format(CustomerName=settings["User"])
    await start_message.update()

@cl.on_message
async def main(message: cl.Message):
    agent = cl.user_session.get("agent")
    response = agent.chat(message.content)
    await cl.Message(author="Assistant", content=response).send()

@cl.on_audio_chunk
async def on_audio_chunk(chunk: cl.AudioChunk):
    if chunk.isStart:
        buffer = BytesIO()
        # This is required for whisper to recognize the file type
        buffer.name = f"input_audio.{chunk.mimeType.split('/')[1]}"
        # Initialize the session for a new audio stream
        cl.user_session.set("audio_buffer", buffer)
        cl.user_session.set("audio_mime_type", chunk.mimeType)

    # Write the chunks to a buffer and transcribe the whole audio at the end
    cl.user_session.get("audio_buffer").write(chunk.data)

@cl.on_audio_end
async def on_audio_end(elements: list[ElementBased]):
    # Get the audio buffer from the session
    audio_buffer: BytesIO = cl.user_session.get("audio_buffer")
    audio_buffer.seek(0)  # Move the file pointer to the beginning
    audio_file = audio_buffer.read()
    audio_mime_type: str = cl.user_session.get("audio_mime_type")
    language = cl.user_session.get("language")

    # input_audio_el = cl.Audio(
    #     mime=audio_mime_type, content=audio_file, name=audio_buffer.name
    # )
    # await cl.Message(
    #     author="You", 
    #     type="user_message",
    #     content="",
    #     elements=[input_audio_el, *elements]
    # ).send()

    filename = f"audio_recording_{uuid4().hex}.{audio_mime_type.split('/')[-1]}"
    file_path = os.path.join(audio_dir, filename)
    with open(file_path, "wb") as f:
        f.write(audio_file)
    print(f"Audio recording saved to: {file_path}")
    audio_data = AudioSegment.from_file(file_path, format="webm")
    audio_data = audio_data.set_sample_width(2)
    audio_data = audio_data.set_frame_rate(16000)
    audio_data = audio_data.set_channels(1)

    transcript = speech_to_text(audio_data.raw_data, AzureLanguages[language].value)
    await cl.Message(author="You", type="user_message", content=transcript).send()
    if transcript:
        agent = cl.user_session.get("agent")
        response = agent.chat(transcript)
        # await cl.Message(author="Assistant", content=response).send()

        # tts_response = text_to_speech(response)
        # output_audio_el = cl.Audio(
        #     name="output_audio",
        #     auto_play=True,
        #     mime="audio/wav",
        #     content=tts_response,
        # )
        answer_message = await cl.Message(content=response).send()

        # answer_message.elements = [output_audio_el]
        # await answer_message.update()

@cl.on_chat_end
async def end():
    agent = cl.user_session.get("agent")
    agent.summarize()
