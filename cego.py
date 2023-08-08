import random
import os
import pygame
from pygame.locals import *
from PIL import Image

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

# Klasse für eine Karte definieren
class Karte:
    def __init__(self, name, bild, wert):
        self.name = name
        self.bild = bild
        self.wert = wert

class SpielerInfo:
    def __init__(self, name, hand, kombiniertes_bild=None):
        self.name = name
        self.hand = hand
        self.kombiniertes_bild = kombiniertes_bild


def zeige_spielerkarten(spieler_info):
    spieler_name = spieler_info.name
    spieler_hand = spieler_info.hand
    spieler_kombiniertes_bild = spieler_info.kombiniertes_bild


def create_combined_image(cards, winkel_list, scale=1.0):
    card_width = cards[0].bild.width
    card_height = cards[0].bild.height
    overlap = int(card_width * 0.3 * scale)  # Überlappungsabstand (30% der Kartenbreite)
    combined_width = int(card_width * len(cards) - (len(cards) - 1) * overlap * scale)  # Anpassung der Breite
    combined_height = int(card_height * scale)  # Anpassung der Höhe
    combined_image = Image.new("RGBA", (combined_width, combined_height))  # Transparenter Hintergrund

    pos_x = 0  # Initialisiere die X-Position

    for i, (card, winkel) in enumerate(zip(cards, winkel_list)):
        # Rotiere das Bild im festen Winkel um den Ankerpunkt und skaliere es
        rotated_card = card.bild.rotate(winkel, resample=Image.BICUBIC, expand=True).resize(
            (int(card_width * scale), int(card_height * scale)), Image.LANCZOS
        )

        # Berechne die Position des Bildes im kombinierten Bild
        pos_y = combined_height - int(rotated_card.height * scale)  # Am unteren Rand zentrieren

        # Kombiniere das rotierte und skalierte Bild mit dem kombinierten Bild unter Beibehaltung des Alphakanals
        combined_image.alpha_composite(rotated_card, (pos_x, pos_y))

        # Aktualisiere die X-Position für die nächste Karte unter Berücksichtigung der Überlappung
        pos_x += int(card_width * scale) - overlap

    return combined_image

# 1. Überprüfung der Benutzereingabe für die Anzahl der Spieler in der Lobby
anzahl_spieler = int(input("Geben Sie die Anzahl der Spieler ein (maximal 7): "))
if anzahl_spieler < 1 or anzahl_spieler > 7:
    print("Ungültige Anzahl der Spieler!")
    exit()

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
    bild = Image.open(os.path.join(karten_ordner, datei)).convert("RGBA")
    name = datei.split(".")[0]
    wert = karten_werte.get(name, 0)  # Wenn der Karte kein Wert zugewiesen wurde, wird 0 als Standardwert verwendet.
    karten.append(Karte(name, bild, wert))

# 5. Karten mischen
random.shuffle(karten)

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
    kartenbilder_mit_winkeln = [(karte.bild.rotate(winkel), winkel) for karte, winkel in zip(hand, hand_winkel_list)]

    combined_image = create_combined_image(hand, hand_winkel_list, scale_factor)
    spieler_info.kombiniertes_bild = combined_image


    spieler_canvas = Canvas(spieler_fenster)
    spieler_canvas.pack()

    verschiebbare_bilder = []
    x_position = 10
    for kartenbild, winkel in kartenbilder_mit_winkeln:
        scaled_image = kartenbild.resize((int(kartenbild.width * scale_factor), int(kartenbild.height * scale_factor)), Image.LANCZOS)
        tk_image = ImageTk.PhotoImage(scaled_image)
        bild = VerschiebbaresBild(spieler_canvas, tk_image, x_position, 10)
        verschiebbare_bilder.append(bild)
        x_position += scaled_image.width + 10  # Abstand zwischen den Bildern

def make_transparent(image):
    if image.mode == 'RGBA':  # Überprüfe, ob das Bild bereits einen Alphakanal hat
        return image

    if image.mode == 'RGB':
        alpha = Image.new('L', image.size, 255)  # Erstelle einen neuen Alphakanal (vollständig undurchsichtig)
        image.putalpha(alpha)  # Füge den Alphakanal dem Bild hinzu

    return image

# 10. Zeige die GUI für jeden Spieler an
for spieler_info in spieler:
    zeige_spielerkarten(spieler_info)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Clear the screen
    screen.fill((255, 255, 255))

    # ... (Rest of the code for displaying player hands and combined images)
    
    pygame.display.flip()  # Update the display
    clock.tick(60)  # Limit frame rate to 60 FPS

# Quit pygame
pygame.quit()


