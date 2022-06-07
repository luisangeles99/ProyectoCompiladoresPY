"""
....###....##.....##....###....####.##......
...##.##...##.....##...##.##....##..##......
..##...##..##.....##..##...##...##..##......
.##.....##.##.....##.##.....##..##..##......
.#########..##...##..#########..##..##......
.##.....##...##.##...##.....##..##..##......
.##.....##....###....##.....##.####.########

Clase de utilidad para conteo, tienen informacion
de un conteo y puede ser reiniciada o asignada 
utilizando sus metodos.
"""

class Avail:
    def __init__(self):
        self.t = 't'
        self.curr = 0
    
    def next(self):
        self.curr = self.curr + 1
        return self.t + str(self.curr)

    def reset(self):
        self.curr = 0