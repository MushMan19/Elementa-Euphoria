import textwrap
from src.constants import Constants
from src.services.visuals import Visuals
from src.tools.tools import generate_visible_colors

class Flashcard:
    def __init__(self, element_name, atomic_number, symbol, atomic_weight, type, property1, property2, property3):
        self.card = Visuals.get_flashcard_image()
        self.question_mark = Visuals.get_question_mark_image()
        self.element_name = element_name
        self.atomic_number = atomic_number
        self.atomic_weight = atomic_weight
        self.symbol = symbol
        self.type = type
        self.property1 = property1
        self.property2 = property2
        self.property3 = property3
        self.props = [self.property1, self.property2, self.property3]
        self.guessed = False
        self.x = Constants.SCREEN_WIDTH
        self.random_color, self.comp_random_color = generate_visible_colors()
        self.showing_answer = False
        # print(self.element_name)
        
    def display(self, screen):
        # screen.fill(Constants.PRIMARY)
        screen.blit(self.card, (self.x, (Constants.SCREEN_HEIGHT - self.card.get_height() + Constants.F_PAD_Y)))
        self.draw_properties(screen)
        if not self.showing_answer:
            screen.blit(self.question_mark, (self.x - ((self.question_mark.get_width() - self.card.get_width())/2) , 40))
        else:
            self.display_answer(screen)


    def update(self):
        # Update the x-coordinate for animation
        if self.x > Constants.SCREEN_WIDTH - (self.card.get_width() + Constants.F_PAD_X):
            self.x -= Constants.FLASHCARD_ANIM_SPEED 
        else:
            self.x = Constants.SCREEN_WIDTH - (self.card.get_width() + Constants.F_PAD_X)

    def display_answer(self, screen):
        # Determine the position for the centered text
        symbol_y = 78

        Visuals.draw_text(screen, Visuals.load_font_bold(Constants.SYMBOL_FONT_SIZE), self.symbol, None, self.random_color, ((self.x + self.card.get_width()/2), symbol_y), rect_pos="midtop")
        Visuals.draw_text(screen, Visuals.load_font(Constants.NAME_FONT_SIZE), self.element_name, None, self.random_color, ((self.x + self.card.get_width()/2), symbol_y + 100), rect_pos="midtop")
        Visuals.draw_text(screen, Visuals.load_font(Constants.ATOM_NUM_FONT_SIZE), str(self.atomic_number), None, self.comp_random_color, (self.x + 56, symbol_y - 25 + Constants.ATOM_NUM_FONT_SIZE/2), rect_pos="midleft")
        Visuals.draw_text(screen, Visuals.load_font(Constants.WEIGHT_FONT_SIZE), str(self.atomic_weight), None, self.comp_random_color, (self.x + Visuals.get_flashcard_image().get_width()- 56, symbol_y - 25 + Constants.WEIGHT_FONT_SIZE/2), rect_pos="midright")
        
        
    def draw_properties(self, screen):
        y_properties_heading = 230
        y_start = y_properties_heading + Constants.PROPERTY_PAD_Y
        font_descale = 14
        Visuals.draw_text(screen, Visuals.load_font_bold(Constants.PROPERTY_FONT_SIZE - font_descale), "Properties:", Constants.PROPERTY_FONT_SIZE, Constants.BLACK, (self.x + Constants.PROPERTY_PAD_X, y_properties_heading), rect_pos="topleft")
        count = 1
        for i, prop in enumerate(self.props,start=1):
            prop_y_space =  y_start + count * (Constants.PROPERTY_FONT_SIZE + 5)
            prop = f'{i}. {prop}'
            wrapped_text = textwrap.fill(prop, width=Constants.PROPERTY_FONT_SIZE)
            lines = wrapped_text.split('\n')
            count  += len(lines)
            y_offset = 0
            for j in lines:
                Visuals.draw_text(screen, Visuals.load_font(Constants.PROPERTY_FONT_SIZE - font_descale), j, None, Constants.BLACK, (self.x + Constants.PROPERTY_PAD_X, prop_y_space + y_offset), rect_pos='topleft')
                y_offset += Constants.PROPERTY_FONT_SIZE + 2