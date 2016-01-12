
class LF_Generator:

    def __init__(self, ast):
        self.ast = ast
        self.output = []

    def generate(self):
        return 0

    def save(self, file):
        with open(file, 'w') as f:
            f.writelines("".join(self.output))
