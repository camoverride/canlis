import cv2
import pygame
import time
import sys



def play_loop_pingpong(video_path, duration_of_first_frame):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    vw = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    vh = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    pygame.init()
    screen = pygame.display.set_mode((vw, vh), pygame.FULLSCREEN)
    clock = pygame.time.Clock()

    # --- SMART PRE-LOADING ---
    print("Pre-loading video to RAM for seamless reverse playback...")
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Convert BGR (OpenCV) to RGB, then to a Pygame Surface
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frames.append(pygame.surfarray.make_surface(rgb.swapaxes(0, 1)))
    cap.release()
    
    if not frames:
        print("Error: Video is empty.")
        return

    first_surface = frames[0]

    print(f"Loaded {len(frames)} frames. Starting playback...")

    while True:
        # 1. STATIC FIRST FRAME
        screen.blit(first_surface, (0, 0))
        pygame.display.flip()
        
        start = time.time()
        while time.time() - start < duration_of_first_frame:
            if pygame.event.get(pygame.QUIT): pygame.quit(); sys.exit()
            clock.tick(10)

        # 2. PLAY FORWARD
        for surface in frames:
            if pygame.event.get(pygame.QUIT): pygame.quit(); sys.exit()
            screen.blit(surface, (0, 0))
            pygame.display.flip()
            clock.tick(fps)

        # 3. PLAY IN REVERSE
        for surface in frames[-2::-1]:
            if pygame.event.get(pygame.QUIT): pygame.quit(); sys.exit()
            screen.blit(surface, (0, 0))
            pygame.display.flip()
            clock.tick(fps)

play_loop_pingpong("applied.mp4", 5)