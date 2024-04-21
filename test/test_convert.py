import unittest
from convert import tex2typ, typ2tex

class ConvertTests(unittest.TestCase):
    """
    A test case class for testing the conversion functions in the typ2tex module.
    """

    def test_tex2typ_conversion(self):
        """
        Test the conversion from TeX to typ.

        This method tests the `tex2typ` function by providing a TeX input and comparing the output with the expected typ output.
        It asserts that the converted typ output matches the expected typ output.

        Args:
            self: The test case instance.

        Returns:
            None
        """
        tex_input = r"\begin{align}x + y = z\end{align}"
        expected_typ_output = "x + y = z"
        typ_output = tex2typ(tex_input)
        self.assertEqual(typ_output, expected_typ_output)

    def test_typ2tex_conversion(self):
        """
        Test the conversion of a typ input to TeX output using the typ2tex function.

        This test case verifies that the typ2tex function correctly converts a typ input string
        to the expected TeX output string.

        The typ input is set to "x + y = z", and the expected TeX output is set to
        r"\begin{align}x + y = z\end{align}".

        The typ2tex function is called with the typ_input, and the resulting TeX output is
        compared to the expected_tex_output using the self.assertEqual method.

        If the conversion is successful, the test case passes. Otherwise, it fails.
        """
        typ_input = "x + y = z"
        expected_tex_output = r"\begin{align}x + y = z\end{align}"
        tex_output = typ2tex(typ_input)
        self.assertEqual(tex_output, expected_tex_output)

if __name__ == "__main__":
    unittest.main()