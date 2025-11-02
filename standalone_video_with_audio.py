import cv2
import pygame
import sys
import os
import time

# --- Configuration ---
VIDEOLIST_FILE = 'videolist.txt'
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FADE_DURATION_MS = 1500
DEFAULT_FPS = 25
PYGAME_MIXER_SETTINGS = {
    "frequency": 44100,
    "size": -16,
    "channels": 2,
    "buffer": 512
}

# --- Helper Functions ---

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- Core Functions ---

def parse_videolist(filename):
    """Parses the videolist into a structured list of playback jobs."""
    if not os.path.exists(filename):
        print(f"Error: '{filename}' not found!")
        sys.exit(1)

    jobs = []
    mode = 'per_video'
    continuous_job = None

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            parts = [p.strip() for p in line.split(',', 1)]
            command = parts[0].upper()
            
            if command == 'CONTINUOUS_AUDIO_GROUP':
                if mode == 'continuous': jobs.append(continuous_job)
                audio_file = parts[1] if len(parts) > 1 and parts[1] else None
                if audio_file:
                    mode = 'continuous'
                    continuous_job = {"type": "continuous_audio", "audio": audio_file, "videos": []}
                else:
                    print("Warning: CONTINUOUS_AUDIO_GROUP requires an audio file.")
                continue

            if command == 'END_CONTINUOUS_AUDIO_GROUP':
                if mode == 'continuous' and continuous_job: jobs.append(continuous_job)
                continuous_job = None
                mode = 'per_video'
                continue

            video_file = parts[0]
            if mode == 'continuous' and continuous_job is not None:
                continuous_job["videos"].append(video_file)
            else:
                audio_file = None
                if len(parts) > 1:
                    if not parts[1]: audio_file = video_file.replace('.mp4', '.mp3')
                    else: audio_file = parts[1]
                jobs.append({"type": "per_video", "video": video_file, "audio": audio_file})

    if mode == 'continuous' and continuous_job: jobs.append(continuous_job)
    return jobs

def check_files_exist(jobs):
    """Checks that all specified video and audio files exist."""
    all_ok = True
    for job in jobs:
        if job["type"] == "per_video":
            if not os.path.exists(resource_path(job["video"])):
                print(f"Error: Video file not found: {job['video']}")
                all_ok = False
            if job["audio"] and not os.path.exists(resource_path(job["audio"])):
                print(f"Error: Audio file not found: {job['audio']}")
                all_ok = False
        elif job["type"] == "continuous_audio":
            if job["audio"] and not os.path.exists(resource_path(job["audio"])):
                print(f"Error: Continuous audio file not found: {job['audio']}")
                all_ok = False
            for video in job["videos"]:
                if not os.path.exists(resource_path(video)):
                    print(f"Error: Video file not found: {video}")
                    all_ok = False
    return all_ok

