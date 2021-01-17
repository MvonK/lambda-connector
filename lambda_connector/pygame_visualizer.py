import pathlib

bot_image_file = pathlib.Path(__file__).parent.absolute() / "bot.png"
bot2_image_file = pathlib.Path(__file__).parent.absolute() / "bot2.png"


class PygameVisualization:
    def __init__(self):
        try:
            import pygame
        except:
            print("Pygame not installed. Do 'pip install pygame' to make the local visualizator work, "
                  "or use the web one")
        self.win = pygame.display.set_mode((900, 600))
        self.bot_image = pygame.image.load(str(bot_image_file))
        self.bot_image2 = pygame.image.load(str(bot2_image_file))

    def print_state(self, state):
        import pygame
        self.win.fill((255, 255, 255))
        for e in pygame.event.get():
            pass
        botimg = self.bot_image
        for player in state["bots"]:
            for bot in state["bots"][player]:
                center = botimg.get_rect().center
                xdif, ydif = center
                rotated = pygame.transform.rotate(botimg, -bot["current_angle"])
                new_rect = rotated.get_rect(center=center)
                self.win.blit(rotated, (new_rect.topleft[0] + bot["x"] - xdif, new_rect.topleft[1] + bot["y"] - ydif))
            botimg = self.bot_image2 if botimg is self.bot_image else self.bot_image
        pygame.display.update()

    def quit(self):
        import pygame
        pygame.display.quit()