# Made by: Jacob Meadows
# Started on March 8th, 2018
"""
Main python file for my Service Learning Project Proposal
"""
import pygame
import ctypes
import string
colors = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255)
}


class ServiceLearningProjectProposal:
    def __init__(self):
        pygame.init()
        pygame.display.init()
        pygame.mixer.init()
        pygame.font.init()

        title = "Service Learning Project Proposal"
        user32 = ctypes.windll.user32
        monitor_size = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        screen = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
        pygame.display.set_caption(title)
        full_screen = True

        channel_1 = pygame.mixer.Channel(0)
        channel_2 = pygame.mixer.Channel(1)
        channels = [channel_1, channel_2]
        channel_sound = {channel_1: None,
                         channel_2: None}
        joyner_lucas___im_sorry = pygame.mixer.Sound("music\Joyner_Lucas_-_I'm_Sorry.wav")
        the_fray_x_ddlc___how_to_save_sayoris_life = pygame.mixer.Sound(
            "music\The_Fray_X_DDLC_-_How_to_Save_Sayori's_Life.wav")
        audio = Audio(channels, channel_sound)

        done = False
        pygame.key.set_repeat(500, 10)
        clock = pygame.time.Clock()
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000)

        tnr_30 = pygame.font.SysFont("Times New Roman", 30)
        intro_text = tnr_30.render(title, False, colors["green"])
        times_clicked = 0
        s_times_clicked = "000000000000000"
        text_objects = []

        typed_rect = pygame.Rect([100, 100], [1000, 100])
        special_input_rect = pygame.Rect([100, 199], [140, 55])

        typed_pos = typed_rect[0] + 10, typed_rect[1] + 10
        special_input_pos = special_input_rect[0] + 10, special_input_rect[1] + 5

        typed = Text(tnr_30, typed_pos, screen, typed_rect, "green")
        special_input = Text(tnr_30, special_input_pos, screen, special_input_rect, "green")

        text_objects += [typed]
        text_objects += [special_input]

        background_rect = [True, screen.get_rect()]
        selected_region = {
            f"{typed_rect}": [False, typed_rect, 1],
            f"{special_input_rect}": [False, special_input_rect, 2]
        }

        while not done:
            for event in pygame.event.get():
                current_position = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.USEREVENT + 1:
                    typed.selector()
                    special_input.selector()
                elif event.type == pygame.KEYDOWN:
                    pressed_key = pygame.key.name(event.key)
                    mods = pygame.key.get_mods()
                    if pressed_key == "escape":
                        if not mods & pygame.KMOD_LSHIFT:
                            if full_screen is True:
                                pygame.display.set_mode(monitor_size, pygame.RESIZABLE)
                                full_screen = False
                            elif full_screen is False:
                                done = True
                        elif mods & pygame.KMOD_LSHIFT:
                            if full_screen is False:
                                pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
                                full_screen = True
                    elif pressed_key == "tab":
                        if background_rect[0] is True:
                            background_rect[0] = False
                            for object_ in selected_region:
                                if selected_region[object_][2] == 1:
                                    selected_region[object_][0] = True
                        else:
                            for object_ in selected_region:
                                if selected_region[object_][0] is True:
                                    selected_region[object_][0] = False
                                    total_regions = len(selected_region.keys())
                                    for object__ in selected_region:
                                        if selected_region[object__][2] == selected_region[object_][2] + 1:
                                            selected_region[object__][0] = True
                                            break
                                        else:
                                            total_regions -= 1
                                    if total_regions == 0:
                                        background_rect[0] = True
                                    break
                    if background_rect[0] is True:
                        if pressed_key == "1":
                            audio.check_channel(mods, joyner_lucas___im_sorry)
                        elif pressed_key == "2":
                            audio.check_channel(mods, the_fray_x_ddlc___how_to_save_sayoris_life)
                    for object_ in text_objects:
                        if selected_region[f"{object_.rect}"][0] is True:
                            object_.check_typed(pressed_key, mods)
                elif event.type == pygame.KEYUP:
                    # pressed_key = pygame.key.name(event.key)
                    # mods = pygame.key.get_mods()
                    pass
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    times_clicked += 1
                    s_times_clicked = str(times_clicked)
                    if len(s_times_clicked) > 15:
                        times_clicked = times_clicked % 1000000000000000
                        s_times_clicked = str(times_clicked)
                    while len(s_times_clicked) != 15:
                        s_times_clicked = "0" + s_times_clicked

                    for object_ in selected_region:
                        if selected_region[object_][1].collidepoint(current_position[0], current_position[1]):
                            background_rect[0] = False
                            selected_region[object_][0] = True
                        elif not selected_region[object_][1].collidepoint(current_position[0], current_position[1]):
                            selected_region[object_][0] = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    pass  # Will most likely be used later.

            s_time = Time().s_time
            clicked_text = tnr_30.render("Clicks: %s" % s_times_clicked, False, colors["green"])
            current_time = tnr_30.render("Time: " + ":".join(reversed(s_time)),
                                         False, colors["green"])

            screen.fill(colors["black"])

            typed.rect_(typed_rect)
            special_input.rect_(special_input_rect)

            screen.blit(intro_text, [10, 5])
            screen.blit(current_time, [monitor_size[0] * 0.7875, monitor_size[1] * 0.955555556])
            if clicked_text is None:
                screen.blit(clicked_text, [monitor_size[0] * 0.7875, monitor_size[1] * 0.911111111])

            for object_ in text_objects:
                if selected_region[f"{object_.rect}"][0] is True:
                    object_.text_box(True)
                elif selected_region[f"{object_.rect}"][0] is False:
                    object_.text_box(False)

            pygame.display.flip()
            clock.tick(60)


