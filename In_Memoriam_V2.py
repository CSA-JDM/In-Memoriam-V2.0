# Made by: Jacob Meadows
# Started on March 8th, 2018
"""
Main python file for [PROJECT NAME].
"""
from FiLogic.Objects import *
import FiLogic.Variables as FiVar
import FiLogic.Multi_Dimensional_Arrays as MultiDimArray
import numpy
import pygame
import time


class App:
    def __init__(self):
        # Initialization
        pygame.init()
        pygame.display.init()
        pygame.mixer.init()
        # Predefined Information
        self.title = "Service Learning Project"
        self.screen = pygame.display.set_mode(FiVar.monitor_size, pygame.FULLSCREEN)
        pygame.display.set_caption(self.title)
        full_screen = True
        # Channels
        channel_1 = pygame.mixer.Channel(0)
        channel_2 = pygame.mixer.Channel(1)
        channel_3 = pygame.mixer.Channel(2)
        channels = [channel_1, channel_2, channel_3]
        channel_sound = {channel_1: None, channel_2: None, channel_3: None}
        # Sounds
        joyner_lucas___im_sorry = pygame.mixer.Sound("music\Joyner_Lucas_-_I'm_Sorry.wav")
        the_fray_x_ddlc___how_to_save_sayoris_life = pygame.mixer.Sound(
            "music\The_Fray_X_DDLC_-_How_to_Save_Sayori's_Life.wav")
        # Audio
        audio = Audio(channels, channel_sound)
        # Predefined Variables
        done = False
        pygame.key.set_repeat(500, 10)
        self.clock = pygame.time.Clock()
        pygame.time.set_timer(pygame.USEREVENT + 1, 1)
        pygame.time.set_timer(pygame.USEREVENT + 2, 1000)
        times_clicked = 0
        # Background
        background_rect = [True, self.screen.get_rect()]
        # Objects
        screen_objects = {}
        screen_objects.update(self.object_init())
        # 3D Map
        pv = MultiDimArray.ThreeDimensionalRenderer(self.screen)

        def map_object(name, _x, _y, _z):
            _object = MultiDimArray.ThreeDimensionalObject()
            _object.add_nodes(
                numpy.array([[x, y, z]
                             for x in range(*_x)
                             for y in range(*_y)
                             for z in range(*_z)])
            )
            _object.add_edges(
                [[n, n + 4] for n in range(0, 4)] +
                [[n, n + 1] for n in range(0, 8, 2)] +
                [[n, n + 2] for n in (0, 1, 4, 5)]
            )
            pv.update(name, _object)

        map_object("cube", [500, 1001, 500], [200, 701, 500], [0, 501, 500])
        # Main Loop
        while not done:
            for event in pygame.event.get():
                current_position = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    pass  # Will probably add a save function here.
                    done = True
                # Millisecond update
                elif event.type == pygame.USEREVENT + 1:
                    s_time, d_time = Time().s_time
                    screen_objects["time_text"][0].update_text = \
                        f"  {d_time[3]}:{d_time[4]}:{d_time[5]}\n{d_time[0]}/{d_time[1]}/{d_time[2]}"
                    screen_objects["session_text"][0].update_text = f"Session Time: {':'.join(reversed(s_time))}"
                    screen_objects["fps_text"][0].update_text = str(round(self.clock.get_fps()))
                    for object_ in screen_objects:
                        if isinstance(screen_objects[object_][0], Button):
                            screen_objects[object_][0].motion_command(current_position)
                # 1000 milliseconds update
                elif event.type == pygame.USEREVENT + 2:
                    for object_ in screen_objects:
                        if isinstance(screen_objects[object_][0], TextInput):
                            screen_objects[object_][0].selector()
                elif event.type == pygame.KEYDOWN:
                    pressed_key = pygame.key.name(event.key)
                    mods = pygame.key.get_mods()
                    if pressed_key == "escape":
                        if not mods & pygame.KMOD_LSHIFT:
                            if full_screen is True:
                                pygame.display.set_mode(FiVar.monitor_size, pygame.RESIZABLE)
                                full_screen = False
                            elif full_screen is False:
                                done = True
                        elif mods & pygame.KMOD_LSHIFT:
                            if full_screen is False:
                                pygame.display.set_mode(FiVar.monitor_size, pygame.FULLSCREEN)
                                full_screen = True
                    elif pressed_key == "tab":
                        if not mods & pygame.KMOD_LSHIFT:
                            if background_rect[0]:
                                background_rect[0] = False
                                highest = [None, FiVar.monitor_size[0], FiVar.monitor_size[1]]
                                for object_ in screen_objects:
                                    if isinstance(screen_objects[object_][0], TextInput) or \
                                            isinstance(screen_objects[object_][0], Button):
                                        if highest[2] > screen_objects[object_][0].rect[1]:
                                            highest = [screen_objects[object_], screen_objects[object_][0].rect[0],
                                                       screen_objects[object_][0].rect[1]]
                                        elif highest[2] == screen_objects[object_][0].rect[1]:
                                            if highest[1] > screen_objects[object_][0].rect[0]:
                                                highest = [screen_objects[object_], screen_objects[object_][0].rect[0],
                                                           screen_objects[object_][0].rect[1]]
                                highest[0][1] = True
                            else:
                                for object_ in screen_objects:
                                    if screen_objects[object_][1]:
                                        screen_objects[object_][1] = False
                                        for object__ in screen_objects:
                                            if isinstance(screen_objects[object__][0], TextInput) or \
                                                    isinstance(screen_objects[object__][0], Button):
                                                if screen_objects[object__][0].rect[1] > \
                                                        screen_objects[object_][0].rect[1]:
                                                    screen_objects[object__][1] = True
                                                    background_rect[0] = False
                                                    break
                                            background_rect[0] = True
                                        break
                        if mods & pygame.KMOD_LSHIFT:
                            if background_rect[0]:
                                background_rect[0] = False
                                lowest = [None, 0, 0]
                                for object_ in screen_objects:
                                    if isinstance(screen_objects[object_][0], TextInput) or \
                                            isinstance(screen_objects[object_][0], Button):
                                        if lowest[2] < screen_objects[object_][0].rect[1]:
                                            lowest = [screen_objects[object_], screen_objects[object_][0].rect[0],
                                                      screen_objects[object_][0].rect[1]]
                                        elif lowest[2] == screen_objects[object_][0].rect[1]:
                                            if lowest[1] < screen_objects[object_][0].rect[0]:
                                                lowest = [screen_objects[object_], screen_objects[object_][0].rect[0],
                                                          screen_objects[object_][0].rect[1]]
                                lowest[0][1] = True
                            else:
                                for object_ in screen_objects:
                                    if screen_objects[object_][1]:
                                        screen_objects[object_][1] = False
                                        for object__ in screen_objects:
                                            if isinstance(screen_objects[object__][0], TextInput) or \
                                                    isinstance(screen_objects[object__][0], Button):
                                                if screen_objects[object__][0].rect[1] < \
                                                        screen_objects[object_][0].rect[1]:
                                                    screen_objects[object__][1] = True
                                                    background_rect[0] = False
                                                    break
                                            background_rect[0] = True
                                        break
                    elif pressed_key == "1":
                        if background_rect[0]:
                            audio.check_channel(mods, joyner_lucas___im_sorry)
                    elif pressed_key == "2":
                        if background_rect[0]:
                            audio.check_channel(mods, the_fray_x_ddlc___how_to_save_sayoris_life)
                    # Input for Text Inputs
                    for object_ in screen_objects:
                        if isinstance(screen_objects[object_][0], TextInput):
                            if screen_objects[object_][1]:
                                screen_objects[object_][0].check_typed(pressed_key, mods)
                elif event.type == pygame.KEYUP:
                    # pressed_key = pygame.key.name(event.key)
                    # mods = pygame.key.get_mods()
                    pass
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pressed_button = event.button
                    clicked_buttons = pygame.mouse.get_pressed()
                    if pressed_button not in (4, 5):
                        if clicked_buttons[0] or clicked_buttons[1] or clicked_buttons[2]:
                            times_clicked += 1
                            s_times_clicked = str(times_clicked)
                            if len(s_times_clicked) > 15:
                                times_clicked = times_clicked % 1000000000000000
                                s_times_clicked = str(times_clicked)
                            while len(s_times_clicked) != 15:
                                s_times_clicked = "0" + s_times_clicked
                            screen_objects["clicked_text"][0].update_text = f"Clicks: {s_times_clicked}"
                            for object_ in screen_objects:
                                if isinstance(screen_objects[object_][0], TextInput) or \
                                        isinstance(screen_objects[object_][0], Button):
                                    if screen_objects[object_][0].rect.collidepoint(current_position[0],
                                                                                    current_position[1]):
                                        background_rect[0] = False
                                        screen_objects[object_][1] = True
                                        if isinstance(screen_objects[object_][0], Button):
                                            screen_objects[object_][0].pressed_command()
                                        break
                                    elif not screen_objects[object_][0].rect.collidepoint(current_position[0],
                                                                                          current_position[1]):
                                        screen_objects[object_][1] = False
                                        background_rect[0] = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    for object_ in screen_objects:
                        if isinstance(screen_objects[object_][0], Button):
                            if screen_objects[object_][1]:
                                screen_objects[object_][1] = False
                                background_rect[0] = True
                if background_rect[0]:
                    pv.check(event)

            self.screen.fill(FiVar.colors["black"])

            pv.update()
            for object_ in screen_objects:
                if isinstance(screen_objects[object_][0], TextBox) or isinstance(screen_objects[object_][0], Button):
                    if isinstance(screen_objects[object_][0], Button) and screen_objects[object_][1]:
                        screen_objects[object_][0].highlight(pygame.mouse.get_pos(), state=True)
                    screen_objects[object_][0].update()
                elif isinstance(screen_objects[object_][0], TextInput):
                    if screen_objects[object_][1]:
                        screen_objects[object_][0].text_box(True)
                    elif not screen_objects[object_][1]:
                        screen_objects[object_][0].text_box(False)

            pygame.display.flip()
            self.clock.tick(300)

    def object_init(self):
        # Title
        title_text = TextBox(FiVar.tnr_30, self.screen, [10, 5], text=self.title,
                             color=FiVar.colors["green"])
        # FPS
        fps_text = TextBox(FiVar.tnr_30, self.screen, [1545, 5], text=str(round(self.clock.get_fps())),
                           color=FiVar.colors["green"])
        # Time
        s_time, d_time = Time().s_time
        time_text = TextBox(FiVar.tnr_30, self.screen, [1440, 810], ([1430, 800], [160, 90]),
                            FiVar.colors["green"],
                            f"  {d_time[3]}:{d_time[4]}:{d_time[5]}\n{d_time[0]}/{d_time[1]}/{d_time[2]}")
        session_text = TextBox(FiVar.tnr_20, self.screen, [1130, 850], color=FiVar.colors["green"],
                               text=f"Session Time: {':'.join(reversed(s_time))}")
        # Click Counter
        clicked_text = TextBox(FiVar.tnr_20, self.screen, [1180, 810], color=FiVar.colors["green"],
                               text=f"Clicks: 000000000000000")
        # New Game
        new_game_button = Button(FiVar.tnr_30, self.screen, [20, 55], [[10, 45], [160, 60]],
                                 color=FiVar.colors["green"], text="New Game",
                                 pressed_command=lambda: [],
                                 motion_command=lambda event_: new_game_button.highlight(event_))
        # User Input
        search_input = TextInput(FiVar.tnr_30, self.screen, pos=[80, 840], rect=pygame.Rect([70, 830], [1000, 55]),
                                 color=FiVar.colors["green"])
        return {
            "title_text": [title_text, False],
            "fps_text": [fps_text, False],
            "time_text": [time_text, False],
            "session_text": [session_text, False],
            "clicked_text": [clicked_text, False],
            "new_game_button": [new_game_button, False],
            "search_input": [search_input, False]
        }

    def save(self):
        pass


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

        local_time = list(time.localtime())
        if len(str(local_time[1])) < 2:
            local_time[1] = "0" + str(local_time[1])
        if len(str(local_time[2])) < 2:
            local_time[2] = "0" + str(local_time[2])
        if len(str(local_time[3])) < 2:
            local_time[3] = "0" + str(local_time[3])
        if len(str(local_time[4])) < 2:
            local_time[4] = "0" + str(local_time[4])
        if len(str(local_time[5])) < 2:
            local_time[5] = "0" + str(local_time[5])

        self.s_time = [[self.s_milliseconds, self.s_seconds, self.s_minutes, self.s_hours,
                       self.s_days, self.s_weeks, self.s_months, self.s_years], local_time]


class Audio:
    def __init__(self, channels, channels_dict):
        self.channels = channels
        self.channel_activity = channels_dict
        self.current_sound = None

    def check_channel(self, mods, sound):
        self.current_sound = sound
        for channel in self.channels:
            if not mods & pygame.KMOD_LSHIFT:
                if not channel.get_busy():
                    if self.current_sound not in self.channel_activity.values() or \
                            self.channel_activity[channel] == self.current_sound:
                        channel.play(self.current_sound)
                        self.channel_activity[channel] = self.current_sound
                elif channel.get_busy():
                    if self.channel_activity[channel] == self.current_sound:
                        channel.unpause()
            elif mods & pygame.KMOD_LSHIFT:
                if self.channel_activity[channel] == self.current_sound:
                    channel.pause()


if __name__ == "__main__":
    App()
