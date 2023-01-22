def amet(name: str)->str:
    """Give a name

    Args:
        name (str): a name

    Returns:
        str: my name is name
    """
    output: str = f"My name is {name}."
    return output


class MyCalss:
    """This is my class"""
    def __init__(self, alpha: float = 0.5) -> None:
        """take alpha

        Args:
            alpha (float, optional): store alpha in self. Defaults to 0.5.
        """
        self.alpha: float = alpha
    def double_alpha(self) -> float:
        """double alpha

        Returns:
            float: double alpha
        """
        return 2 * self.alpha