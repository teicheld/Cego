import pygame
from pygame.locals import *
import os

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Kartenspiel")

# Initialize pygame display
pygame.init()

# Create a clock object to control frame rate
clock = pygame.time.Clock()

# Load card images
karten_ordner = "Karten"
karten_dateien = [file for file in os.listdir(karten_ordner) if file.endswith(".png")]
karten_bilder = [pygame.image.load(os.path.join(karten_ordner, datei)) for datei in karten_dateien]


# 1. Überprüfung der Benutzereingabe für die Anzahl der Spieler in der Lobby
anzahl_spieler = int(input("Geben Sie die Anzahl der Spieler ein (maximal 7): "))
if anzahl_spieler < 1 or anzahl_spieler > 7:
    print("Ungültige Anzahl der Spieler!")
    exit()

class SpielerInfo:
    def __init__(self, name, hand, kombiniertes_bild):
        self.name = name
        self.hand = hand
        self.kombiniertes_bild = kombiniertes_bild

class Karte:
    def __init__(self, name, bild, wert):
        self.name = name
        self.bild = bild
        self.wert = wert

# 2. Eingabe der Spielernamen und Erstellen der Spielerliste
spieler = []
for i in range(anzahl_spieler):
    spielername = input(f"Geben Sie den Namen für Spieler {i + 1} ein: ")
    spieler.append(SpielerInfo(spielername, [], []))
    
# 4. Neue Kartenliste vor jeder Runde erstellen
karten = []
karten_ordner = "Karten"
karten_dateien = [file for file in os.listdir(karten_ordner) if file.endswith(".png")]

# Wertzuordnung für jede Karte (Beispielwerte)
karten_werte = {
    "1.png": 1,
    "2.png": 2,
    "3.png": 3,
    "4.png": 4,
    "5.png": 5,
    "6.png": 6,
    "7.png": 7,
    "8.png": 8,
    "9.png": 9,
    "10.png": 10,
    "11.png": 11,
    "12.png": 12,
    "13.png": 13,
    "14.png": 14,
    "15.png": 15,
    "16.png": 16,
    "17.png": 17,
    "18.png": 18,
    "19.png": 19,
    "20.png": 20,
    "21.png": 21,
    "Bube.png": 22,

}

for datei in karten_dateien:
    bild = pygame.image.load(os.path.join(karten_ordner, datei)).convert_alpha()
    name = datei.split(".")[0]
    wert = karten_werte.get(name, 0)
    karten.append(Karte(name, bild, wert))

# 6. Karten gleichmäßig auf die Spieler verteilen
anzahl_karten_pro_spieler = len(karten) // anzahl_spieler
for spieler_idx in range(anzahl_spieler):
    for _ in range(anzahl_karten_pro_spieler):
        karte = karten.pop()
        spieler[spieler_idx].hand.append(karte)

image_cache = []

class VerschiebbaresBild:
    def __init__(self, canvas, image, x, y):
        self.canvas = canvas
        self.image = image
        self.id = canvas.create_image(x, y, image=image, anchor=NW)
        self.original_position = (x, y)  # Store the original position
        self.drag_data = {"x": 0, "y": 0}
        self.canvas.tag_bind(self.id, "<ButtonPress-1>", self.start_drag)
        self.canvas.tag_bind(self.id, "<B1-Motion>", self.drag)
        self.canvas.tag_bind(self.id, "<ButtonRelease-1>", self.release_drag)

    def start_drag(self, event):
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def drag(self, event):
        delta_x = event.x - self.drag_data["x"]
        delta_y = event.y - self.drag_data["y"]
        self.canvas.move(self.id, delta_x, delta_y)
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def release_drag(self, event):
        # Return the image to its original position
        self.canvas.coords(self.id, self.original_position[0], self.original_position[1])

# 8. Kombiniertes Bild für jeden Spieler erstellen und anzeigen
for spieler_info in spieler:
    hand = spieler_info.hand
    hand_name = spieler_info.name
    hand_winkel_list = [20, 8, -8, -10]  # Hier kannst du die festen Winkel für jede Karte anpassen
    scale_factor = 0.3  # Verkleinern der kombinierten Bilder auf die Hälfte ihrer ursprünglichen Größe

    print(f"\nKarten für {hand_name}:")
    kartenbilder_mit_winkeln = [(pygame.transform.rotate(karte.bild, winkel), winkel) for karte, winkel in zip(hand, hand_winkel_list)]

# ... (Previous code)

def create_combined_image(images_with_angles, scale_factor):
    total_width = 0
    max_height = 0

    for image, _ in images_with_angles:
        total_width += int(image.get_width() * scale_factor)
        max_height = max(max_height, int(image.get_height() * scale_factor))

    combined_image = pygame.Surface((total_width, max_height), pygame.SRCALPHA)

    x_offset = 0
    for image, angle in images_with_angles:
        rotated_image = pygame.transform.rotozoom(image, angle, scale_factor)
        combined_image.blit(rotated_image, (x_offset, 0))
        x_offset += int(image.get_width() * scale_factor)

    return combined_image

# Create a combined image for each player's hand
for spieler_info in spieler:
    hand = spieler_info.hand
    hand_name = spieler_info.name
    hand_winkel_list = [20, 8, -8, -10]
    scale_factor = 0.3

    print(f"\nKarten für {hand_name}:")
    kartenbilder_mit_winkeln = [(pygame.transform.rotate(karte.bild, winkel), winkel) for karte, winkel in zip(hand, hand_winkel_list)]

    combined_image = create_combined_image(kartenbilder_mit_winkeln, scale_factor)
    spieler_info.kombiniertes_bild = combined_image  # Store the combined image in the SpielerInfo object

# Display the player hands and combined images
for spieler_info in spieler:
    print(f"\nSpieler: {spieler_info.name}")
    print("Karten:")
    for karte in spieler_info.hand:
        print(f" - {karte.name}")
    
    # Display the combined image for the player's hand
    combined_image = spieler_info.kombiniertes_bild
    x_pos = 0  # Starting position for the combined image
    y_pos = SCREEN_HEIGHT - combined_image.get_height()  # Position from the bottom of the screen
    screen.blit(combined_image, (x_pos, y_pos))
    x_pos += combined_image.get_width()  # Update the position for the next player

def make_transparent(image):
    if image.mode == 'RGBA':  # Überprüfe, ob das Bild bereits einen Alphakanal hat
        return image

    if image.mode == 'RGB':
        alpha = Image.new('L', image.size, 255)  # Erstelle einen neuen Alphakanal (vollständig undurchsichtig)
        image.putalpha(alpha)  # Füge den Alphakanal dem Bild hinzu

    return image

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Clear the screen
    screen.fill((255, 255, 255))

    # Display the player hands and combined images
    x_pos = 0  # Starting position for the combined image
    for spieler_info in spieler:
        combined_image = spieler_info.kombiniertes_bild
        y_pos = SCREEN_HEIGHT - combined_image.get_height()  # Position from the bottom of the screen
        screen.blit(combined_image, (x_pos, y_pos))
        x_pos += combined_image.get_width()  # Update the position for the next player

    # ... (Rest of the code for displaying player hands and combined images)
    
    pygame.display.flip()  # Update the display
    clock.tick(60)  # Limit frame rate to 60 FPS

# Quit pygame
pygame.quit()


