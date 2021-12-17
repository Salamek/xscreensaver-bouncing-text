import random
import signal
import datetime
import os
import sys

# Disable stupid pygame message on import
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame


class BouncingText(pygame.sprite.Sprite):

    def __init__(self, text: str,  font, color):
        super(BouncingText, self).__init__()
        self.rect = pygame.Rect((1, 1), (1, 1))
        self.font = font
        self.color = color
        self.text = text

        self.update_image()

    def update_image(self):
        height = self.font.get_height()
        # Put the rendered text surfaces into this list.

        text_to_drawn = datetime.datetime.now().strftime(self.text).splitlines()

        text_surfaces = []
        for txt in text_to_drawn:
            text_surfaces.append(self.font.render(txt, True, self.color))
        # The width of the widest surface.
        width = max(txt_surf.get_width() for txt_surf in text_surfaces)

        # A transparent surface onto which we blit the text surfaces.
        self.image = pygame.Surface((width, height*len(text_to_drawn)), pygame.SRCALPHA)
        for y, txt_surf in enumerate(text_surfaces):
            text_x = (width - txt_surf.get_width()) / 2
            text_y = y*height
            self.image.blit(txt_surf, (text_x, text_y))
        # Get a new rect (if you maybe want to make the text clickable).
        self.rect = self.image.get_rect(topleft=self.rect.topleft)


class Screensaver:
    def __init__(self,
                 text: str,
                 full_screen: bool = False,
                 show_fps: bool = False,
                 text_color: str = '#4285F4',
                 background_color: str = '#000000',
                 speed: int = 1,
                 fps: int = 60
                 ):
        self.text = text
        self.show_fps = show_fps
        self.background_color = pygame.Color(background_color)
        self.text_color = pygame.Color(text_color)
        self.speed = speed
        self.fps = fps
        signal.signal(signal.SIGTERM, self.handle_term)

        window_id = os.environ.get('XSCREENSAVER_WINDOW')
        if window_id:
            os.environ['SDL_WINDOWID'] = window_id

        pygame.init()
        pygame.display.set_caption('Bouncing text screensaver')
        pygame.mouse.set_visible(False)

        info_object = pygame.display.Info()
        self.clock = pygame.time.Clock()
        self.width = info_object.current_w
        self.height = info_object.current_h
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) if full_screen else pygame.display.set_mode((self.width, self.height))

        self.fps_font = pygame.font.Font(None, 40)

    def handle_term(self, signal=None, frame=None):
        pygame.quit()
        sys.exit(0)

    def update_fps(self):
        fps = 'FPS: {}'.format(int(self.clock.get_fps()))
        fps_text = self.fps_font.render(fps, True, pygame.Color("coral"))
        return fps_text

    def run(self):
        # Font size is 10% of height of the screen
        font_size = int(self.height if self.height < self.width else self.width * 0.1)
        has_strftime = '%' in self.text

        bouncing_text = BouncingText(
            self.text,
            pygame.font.Font(None, font_size),
            self.text_color
        )
        all_sprites = pygame.sprite.Group(bouncing_text)

        if self.width > bouncing_text.rect.width:
            position_x = random.randint(bouncing_text.rect.width, self.width)
        elif self.width < bouncing_text.rect.width:
            position_x = random.randint(self.width, bouncing_text.rect.width)
        else:
            position_x = 0

        if self.height > bouncing_text.rect.height:
            position_y = random.randint(bouncing_text.rect.height, self.height)
        elif self.height < bouncing_text.rect.height:
            position_y = random.randint(self.height, bouncing_text.rect.height)
        else:
            position_y = 0

        position = [position_x, position_y]
        #position = [random.randint(bouncing_text.rect.width, self.width), random.randint(bouncing_text.rect.height, self.height)]
        velocity = [self.speed, self.speed]

        #time_event = pygame.USEREVENT + 1
        #pygame.time.set_timer(time_event, 1000)

        while True:

            # Events
            #update_image = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.handle_term()
                #elif event.type == time_event:
                #    update_image = True

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

            # Render
            position[0] += velocity[0]
            position[1] += velocity[1]
            if position[0] > self.width or position[0] < bouncing_text.rect.width:
                velocity[0] = -velocity[0]

            if position[1] > self.height or position[1] < bouncing_text.rect.height:
                velocity[1] = -velocity[1]

            new_pos_x = position[0] - bouncing_text.rect.width
            new_pos_y = position[1] - bouncing_text.rect.height

            bouncing_text.rect.x = new_pos_x
            bouncing_text.rect.y = new_pos_y
            # Update image if string contains % that ~means a strftime needs to be used
            if has_strftime:
                bouncing_text.update_image()
            self.screen.fill(self.background_color)
            if self.show_fps:
                self.screen.blit(self.update_fps(), (10, 0))
            all_sprites.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(self.fps)
