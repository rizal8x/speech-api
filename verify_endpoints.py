import requests
import time
import sys

BASE_URL = "http://localhost:8000"

def wait_for_server():
    print("Waiting for server...")
    for _ in range(30):
        try:
            resp = requests.get(f"{BASE_URL}/health")
            if resp.status_code == 200:
                print("Server is up!")
                return
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(1)
    print("Server failed to start.")
    sys.exit(1)

def test_tts():
    print("\nTesting TTS...")
    text = "Hello, this is a test of the speech API running on a mini PC."
    start = time.time()
    resp = requests.post(f"{BASE_URL}/v1/speech/tts", json={"text": text})
    duration = time.time() - start
    
    if resp.status_code == 200:
        with open("test_output.wav", "wb") as f:
            f.write(resp.content)
        print(f"TTS Success! Saved to test_output.wav. Time: {duration:.2f}s")
        return "test_output.wav"
    else:
        print(f"TTS Failed: {resp.text}")
        sys.exit(1)

def test_stt(audio_path):
    print("\nTesting STT...")
    start = time.time()
    with open(audio_path, "rb") as f:
        files = {"file": (audio_path, f, "audio/wav")}
        resp = requests.post(f"{BASE_URL}/v1/speech/stt", files=files)
    duration = time.time() - start
    
    if resp.status_code == 200:
        result = resp.json()
        print(f"STT Success! Text: {result.get('text')}")
        print(f"Time: {duration:.2f}s")
        print(f"Metadata: {result}")
    else:
        print(f"STT Failed: {resp.text}")
        sys.exit(1)

if __name__ == "__main__":
    wait_for_server()
    audio_file = test_tts()
    test_stt(audio_file)
