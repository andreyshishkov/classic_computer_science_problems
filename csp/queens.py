from csp import Constraint, CSP
from typing import Dict, List, Optional


class QueenConstraint(Constraint[int, int]):

    def __init__(self, columns: List[int]) -> None:
        super().__init__(columns)
        self.columns: List[int] = columns

    def satisfied(self, assignment: Dict[int, int]) -> bool:
        for q1c, q1r in assignment.items():
            for q2c in range(q1c + 1, len(self.columns) + 1):
                if q2c in assignment:
                    q2r: int = assignment[q2c]
                    if q1r == q2r:
                        return False
                    if abs(q1r - q2r) == abs(q1c - q2c):
                        return False
        return True


if __name__ == '__main__':
    columns: List[int] = [x for x in range(1, 9)]
    rows: Dict[int, List[int]] = {}
    for column in columns:
        rows[column] = [x for x in range(1, 9)]
    csp: CSP[int, int] = CSP(columns, rows)

    csp.add_constraint(QueenConstraint(columns))
    solution: Optional[Dict[int, int]] = csp.backtracking_search()
    if solution is None:
        print("No solution found!")
    else:
        print(solution)