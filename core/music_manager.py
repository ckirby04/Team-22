import os
import random
import pygame
from settings import MUSIC_DIR, HELMET_SOUNDS_DIR

# Custom event for when a music track ends
MUSIC_END_EVENT = pygame.USEREVENT + 1


class MusicManager:
    def __init__(self):
        self._tracks = []
        self._sounds = {}

        # Discover MP3 tracks
        if os.path.isdir(MUSIC_DIR):
            for f in sorted(os.listdir(MUSIC_DIR)):
                if f.lower().endswith(".mp3"):
                    self._tracks.append(os.path.join(MUSIC_DIR, f))

        # Preload helmet WAV sounds (skip 0-byte files)
        if os.path.isdir(HELMET_SOUNDS_DIR):
            for f in os.listdir(HELMET_SOUNDS_DIR):
                if f.lower().endswith(".wav"):
                    path = os.path.join(HELMET_SOUNDS_DIR, f)
                    if os.path.getsize(path) > 0:
                        try:
                            self._sounds[f] = pygame.mixer.Sound(path)
                        except Exception as e:
                            print(f"Could not load sound {f}: {e}")

        pygame.mixer.music.set_endevent(MUSIC_END_EVENT)

    def play_random_track(self):
        if not self._tracks:
            return
        track = random.choice(self._tracks)
        try:
            pygame.mixer.music.load(track)
            pygame.mixer.music.play()
        except Exception as e:
            print(f"Music playback error: {e}")

    def handle_music_end_event(self):
        self.play_random_track()

    def play_sound(self, filename):
        sound = self._sounds.get(filename)
        if sound:
            sound.play()

    def stop(self):
        try:
            pygame.mixer.music.stop()
            pygame.mixer.stop()
        except Exception:
            pass