def play_sequence(screen, clock, jobs):
    """Plays the sequence of jobs using Pygame for display with audio fading."""

    def play_video_frame(cap, fps, do_fade_out=False):
        # --- Calculate scaling and centering ---
        video_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        video_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        
        window_aspect = WINDOW_WIDTH / WINDOW_HEIGHT
        video_aspect = video_width / video_height

        if video_aspect > window_aspect:
            scaled_width = WINDOW_WIDTH
            scaled_height = int(scaled_width / video_aspect)
        else:
            scaled_height = WINDOW_HEIGHT
            scaled_width = int(scaled_height * video_aspect)

        pos_x = (WINDOW_WIDTH - scaled_width) // 2
        pos_y = (WINDOW_HEIGHT - scaled_height) // 2
        # --- End of scaling logic ---

        fade_frames = fps * (FADE_DURATION_MS / 1000.0)
        fade_out_triggered = False
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    pygame.mixer.music.stop()
                    cap.release()
                    return False  # Signal to exit main loop

            current_frame_pos = cap.get(cv2.CAP_PROP_POS_FRAMES)
            if do_fade_out and not fade_out_triggered and (total_frames - current_frame_pos) <= fade_frames:
                pygame.mixer.music.fadeout(FADE_DURATION_MS)
                fade_out_triggered = True

            ret, frame = cap.read()
            if not ret:
                running = False
                break

            frame_resized = cv2.resize(frame, (scaled_width, scaled_height))
            frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
            video_surf = pygame.surfarray.make_surface(frame_rgb.swapaxes(0, 1))
            
            screen.fill((0, 0, 0))
            screen.blit(video_surf, (pos_x, pos_y))
            pygame.display.flip()

            clock.tick(fps)
        return True

    for i, job in enumerate(jobs):
        if job["type"] == "per_video":
            video_file, audio_file = job["video"], job["audio"]
            print(f"Playing: {video_file}" + (f" with {audio_file}" if audio_file else " (silent)"))

            cap = cv2.VideoCapture(resource_path(video_file))
            if not cap.isOpened():
                print(f"Error: Could not open video file: {video_file}")
                continue

            fps = cap.get(cv2.CAP_PROP_FPS) or DEFAULT_FPS

            has_audio = audio_file and pygame.mixer.get_init()
            if has_audio:
                try:
                    audio_full_path = resource_path(audio_file)
                    print(f"Attempting to load audio: {audio_full_path}")
                    pygame.mixer.music.load(audio_full_path)
                    pygame.mixer.music.play(loops=-1, fade_ms=FADE_DURATION_MS)
                    print(f"Audio {audio_file} started successfully.")
                except pygame.error as e:
                    print(f"Error playing audio {audio_file}: {e}")
                    print("Audio will be disabled for this video.")
                    has_audio = False

            if not play_video_frame(cap, fps, do_fade_out=has_audio):
                return False

            if has_audio:
                while pygame.mixer.music.get_busy(): time.sleep(0.01)
            cap.release()

        elif job["type"] == "continuous_audio":
            audio_file, video_list = job["audio"], job["videos"]
            print(f"Starting continuous audio: {audio_file}")

            has_audio = audio_file and pygame.mixer.get_init()
            if has_audio:
                try:
                    audio_full_path = resource_path(audio_file)
                    print(f"Attempting to load continuous audio: {audio_full_path}")
                    pygame.mixer.music.load(audio_full_path)
                    # Fade in only on the first video of the group
                    pygame.mixer.music.play(loops=-1, fade_ms=FADE_DURATION_MS)
                    print(f"Continuous audio {audio_file} started successfully.")
                except pygame.error as e:
                    print(f"Error playing continuous audio {audio_file}: {e}")
                    print("Continuous audio will be disabled.")
                    has_audio = False

            for idx, video_file in enumerate(video_list):
                print(f"  _ Playing video: {video_file}")
                cap = cv2.VideoCapture(resource_path(video_file))
                if not cap.isOpened():
                    print(f"Error: Could not open video file: {video_file}")
                    continue

                fps = cap.get(cv2.CAP_PROP_FPS) or DEFAULT_FPS
                is_last_video = (idx == len(video_list) - 1)

                if not play_video_frame(cap, fps, do_fade_out=(has_audio and is_last_video)):
                    return False
                
                cap.release()

            if has_audio:
                while pygame.mixer.music.get_busy(): time.sleep(0.01)

    return True

# --- Main Execution ---

def main():
    """Main function to run the program."""
    # --- Pygame Initialization ---
    try:
        pygame.mixer.init(**PYGAME_MIXER_SETTINGS)
        print("Pygame mixer initialized successfully.")
    except pygame.error as e:
        print(f"Warning: Could not initialize Pygame mixer. Error: {e}")
        print("Audio will be disabled.")

    pygame.init()
    print("Pygame fully initialized.")
    print(f"Pygame mixer status after init: {pygame.mixer.get_init()}")

    # --- Job and File Validation ---
    job_sequence = parse_videolist(resource_path(VIDEOLIST_FILE))
    
    if not job_sequence:
        print("The videolist is empty. Nothing to play.")
        if pygame.mixer.get_init():
            pygame.mixer.quit()
        pygame.quit()
        return

    if not check_files_exist(job_sequence):
        print("\nPlease check the filenames in your videolist and try again.")
        if pygame.mixer.get_init():
            pygame.mixer.quit()
        pygame.quit()
        sys.exit(1)

    # --- Pygame Window Setup ---
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Video Sequence")
    clock = pygame.time.Clock()

    # --- Main Loop ---
    play_sequence(screen, clock, job_sequence)

    # --- Shutdown ---
    if pygame.mixer.get_init():
        pygame.mixer.quit()
    pygame.quit()
    print("Sequence finished!")


if __name__ == '__main__':
    main()