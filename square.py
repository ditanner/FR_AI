class Square():

    def __init__(self, position):
        self.left_token = '  '
        self.right_token = '  '
        self.position = position

    def print_left_token(self):
        print(self.left_token, end='')

    def print_right_token(self):
        print(self.right_token, end='')

    def print_position(self):
        print(self.position, end='')
