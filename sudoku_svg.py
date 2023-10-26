import sys
from string import Template as StringTemplate

class SudokuSVG:
    '''
        template_path - path to .svg template
        insert_template - string template for svg element. see example below
        cord_lambda - lambda to compute coordinates. should return array of 2 numbers (x and y)
    '''
    def __init__(self, template_path, insert_template, cord_lambda):
        self.template_path = template_path
        self.insert_template = insert_template
        self.cord_lambda = cord_lambda

    def _parse_puzzle(self, puzzle):
        res = []

        for i in range(0, len(puzzle)):
            c = puzzle[i]
            if (c in "123456789"):
                pos = self.cord_lambda(i%9, i//9)
                res.append(self.insert_template.substitute(x=pos[0], y=pos[1], n=int(c)))

        return res

    '''
        path - path to output .svg file
        puzzle - sudoku puzzle. Supported separators: pretty much all
    '''
    def generate(self, path, puzzle):
        if (len(puzzle) != 9*9): print("Can't handle this puzzle! Exiting"); return

        with open(self.template_path, "r") as file:
            lines = file.readlines()

        new_lines = []
        for line in lines:
            new_lines.append(line)
            if "<!-- insert_numbers_here -->" in line:
                new_lines += self._parse_puzzle(puzzle)

        with open(path, 'w') as file:
            file.writelines(new_lines)

        
if __name__ == "__main__":
    svg = SudokuSVG("template.svg", 
                    StringTemplate('\t\t<tspan x="$x" y="$y">$n</tspan>\n'), 
                    lambda x, y: [50 + x * 100, 80 + y * 100])

    puzzle = "6.7...8.42.........83....1........8..1..3......4567....2...1......7.84.5...64...."
    if (len(sys.argv) == 2):
        puzzle = sys.argv[1]

    svg.generate("output.svg", puzzle)
