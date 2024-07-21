def list_audio_devices():
#     p = pyaudio.PyAudio()
#     print("Available audio devices:")
#     for i in range(p.get_device_count()):
#         info = p.get_device_info_by_index(i)
#         print(f"{info['index']}: {info['name']} (Input Channels: {info['maxInputChannels']})")
#     p.terminate()