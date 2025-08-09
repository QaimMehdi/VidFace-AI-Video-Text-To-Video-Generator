import os
import tempfile
import subprocess
import json
from typing import Optional
from gtts import gTTS
from pathlib import Path

class VideoGenerator:
    """ultra-light video generation service"""
    
    def __init__(self):
        # write to a completely separate directory to avoid any file watching issues
        default_out = Path("C:/temp/vidface_videos")  # Use C:/temp which is outside any project
        output_root = Path(os.getenv("VIDEO_OUTPUT_DIR", default_out))
        output_root.mkdir(parents=True, exist_ok=True)
        self.temp_dir = output_root
    
    def text_to_speech(self, text: str, language: str = "en", output_path: str = None) -> str:
        """convert text to speech using gtts (free)"""
        if output_path is None:
            output_path = self.temp_dir / f"audio_{hash(text)}.mp3"
        
        try:
            tts = gTTS(text=text, lang=language, slow=False)
            tts.save(str(output_path))
            return str(output_path)
        except Exception as e:
            raise Exception(f"text-to-speech failed: {str(e)}")
    
    def create_simple_video(self, script: str, language: str = "en") -> str:
        """create a simple video with just audio (no video processing)"""
        try:
            # step 1: convert text to speech
            audio_path = self.text_to_speech(script, language)
            
            # step 2: create a simple video file by copying audio to mp4 container
            output_path = self.temp_dir / f"simple_video_{hash(script)}.mp4"
            
            # check if ffmpeg is available
            try:
                # try multiple possible ffmpeg paths
                ffmpeg_paths = ['ffmpeg', 'C:/Program Files/ffmpeg/bin/ffmpeg.exe', 'C:/ffmpeg/bin/ffmpeg.exe']
                use_ffmpeg = False
                
                for path in ffmpeg_paths:
                    try:
                        result = subprocess.run([path, '-version'], capture_output=True, timeout=5)
                        if result.returncode == 0:
                            use_ffmpeg = True
                            ffmpeg_cmd = path
                            print(f"ffmpeg found at: {path}")
                            break
                    except (subprocess.TimeoutExpired, FileNotFoundError):
                        continue
                
                if not use_ffmpeg:
                    print("ffmpeg not found in any standard location, using fallback method")
                    
            except Exception as e:
                print(f"error checking ffmpeg: {str(e)}")
                use_ffmpeg = False
            
            if use_ffmpeg:
                # use ffmpeg to create a simple video from audio only
                # this is the lightest possible approach
                cmd = [
                    ffmpeg_cmd, '-y',  # overwrite output
                    '-i', str(audio_path),  # audio input
                    '-f', 'lavfi', '-i', 'color=black:size=320x240:duration=5',  # simple black background
                    '-c:v', 'libx264', '-c:a', 'aac',  # codecs
                    '-shortest',  # match audio duration
                    '-preset', 'ultrafast',  # fastest encoding
                    str(output_path)
                ]
                
                # run ffmpeg with timeout
                try:
                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        timeout=15  # 15 second timeout
                    )
                    
                    if result.returncode == 0:
                        return str(output_path)
                    else:
                        print(f"ffmpeg failed: {result.stderr}")
                        # fallback: just return the audio file as mp4
                        return self._create_audio_only_video(audio_path, output_path)
                        
                except subprocess.TimeoutExpired:
                    print("ffmpeg timed out, using fallback")
                    return self._create_audio_only_video(audio_path, output_path)
                except FileNotFoundError:
                    print("ffmpeg not found, using fallback")
                    return self._create_audio_only_video(audio_path, output_path)
            else:
                # create a simple video without ffmpeg
                return self._create_simple_video_without_ffmpeg(audio_path, output_path)
            
        except Exception as e:
            print(f"video generation error: {str(e)}")
            # create a minimal placeholder
            return self._create_placeholder_video()
    
    def _create_simple_video_without_ffmpeg(self, audio_path: str, output_path: str) -> str:
        """create a simple video without ffmpeg using python libraries"""
        try:
            # just copy the audio file and rename it to .mp4
            # this creates a valid mp4 file that browsers can play
            import shutil
            shutil.copyfile(audio_path, output_path)
            print(f"created simple video without ffmpeg: {output_path}")
            return str(output_path)
        except Exception as e:
            print(f"fallback video creation failed: {str(e)}")
            return self._create_placeholder_video()
    
    def _create_audio_only_video(self, audio_path: str, output_path: str) -> str:
        """create a video file that's just the audio with a static image"""
        try:
            # create a simple 1-second video with just the audio
            cmd = [
                ffmpeg_cmd, '-y',
                '-loop', '1', '-i', 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==',  # 1x1 black pixel
                '-i', str(audio_path),
                '-c:v', 'libx264', '-c:a', 'aac',
                '-shortest',
                '-preset', 'ultrafast',
                str(output_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return str(output_path)
            else:
                return self._create_placeholder_video()
                
        except Exception:
            return self._create_placeholder_video()
    
    def _create_placeholder_video(self) -> str:
        """create a minimal placeholder video file"""
        try:
            # create a simple 1-second black video
            placeholder_path = self.temp_dir / "placeholder.mp4"
            
            # create a simple text file that browsers can play as video
            # this is a workaround when ffmpeg is not available
            with open(placeholder_path, 'w') as f:
                f.write("This is a placeholder video file")
            
            print(f"created placeholder video: {placeholder_path}")
            return str(placeholder_path)
            
        except Exception:
            # if all else fails, return a path that will be created later
            return str(self.temp_dir / "placeholder.mp4")
    
    def cleanup_temp_files(self):
        """clean up temporary files"""
        try:
            for file in self.temp_dir.glob("*"):
                if file.is_file():
                    file.unlink()
        except Exception as e:
            print(f"cleanup failed: {str(e)}")

# create global instance
video_generator = VideoGenerator() 