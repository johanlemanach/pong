import pygame
import random
from menu import show_menu
# Constantes pour la largeur et la hauteur de la fenêtre
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720

# Valeurs RGB pour les couleurs utilisées dans le jeu
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

# Vitesse de déplacement des raquettes
PADDLE_SPEED = 0.3  # Redéfinition de la vitesse de la raquette

# ==============================================================================
# |                   Fonction pour obtenir le nom du joueur                   |
# ==============================================================================
# Cette fonction permet de demander au joueur d'entrer son nom avant de jouer
def get_player_name(prompt, screen, font, clock, color):
    input_box = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2, 400, 50) # Position et taille de la zone de saisie
    color_inactive = pygame.Color('lightskyblue3') # Couleur de la zone de saisie
    color_active = pygame.Color('dodgerblue2') # Couleur de la zone de saisie lorsqu'elle est active
    color_box = color_inactive # Couleur de la zone de saisie
    active = False # Pour savoir si la zone de saisie est active
    text = '' # Texte saisi par le joueur
    done = False # Pour savoir si le joueur a terminé de saisir son nom
 
    while not done:
        for event in pygame.event.get(): # Parcourir tous les événements
            if event.type == pygame.QUIT: # Si l'événement est de quitter, quitter le jeu
                pygame.quit() # Quitter Pygame
                return None # Retourner None
            if event.type == pygame.KEYDOWN: # Si l'événement est une touche enfoncée
                if event.key == pygame.K_RETURN: # Si la touche enfoncée est Entrée
                    done = True # Terminer la saisie
                elif event.key == pygame.K_BACKSPACE: # Si la touche enfoncée est Retour Arrière
                    text = text[:-1] # Supprimer le dernier caractère
                else: # Sinon
                    text += event.unicode # Ajouter le caractère saisi au texte
            if event.type == pygame.MOUSEBUTTONDOWN: # Si l'événement est un clic de souris
                if input_box.collidepoint(event.pos): # Si le clic est dans la zone de saisie
                    active = not active # Activer ou désactiver la zone de saisie
                else:
                    active = False # Désactiver la zone de saisie
                color_box = color_active if active else color_inactive # Changer la couleur de la zone de saisie

        screen.fill(COLOR_BLACK) # Remplir l'écran en noir
        txt_surface = font.render(text, True, color) # Rendre le texte saisi
        width = max(200, txt_surface.get_width() + 10) # Largeur de la zone de saisie
        input_box.w = width # Ajuster la largeur de la zone de saisie
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5)) # Afficher le texte saisi
        pygame.draw.rect(screen, color_box, input_box, 2) # Dessiner la zone de saisie

        # Rendre le prompt
        prompt_surface = font.render(prompt, True, color) # Rendre le prompt
        screen.blit(prompt_surface, (input_box.x, input_box.y - 30)) # Afficher le prompt

        pygame.display.flip() # Mettre à jour l'affichage
        clock.tick(30) # Limiter le nombre de frames par seconde

    return text # Retourner le texte saisi
# ==============================================================================
# |     Fonction pour initialiser la balle avec une vitesse modifiable         |
# ==============================================================================
# Cette fonction initialise la balle avec une vitesse aléatoire
def initialize_ball():
    ball_rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 25, 25) # Position et taille de la balle
    ball_speed_factor = 0.05  # Ajustement de la vitesse de la balle
    ball_accel_x = random.choice([-1, 1]) * random.randint(2, 3) * ball_speed_factor  # Ajustement de la vitesse initiale
    ball_accel_y = random.choice([-1, 1]) * random.randint(2, 3) * ball_speed_factor # Ajustement de la vitesse initiale
    return ball_rect, ball_accel_x, ball_accel_y # Retourner la balle et sa vitesse
