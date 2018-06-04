# Made by: Jacob Meadows
# Started on March 8th, 2018
"""
Object logic file for [PROJECT NAME].
"""
import FiLogic.Variables as FiVar
import pygame
import string


class ScreenObject:
    def __init__(self, pos, font, surface, color, rect=None, width=1):
        self.pos = pos
        self.font = font
        self.surface = surface
        self.color = color
        self.orig_color = color
        self.given_rect = rect
        self.width = width
        self.x = self.pos[0]
        self.y = self.pos[1]
        if self.given_rect is not None:
            self.rect = pygame.draw.rect(self.surface, self.color, self.given_rect, 0)
            self.rect = pygame.draw.rect(self.surface, self.color, self.given_rect, self.width)

    def update(self):
        self.rect = pygame.draw.rect(self.surface, FiVar.colors["black"], self.given_rect, 0)
        self.rect = pygame.draw.rect(self.surface, self.orig_color, self.given_rect, self.width)
        if self.width == 0:
            self.rect = pygame.draw.rect(self.surface, self.color, self.given_rect, 2)


class TextInput(ScreenObject):
    def __init__(self, font, surface, pos=(0, 0), rect=pygame.Rect([0, 0], [0, 0]),
                 color=FiVar.colors["white"]):
        super().__init__(pos, font, surface, color, rect)
        self.selector_state = False
        self.key = None
        self.key_memory = {}
        self.mods = None
        self.given_string = ""
        self.string_pos = 0
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

    def text_box(self, selected):
        # Remaking text input logic; used to lag after a certain amount of inputs.
        self.rect = pygame.draw.rect(self.surface, FiVar.colors["black"], self.given_rect, 0)
        self.rect = pygame.draw.rect(self.surface, FiVar.colors["green"], self.given_rect, 1)
        old_y = self.y
        try:
            self.rendered_letter = self.font.render(f"{self.given_string[self.string_pos]}", True,
                                                    FiVar.colors["green"])
            self.letter_w, self.letter_h = self.rendered_letter.get_size()

            word = self.given_string[self.string_pos]
            extra_letter = self.string_pos - 1
            try:
                while self.given_string[extra_letter] != " " and extra_letter >= 0:
                    word = self.given_string[extra_letter] + word
                    extra_letter -= 1
                extra_letter += 1
            except IndexError:
                word = self.given_string[:self.string_pos + 1]
            try:
                rendered_word = self.font.render(f"{word}", True, FiVar.colors["green"])
            except pygame.error:
                rendered_word = self.font.render("TOO LARGE", True, FiVar.colors["green"])
                self.key_memory = {}
                self.given_string = "TOO LARGE"
                self.rendered_letter = self.font.render("T", True, FiVar.colors["green"])
                self.letter_w, self.letter_h = self.rendered_letter.get_size()
                self.x, self.y = self.pos[0], self.pos[1]
                self.string_pos = 0
            word_w, word_h = rendered_word.get_size()

            if self.x + self.letter_w <= self.rect[2] + self.pos[0] - 20:
                if self.given_string[self.string_pos] in self.key_memory:
                    self.key_memory[self.given_string[self.string_pos]] += [[[self.x, self.y], self.rendered_letter,
                                                                             self.string_pos]]
                else:
                    self.key_memory[self.given_string[self.string_pos]] = [[[self.x, self.y], self.rendered_letter,
                                                                            self.string_pos]]
                self.x += self.letter_w
                self.string_pos += 1
            elif self.x + self.letter_w > self.rect[2] + self.pos[0] - 20:
                if word_w > self.rect[2] - 320:
                    self.y += self.letter_h
                    self.x = self.pos[0]
                    if self.given_string[self.string_pos] in self.key_memory:
                        self.key_memory[self.given_string[self.string_pos]] += [[[self.x, self.y], self.rendered_letter,
                                                                                 self.string_pos]]
                    else:
                        self.key_memory[self.given_string[self.string_pos]] = [[[self.x, self.y], self.rendered_letter,
                                                                                self.string_pos]]
                    self.x += self.letter_w
                    self.string_pos += 1
                elif self.x + word_w > self.rect[2] + self.pos[0] - 20:
                    to_delete = []
                    for k in range(extra_letter, self.string_pos + 1):
                        for key in self.key_memory:
                            for letter in range(len(self.key_memory[key])):
                                if self.key_memory[key][letter][2] == k:
                                    to_delete += [[key, letter]]
                    to_delete = reversed(to_delete)
                    for l in to_delete:
                        del self.key_memory[l[0]][l[1]]
                        self.string_pos -= 1
                    self.y += word_h
                    self.x = self.pos[0]
                    for letter in word:
                        self.rendered_letter = self.font.render(f"{letter}", True, FiVar.colors["green"])
                        self.letter_w, self.letter_h = self.rendered_letter.get_size()
                        if letter in self.key_memory:
                            self.key_memory[letter] += [[[self.x, self.y], self.rendered_letter, self.string_pos]]
                        else:
                            self.key_memory[letter] = [[[self.x, self.y], self.rendered_letter, self.string_pos]]
                        self.x += self.letter_w
                        self.string_pos += 1
        except IndexError:
            if self.string_pos > len(self.given_string):
                to_delete = []
                for key in self.key_memory:
                    for letter in range(len(self.key_memory[key])):
                        if self.key_memory[key][letter][2] == self.string_pos - 1:
                            to_delete += [[key, letter]]
                            self.x, self.y = self.key_memory[key][letter][0]
                for l in to_delete:
                    del self.key_memory[l[0]][l[1]]
                    self.string_pos -= 1

        if self.y < old_y:
            for key_ in self.key_memory:
                for letter_ in range(len(self.key_memory[key_])):
                    if self.key_memory[key_][letter_][0][1] < self.rect[1]:
                        self.y += self.letter_h
                        for key in self.key_memory:
                            for letter in range(len(self.key_memory[key])):
                                self.key_memory[key][letter] = [[self.key_memory[key][letter][0][0],
                                                                self.key_memory[key][letter][0][1] + self.letter_h],
                                                                self.key_memory[key][letter][1],
                                                                self.key_memory[key][letter][2]]
                        break

        if self.y > self.rect[1] + self.rect[3] - 20:
            self.y -= self.letter_h
            for key in self.key_memory:
                for letter in range(len(self.key_memory[key])):
                    self.key_memory[key][letter] = [[self.key_memory[key][letter][0][0],
                                                    self.key_memory[key][letter][0][1] - self.letter_h],
                                                    self.key_memory[key][letter][1],
                                                    self.key_memory[key][letter][2]]

        for key in self.key_memory:
            for letter in range(len(self.key_memory[key])):
                if self.rect[0] < self.key_memory[key][letter][0][0] < self.rect[0] + self.rect[2] and \
                        self.rect[1] < self.key_memory[key][letter][0][1] < self.rect[1] + self.rect[3] - 20:
                    self.surface.blit(self.key_memory[key][letter][1], self.key_memory[key][letter][0])

        """
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
        """

        if selected:
            if self.selector_state:
                rendered_selector = self.font.render("|", True, FiVar.colors["green"])
                self.surface.blit(rendered_selector, [self.x, self.y-2])

    def selector(self):
        if not self.selector_state:
            self.selector_state = True
        elif self.selector_state:
            self.selector_state = False


