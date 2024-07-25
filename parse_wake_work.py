import pyaudio
import wave
import os
import asyncio 

async def record_audio(output_filename, duration=5, sample_rate=16000, channels=1):
    chunk = 1024
    audio_format = pyaudio.paInt16
    
    paudio = pyaudio.PyAudio()
    stream = paudio.open(format=audio_format, channels=channels, rate=sample_rate, input=True, frames_per_buffer=chunk)
    
    frames = []
    
    for i in range(int(sample_rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)
    
    stream.stop_stream()
    stream.close()
    paudio.terminate()
    
    wavefile = wave.open(output_filename, 'wb')
    wavefile.setnchannels(channels)
    wavefile.setsampwidth(paudio.get_sample_size(audio_format))
    wavefile.setframerate(sample_rate)
    wavefile.writeframes(b''.join(frames))
    wavefile.close()
    
    
async def parse_audio(input_filename):
    import whisper
    model = whisper.load_model("base")
    result = model.transcribe(input_filename)
    print(result["text"])
    return result
    
    
async def parse_wake_work(transcription):
    if "banana" in transcription:
        print("Found banana!!")
        return True
    
while True:
    pool = asyncio.new_event_loop()
    pool.run_until_complete(record_audio('test.wav'))
    pool.run_until_complete(transcript = parse_audio('test.wav'))
    pool.run_until_complete(parse_wake_word = transcript['text'])