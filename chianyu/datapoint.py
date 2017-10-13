#-*- coding: utf-8 -*-

class sentence:

    def __init__(self, Id, Text, Category=None):
        self.Id = Id
        self.Text = Text
        self.Category = Category

        self.labels = {
            '0': 'Slovak',
            '1': 'French',
            '2': 'Spanish',
            '3': 'German',
            '4': 'Polish',
        }

        self.Neighbors = {}

    def __repr__(self):
        return 'ID: %s\nText: %s\nCategory: %s\nNeighbors: %s' % (
            self.Id,
            self.Text,
            self.labels.get(self.Category, self.Category),
            self.Neighbors,
        )

def main():
    print('hello world')

if __name__ == '__main__':
    main()
