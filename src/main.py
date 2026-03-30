from src.gui.game import init_game

def print_solution(node):
    path = []
    current = node
    while current:
        path.append(current.state)
        current = current.parent

    for state in reversed(path):
        print(state)

#def calc_time

def main():
    init_game()

if __name__ == "__main__":
    main()