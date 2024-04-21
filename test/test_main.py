import unittest
from main import TranslatorWindow

class TranslatorWindowTests(unittest.TestCase):
    """
    Unit tests for the TranslatorWindow class.
    """

    def setUp(self):
        """
        Set up the test environment before each test case.

        This method is called before each individual test case is run. It initializes the `window` attribute with an instance of the `TranslatorWindow` class.

        Parameters:
            self (TestCase): The current test case instance.

        Returns:
            None
        """
        self.window = TranslatorWindow()

    def test_translate_text_same_language(self):
        """
        Test case to verify the translation of text when the source and target languages are the same.

        Steps:
        1. Set the source language combobox to "LaTeX".
        2. Set the target language combobox to "LaTeX".
        3. Set the input textbox with the text "This is a test".
        4. Call the translate_text method.
        5. Get the text from the output textbox.
        6. Assert that the output text is equal to the input text.
        """
        self.window.source_language_combobox.setCurrentText("LaTeX")
        self.window.target_language_combobox.setCurrentText("LaTeX")
        self.window.input_textbox.setPlainText("This is a test")
        self.window.translate_text()
        output_text = self.window.output_textbox.toPlainText()
        self.assertEqual(output_text, "This is a test")

    def test_translate_text_latex_to_typst(self):
        """
        Test case to verify the translation from LaTeX to Typst.

        This test sets the source language to LaTeX, target language to Typst,
        and input text to "\\alpha + \\beta = \\gamma". It then calls the
        `translate_text` method of the window object and checks if the output
        text matches the expected result "α + β = γ".
        """
        self.window.source_language_combobox.setCurrentText("LaTeX")
        self.window.target_language_combobox.setCurrentText("Typst")
        self.window.input_textbox.setPlainText("\\alpha + \\beta = \\gamma")
        self.window.translate_text()
        output_text = self.window.output_textbox.toPlainText()
        self.assertEqual(output_text, "α + β = γ")

    def test_translate_text_typst_to_latex(self):
        """
        Test case for translating text from Typst to LaTeX.

        Sets the source language to Typst, target language to LaTeX,
        and input text to "alpha + beta = gamma". Then, it calls the
        `translate_text` method of the window object. Finally, it
        asserts that the output text in the output_textbox is equal
        to "\\alpha + \\beta = \\gamma".
        """
        self.window.source_language_combobox.setCurrentText("Typst")
        self.window.target_language_combobox.setCurrentText("LaTeX")
        self.window.input_textbox.setPlainText("alpha + beta = gamma")
        self.window.translate_text()
        output_text = self.window.output_textbox.toPlainText()
        self.assertEqual(output_text, "\\alpha + \\beta = \\gamma")

    def test_translate_text_invalid_language(self):
        """
        Test case to check the translation of text when an invalid language is selected.

        Steps:
        1. Set the source language to "Invalid".
        2. Set the target language to "LaTeX".
        3. Set the input text to "This is a test".
        4. Call the translate_text method.
        5. Get the output text from the output_textbox.
        6. Assert that the output text is "Error!".

        This test case ensures that an error message is displayed when an invalid language is selected for translation.
        """
        self.window.source_language_combobox.setCurrentText("Invalid")
        self.window.target_language_combobox.setCurrentText("LaTeX")
        self.window.input_textbox.setPlainText("This is a test")
        self.window.translate_text()
        output_text = self.window.output_textbox.toPlainText()
        self.assertEqual(output_text, "Error!")

    def test_clean_text(self):
        """
        Test case to verify the behavior of the clean_text method.

        It sets the text in the output_textbox to "This is some output",
        calls the clean_text method, and then checks if the text in the
        output_textbox is empty.

        """
        self.window.output_textbox.setPlainText("This is some output")
        self.window.clean_text()
        output_text = self.window.output_textbox.toPlainText()
        self.assertEqual(output_text, "")

if __name__ == "__main__":
    unittest.main()