class Time:
    def __init__(self):
        self.milliseconds = pygame.time.get_ticks()
        self.seconds = self.milliseconds // 1000
        self.minutes = self.seconds // 60
        self.hours = self.minutes // 60
        self.days = self.hours // 24
        self.weeks = self.days // 7
        self.months = self.weeks // 4
        self.years = self.months // 12

        self.s_milliseconds = str(self.milliseconds % 1000)
        self.s_seconds = str(self.seconds % 60)
        self.s_minutes = str(self.minutes % 60)
        self.s_hours = str(self.hours % 24)
        self.s_days = str(self.days % 7)
        self.s_weeks = str(self.weeks % 4)
        self.s_months = str(self.months % 12)
        self.s_years = str(self.years)

        while len(self.s_milliseconds) != 3:
            self.s_milliseconds = "0" + self.s_milliseconds
        while len(self.s_seconds) != 2:
            self.s_seconds = "0" + self.s_seconds
        while len(self.s_minutes) != 2:
            self.s_minutes = "0" + self.s_minutes
        while len(self.s_hours) != 2:
            self.s_hours = "0" + self.s_hours

        self.s_time = [self.s_milliseconds, self.s_seconds, self.s_minutes, self.s_hours,
                       self.s_days, self.s_weeks, self.s_months, self.s_years]


