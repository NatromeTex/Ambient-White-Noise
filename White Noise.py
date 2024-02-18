import pygame
import os

# Define sound file paths and initial volumes
pygame.mixer.init(channels=8)  # Initialize with 8 channels for surround sound
sounds = {
    "rain": os.path.join("sounds", "rain.wav"),
    "sea": os.path.join("sounds", "sea.wav"),
    "city": os.path.join("sounds", "city.wav"),
    "airplane": os.path.join("sounds", "airplane.wav"),
    "car_engine": os.path.join("sounds", "car_engine.wav"),
}
volumes = {key: 0 for key in sounds}  # Set initial volume to 50% for each sound

# Create Pygame window and UI elements
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sound Loop Player")

font = pygame.font.SysFont(None, 24)
sound_labels = {
    sound: font.render(sound.capitalize(), True, (255, 255, 255))
    for sound in sounds
}
volume_labels = {
    sound: font.render("Volume:", True, (255, 255, 255))
    for sound in sounds
}
volume_sliders = {
    sound: pygame.Rect(100, 50 + index * 50, 200, 20)  # Adjust positions as needed
    for index, sound in enumerate(sounds)
}

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle button clicks for sound toggling
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for sound, rect in volume_sliders.items():
                if rect.collidepoint(pos):
                    is_playing = pygame.mixer.Channel(sounds[sound].get_channels()).get_busy()
                    if is_playing:
                        pygame.mixer.Channel(sounds[sound].get_channels()).fadeout(500)  # Fade out gracefully
                    else:
                        sound_channel = pygame.mixer.Channel(sounds[sound].get_channels())
                        sound_channel.queue(sounds[sound])
                        sound_channel.set_volume(volumes[sound])  # Set volume based on slider
                        sound_channel.play()

    # Update UI elements and screen
    screen.fill((0, 0, 0))  # Clear the screen

    for sound, rect in volume_sliders.items():
        pygame.draw.rect(screen, (255, 255, 255), rect)
        volume_slider_rect = pygame.Rect(rect.x + 5, rect.y + 5, rect.width - 10, rect.height - 10)
        pygame.draw.rect(screen, (0, 255, 0) if volumes[sound] >= 0.5 else (255, 0, 0), volume_slider_rect)

    for sound, label in sound_labels.items():
        screen.blit(label, (10, 50 + 50 * sounds.index(sound)))
    for sound, label in volume_labels.items():
        screen.blit(label, (10, 75 + 50 * sounds.index(sound)))

    pygame.display.flip()

pygame.quit()
