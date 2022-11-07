from dim_checker.errors import ConstraintDimError, ConstraintTypeError


class Constraints:

    def __init__(self, constraints: dict) -> None:
        """Initialize constraints.

        Args:
            constraints (dict): dimensions constraints.
        """
        self.variables = self.parse_constraints(constraints)

    def parse_constraints(self, constraints: dict) -> dict:
        """Parse the constraints and check there validity.

        Args:
            constraints (dict): dictionary of constraints on 
            dimensions.

        Raises:
            ConstraintDimError: error raised when the constant dimension format 
            is not respected.
            ConstraintTypeError: error raised when the constant value type is not 
            correct.

        Returns:
            dict: valid constraints.
        """
        # check dimension constraints validity
        for dim in constraints.keys():
            value = constraints[dim]
            if len(dim) > 1 or (not dim.isalpha()):
                raise ConstraintDimError(dim) 
            
            if not isinstance(value, int) :
                raise ConstraintTypeError(dim, value)

        return constraints

