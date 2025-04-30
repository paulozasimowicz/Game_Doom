import pygame
import os
from src.utils.constants import *

class HealthHeart:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = HEART_SIZE
        self.collected = False
        self.animation_time = 0
        self.animation_speed = 0.1
        self.pulse_scale = 1.0
        self.pulse_direction = 1
        self.images = []
        self.current_frame = 0
        self.load_images()

    def load_images(self):
        try:
            # Create Images folder if it doesn't exist
            if not os.path.exists('Images'):
                os.makedirs('Images')
                print("Created Images folder. Please add heart animation images.")
            
            # Try to load 8 frames first
            frame_count = 8
            while frame_count > 0:
                image_path = os.path.join('Images', f'heart{frame_count}.png')
                if os.path.exists(image_path):
                    break
                frame_count -= 1
            
            if frame_count == 0:
                print("No heart images found. Using fallback heart graphics.")
                return
            
            # Load all available frames
            for i in range(1, frame_count + 1):
                image_path = os.path.join('Images', f'heart{i}.png')
                if os.path.exists(image_path):
                    image = pygame.image.load(image_path)
                    image = image.convert_alpha()
                    image = pygame.transform.scale(image, (self.size, self.size))
                    self.images.append(image)
            
            print(f"Loaded {len(self.images)} heart animation frames from Images folder")
            
        except Exception as e:
            print(f"Error loading heart images: {e}")
            self.images = []

    def draw(self, screen, x, y, size):
        if self.collected:
            return
            
        # Update pulse animation
        self.animation_time += self.animation_speed
        if self.animation_time >= 0.2:
            self.animation_time = 0
            self.pulse_scale += 0.1 * self.pulse_direction
            if self.pulse_scale >= 1.2:
                self.pulse_direction = -1
            elif self.pulse_scale <= 0.8:
                self.pulse_direction = 1
        
        if self.images:
            # Draw the current animation frame
            scaled_size = int(size * self.pulse_scale)
            scaled_image = pygame.transform.scale(self.images[self.current_frame], 
                                               (scaled_size, scaled_size))
            screen.blit(scaled_image, (x - scaled_size//2, y - scaled_size//2))
        else:
            # Fallback to drawn heart
            scaled_size = int(size * self.pulse_scale)
            heart_points = [
                (x, y - scaled_size//2),  # Top
                (x - scaled_size//2, y),  # Left
                (x, y + scaled_size//2),  # Bottom
                (x + scaled_size//2, y)   # Right
            ]
            pygame.draw.polygon(screen, (255, 0, 0), heart_points) 