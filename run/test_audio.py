# import argparse

# import pyaudio
# from lit_checker.args import GlobalConfig
# from lit_checker.camera.camera_processor import CameraProcessor


# def main(yaml_config_path: str) -> None:
#     config = GlobalConfig.from_yaml(yaml_config_path)
#     camera_processor = CameraProcessor(config, verbose=False)
#     audio_recorder = AudioRecorder()
#     audio_recorder.start()
#     frames = camera_processor.run_capture_routine(maximum_frames=100)
#     audio_recorder.stop()
#     output_path = camera_processor.write_frames(frames)
#     print(f"Wrote frames at: {output_path}")


# class AudioRecorder():

#     # Audio class based on pyAudio and Wave
#     def __init__(self):
#         self.open = True
#         self.rate = 16000
#         self.frames_per_buffer = 1024
#         self.channels = 2
#         self.format = pyaudio.paInt16
#         self.audio_filename = "temp_audio.wav"
#         self.audio = pyaudio.PyAudio()
#         self.stream = self.audio.open(format=self.format,
#                                       channels=self.channels,
#                                       rate=self.rate,
#                                       input=True,
#                                       frames_per_buffer=self.frames_per_buffer)
#         self.audio_frames = []

#     # Audio starts being recorded

#     def record(self):

#         self.stream.start_stream()
#         while (self.open == True):
#             data = self.stream.read(self.frames_per_buffer)
#             self.audio_frames.append(data)
#             if self.open == False:
#                 break

#     # Finishes the audio recording therefore the thread too

#     def stop(self):

#         if self.open == True:
#             self.open = False
#             self.stream.stop_stream()
#             self.stream.close()
#             self.audio.terminate()

#             waveFile = wave.open(self.audio_filename, 'wb')
#             waveFile.setnchannels(self.channels)
#             waveFile.setsampwidth(self.audio.get_sample_size(self.format))
#             waveFile.setframerate(self.rate)
#             waveFile.writeframes(b''.join(self.audio_frames))
#             waveFile.close()

#         pass

#     # Launches the audio recording function using a thread
#     def start(self):
#         audio_thread = threading.Thread(target=self.record)
#         audio_thread.start()


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument(
#         "--cfg",
#         default="configs/c100/config_c100.yaml",
#         action="store",
#         type=str,
#         required=True,
#         help="YAML configuration file path",
#     )
#     args = parser.parse_args()
#     main(args.cfg)