def main():
    # CONFIGURATION DU JEU

    # Initialiser la bibliothèque PyGame (absolument nécessaire)
    pygame.init()

    # Créer la fenêtre pour le jeu
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Définir le titre de la fenêtre
    pygame.display.set_caption("Pong")

    # Font pour le texte
    font = pygame.font.SysFont('Consolas', 30)

    # Créer l'objet clock pour suivre le temps
    clock = pygame.time.Clock()

    # Afficher le menu
    show_menu(screen)



    # Saisie des prénoms des joueurs
    player_1_name = get_player_name("Enter Player 1 Name:", screen, font, clock, COLOR_WHITE)
    if player_1_name is None:
        return
    player_2_name = get_player_name("Enter Player 2 Name:", screen, font, clock, COLOR_WHITE)
    if player_2_name is None:
        return

    # Les raquettes des joueurs
    paddle_1_rect = pygame.Rect(30, SCREEN_HEIGHT // 2 - 50, 7, 100)
    paddle_2_rect = pygame.Rect(SCREEN_WIDTH - 37, SCREEN_HEIGHT // 2 - 50, 7, 100)

    # Suivre le mouvement des raquettes par frame
    paddle_1_move = 0
    paddle_2_move = 0

    # Initialiser la balle
    ball_rect, ball_accel_x, ball_accel_y = initialize_ball()

    # Ceci est pour vérifier si la balle doit bouger
    started = False

    # Scores des joueurs
    score_1 = 0
    score_2 = 0
# ==============================================================================
# |                             BOUCLE DU JEU                                  |
# ==============================================================================
    # Boucle principale du jeu
    while True:
        # Définir la couleur de fond en noir
        screen.fill(COLOR_BLACK)

        for event in pygame.event.get(): # Parcourir tous les événements
            if event.type == pygame.QUIT: # Si l'événement est de quitter
                pygame.quit() # Quitter Pygame
                return # Quitter la fonction

            if event.type == pygame.KEYDOWN: # Si l'événement est une touche enfoncée
                if event.key == pygame.K_SPACE: # Si la touche enfoncée est Espace
                    started = True # Commencer le jeu
 
                # JOUEUR 1
                if event.key == pygame.K_w: # Si la touche enfoncée est W
                    paddle_1_move = -PADDLE_SPEED # Déplacer la raquette vers le haut
                if event.key == pygame.K_s: # Si la touche enfoncée est S
                    paddle_1_move = PADDLE_SPEED # Déplacer la raquette vers le bas

                # JOUEUR 2
                if event.key == pygame.K_UP: # Si la touche enfoncée est Flèche Haut
                    paddle_2_move = -PADDLE_SPEED # Déplacer la raquette vers le haut
                if event.key == pygame.K_DOWN: # Si la touche enfoncée est Flèche Bas
                    paddle_2_move = PADDLE_SPEED # Déplacer la raquette vers le bas

            if event.type == pygame.KEYUP: # Si l'événement est une touche relâchée
                if event.key == pygame.K_w or event.key == pygame.K_s: # Si la touche relâchée est W ou S
                    paddle_1_move = 0.0 # Arrêter le mouvement de la raquette
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN: # Si la touche relâchée est Flèche Haut ou Bas
                    paddle_2_move = 0.0 # Arrêter le mouvement de la raquette

        # Faire bouger la balle après 3 secondes
        if not started:
            text = font.render('Press Space to Start', True, COLOR_WHITE) # Afficher le texte
            text_rect = text.get_rect() # Obtenir le rectangle du texte
            text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2) # Centrer le texte
            screen.blit(text, text_rect) # Afficher le texte
        else:
            # Si la balle sort des limites, ajouter un point au joueur adverse et réinitialiser la balle
            if ball_rect.left <= 0: # Si la balle sort à gauche
                score_2 += 1 # Ajouter un point au joueur 2
                ball_rect, ball_accel_x, ball_accel_y = initialize_ball() # Réinitialiser la balle
                started = False # Arrêter le jeu

            if ball_rect.right >= SCREEN_WIDTH: # Si la balle sort à droite
                score_1 += 1 # Ajouter un point au joueur 1
                ball_rect, ball_accel_x, ball_accel_y = initialize_ball() # Réinitialiser la balle
                started = False     # Arrêter le jeu

            # Si la balle se rapproche du haut
            if ball_rect.top <= 0:  # Si la balle touche le haut
                ball_accel_y *= -1 # Inverser la direction de la balle
                ball_rect.top = 0 # Faire en sorte que la balle reste à l'intérieur de l'écran

            # Faire de même avec le bas
            if ball_rect.bottom >= SCREEN_HEIGHT: # Si la balle touche le bas
                ball_accel_y *= -1 # Inverser la direction de la balle
                ball_rect.bottom = SCREEN_HEIGHT # Faire en sorte que la balle reste à l'intérieur de l'écran

            # Gérer les collisions avec les raquettes
            if paddle_1_rect.colliderect(ball_rect) and ball_accel_x < 0: # Si la balle touche la raquette 1
                ball_accel_x *= -1 # Inverser la direction de la balle
                ball_rect.left = paddle_1_rect.right # Faire en sorte que la balle reste à l'intérieur de la raquette

            if paddle_2_rect.colliderect(ball_rect) and ball_accel_x > 0:
                ball_accel_x *= -1
                ball_rect.right = paddle_2_rect.left

            # Déplacer la balle
            ball_rect.x += ball_accel_x * 60 # Déplacer la balle horizontalement
            ball_rect.y += ball_accel_y * 60 # Déplacer la balle verticalement

        # Déplacer les raquettes
        paddle_1_rect.y += paddle_1_move * 60 # Déplacer la raquette 1
        paddle_2_rect.y += paddle_2_move * 60 # Déplacer la raquette 2

        # Empêcher les raquettes de sortir des limites
        if paddle_1_rect.top < 0: # Si la raquette 1 touche le haut
            paddle_1_rect.top = 0 # Faire en sorte que la raquette reste à l'intérieur de l'écran
        if paddle_1_rect.bottom > SCREEN_HEIGHT: # Si la raquette 1 touche le bas
            paddle_1_rect.bottom = SCREEN_HEIGHT # Faire en sorte que la raquette reste à l'intérieur de l'écran

        if paddle_2_rect.top < 0:
            paddle_2_rect.top = 0
        if paddle_2_rect.bottom > SCREEN_HEIGHT:
            paddle_2_rect.bottom = SCREEN_HEIGHT

        # Dessiner les raquettes des joueurs et la balle
        pygame.draw.rect(screen, COLOR_WHITE, paddle_1_rect) # Dessiner la raquette 1
        pygame.draw.rect(screen, COLOR_WHITE, paddle_2_rect) # Dessiner la raquette 2
        pygame.draw.circle(screen, COLOR_WHITE, ball_rect.center, ball_rect.width // 2)  # Dessiner la balle


        # Afficher les scores
        score_text = font.render(f"{player_1_name}: {score_1} - {player_2_name}: {score_2}", True, COLOR_WHITE) # Afficher le score
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 50)) # Centrer le score
        screen.blit(score_text, score_rect) # Afficher le score

        # Mettre à jour l'affichage
        pygame.display.update()

        # Obtenir le temps écoulé entre maintenant et la dernière frame
        clock.tick(60)

if __name__ == '__main__':
    main()