class TextBox(ScreenObject):
    def __init__(self, font, surface, pos=(0, 0), rect=pygame.Rect([0, 0], [0, 0]), color="white", text="", width=1):
        super().__init__(pos, font, surface, color, rect, width)
        text = text.split("\n")
        self.text = []
        self.update_text = ""
        if isinstance(text, list):
            for t in text:
                self.text += [self.font.render(t, True, color)]
        else:
            self.text = [self.font.render(text, True, color)]

    def update(self):
        self.x, self.y = self.pos[0], self.pos[1]
        super().update()
        if isinstance(self.update_text, str) and self.update_text != "":
            self.update_text = self.update_text.split("\n")
            if isinstance(self.update_text, list):
                self.text = []
                for t in self.update_text:
                    self.text += [self.font.render(t, True, self.color)]
            else:
                self.text = [self.font.render(self.update_text, True, self.color)]
        for t in self.text:
            self.surface.blit(t, [self.x, self.y])
            self.y += t.get_size()[1]


class Button(ScreenObject):
    def __init__(self, font, surface, pos=(0, 0), rect=pygame.Rect([0, 0], [0, 0]), color="white", text="",
                 pressed_command=None, motion_command=None, width=1):
        super().__init__(pos, font, surface, color, rect, width)
        self.orig_width = width
        self.text_str = text
        text = text.split("\n")
        self.text = []
        self.update_text = ""
        if isinstance(text, list):
            for t in text:
                self.text += [self.font.render(t, True, color)]
        else:
            self.text = [self.font.render(text, True, color)]
        self.pressed_command = pressed_command
        self.motion_command = motion_command

    def update(self):
        self.x, self.y = self.pos[0], self.pos[1]
        super().update()
        self.text = [self.font.render(self.text_str, True, self.color)]
        if isinstance(self.update_text, str) and self.update_text != "":
            self.update_text = self.update_text.split("\n")
            if isinstance(self.update_text, list):
                self.text = []
                for t in self.update_text:
                    self.text += [self.font.render(t, True, self.color)]
            else:
                self.text = [self.font.render(self.update_text, True, self.color)]
        for t in self.text:
            self.surface.blit(t, [self.x, self.y])
            self.y += t.get_size()[1]

    def highlight(self, current_position, state=False):
        if self.rect.collidepoint(current_position[0], current_position[1]) or state:
            self.color = FiVar.colors["black"]
            self.width = 0
        elif not self.rect.collidepoint(current_position[0], current_position[1]):
            self.color = self.orig_color
            self.width = self.orig_width