class Text:
    def __init__(self, font, pos, surface, rect, color):
        self.pos = pos
        self.font = font
        self.surface = surface
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.selector_state = False
        self.rect = pygame.draw.rect(self.surface, colors[color], rect, 1)
        self.key = None
        self.mods = None
        self.given_string = ""
        self.rendered_letter = ""
        self.letter_w = 0
        self.letter_h = 0
        self.key_values = {
            "`": "~",
            "1": "!",
            "2": "@",
            "3": "#",
            "4": "$",
            "5": "%",
            "6": "^",
            "7": "&",
            "8": "*",
            "9": "(",
            "0": ")",
            "-": "_",
            "=": "+",
            "[": "{",
            "]": "}",
            ";": ":",
            "'": '"',
            "\\": "|",
            ",": "<",
            ".": ">",
            "/": "?"
        }

    def check_typed(self, key, mods):
        self.key = key
        self.mods = mods
        if self.key in string.ascii_letters:
            if self.mods & pygame.KMOD_LSHIFT:
                self.key = self.key.upper()
            self.given_string += self.key
        elif self.key in self.key_values:
            if self.mods & pygame.KMOD_LSHIFT:
                self.key = self.key_values[self.key]
            self.given_string += self.key
        elif self.key == "space":
            self.given_string += " "
        elif self.key == "backspace":
            self.given_string = self.given_string[:-1]

    def rect_(self, typed_rect):
        self.rect = pygame.draw.rect(self.surface, colors["green"], typed_rect, 1)

    def text_box(self, selected):
        to_blit = {}
        self.x = self.pos[0]
        self.y = self.pos[1]

        for letter in range(len(self.given_string)):
            word = self.given_string[letter]
            extra_letter = letter - 1
            try:
                while self.given_string[extra_letter] != " ":
                    word = self.given_string[extra_letter] + word
                    extra_letter -= 1
            except IndexError:
                word = self.given_string[:letter + 1]

            self.rendered_letter = self.font.render(f"{self.given_string[letter]}", False, colors["green"])
            try:
                rendered_word = self.font.render(f"{word}", False, colors["green"])
            except pygame.error:
                rendered_word = self.font.render("TOO LARGE", False, colors["green"])

            self.letter_w, self.letter_h = self.rendered_letter.get_size()
            word_w, word_h = rendered_word.get_size()

            if self.x + self.letter_w <= self.rect[2] + self.pos[0] - 20:
                to_blit[self.rendered_letter] = [self.x, self.y], letter
                self.x += self.letter_w
            elif self.x + self.letter_w > self.rect[2] + self.pos[0] - 20:
                if word_w > self.rect[2] - 20:
                    self.y += self.letter_h
                    self.x = self.pos[0]
                    to_blit[self.rendered_letter] = [self.x, self.y], f"{extra_letter}:{letter}"
                    self.x += self.letter_w
                else:
                    to_delete = []
                    for k in range(extra_letter, letter):
                        for l in to_blit:
                            if to_blit[l][1] == k:
                                to_delete += [l]
                    for l in to_delete:
                        del to_blit[l]
                    self.y += word_h
                    self.x = self.pos[0]
                    to_blit[rendered_word] = [self.x, self.y], len(self.given_string)
                    self.x += word_w
            if self.y > self.rect[1] + self.rect[3] - 50:
                self.y -= self.letter_h
                for l in to_blit:
                    to_blit[l] = [to_blit[l][0][0], to_blit[l][0][1] - self.letter_h], to_blit[l][1]

        for l in to_blit:
            if self.rect[0] < to_blit[l][0][0] < self.rect[0] + self.rect[2] and \
                    self.rect[1] < to_blit[l][0][1] < self.rect[1] + self.rect[3]:
                self.surface.blit(l, to_blit[l][0])

        if selected is True:
            if self.selector_state is True:
                rendered_selector = self.font.render("|", False, colors["green"])
                self.surface.blit(rendered_selector, [self.x, self.y])

    def selector(self):
        if self.selector_state is False:
            self.selector_state = True
        elif self.selector_state is True:
            self.selector_state = False


class Audio:
    def __init__(self, channels, channels_dict):
        self.channels = channels
        self.channel_activity = channels_dict
        self.mods = None
        self.current_sound = None

    def check_channel(self, mods, sound):
        self.current_sound = sound
        for channel in self.channels:
            if not mods & pygame.KMOD_LSHIFT:
                if not channel.get_busy():
                    if self.current_sound not in self.channel_activity.values():
                        channel.play(self.current_sound)
                        self.channel_activity[channel] = self.current_sound
                        break
                elif channel.get_busy():
                    if self.channel_activity[channel] == self.current_sound:
                        channel.unpause()
            elif mods & pygame.KMOD_LSHIFT:
                if self.channel_activity[channel] == self.current_sound:
                    channel.pause()


if __name__ == "__main__":
    ServiceLearningProjectProposal()
