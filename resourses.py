class Emoji:
    _bookmark_tabs = u'\U0001f4d1'
    _memo = u'\U0001f4dd'
    _open_book = u'\U0001F4D6'
    _upwards_trend = u'\U0001f4c8'
    _leftwards_arrow = u'\U00002B05'
    _alien = u'\U0001F47E'
    _victory_hand = u'\U0000270C'
    _tea_cap = u'\U00002615'
    _finger_down = u'\U0001F447'

    learn = _open_book
    test = _memo
    topic = _bookmark_tabs
    statistics = _upwards_trend
    back = _leftwards_arrow
    alien = _alien
    hello = _victory_hand
    tea_cap = _tea_cap
    finger_down = _finger_down

class Status:
    idle = "idle"
    learning = "learning"
    testing = "testing"

    def get_status_types(self):
        temp = [self.idle, self.learning, self.testing]
        return temp

type_testing_words = {'current_index': 0, 'testing_data': []}
type_testing_words_data = {'ew': 'dummy', 'rw': 'заглушка', 'iactc': None}

if __name__ == "__main__":
    print("This is package file")
