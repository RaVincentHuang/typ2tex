import subprocess
import re
import eel

def tex_cache_write(input_string):
    """
    Write the input string to a temporary .tex file.

    Args:
        input_string (str): The string to be written to the file.

    Returns:
        None
    """
    file_path = ".pandoc/temp.tex"
    with open(file_path, "w") as file:
        file.write(input_string)
 
def tex_cache_read():
    """
    Read the contents of the temporary TeX cache file.

    Returns:
        str: The contents of the temporary TeX cache file.
    """
    filename = ".pandoc/temp.tex"
    with open(filename, "r") as file:
        return file.read()
    
def typ_cache_write(input_string):
    """
    Write the input string to a temporary file for caching.

    Args:
        input_string (str): The string to be written to the file.

    Returns:
        None
    """
    file_path = ".pandoc/temp.typ"
    with open(file_path, "w") as file:
        file.write(input_string)
 
def typ_cache_read():
    """
    Reads the contents of the temporary .typ file and returns it as a string.

    Returns:
        str: The contents of the .typ file.
    """
    filename = ".pandoc/temp.typ"
    with open(filename, "r") as file:
        return file.read()
    
import subprocess

def typ2tex_call():
    """
    Converts a .typ file to a .tex file using pandoc.

    This function runs the pandoc command to convert a .typ file to a .tex file.
    It uses the subprocess module to execute the command.

    Raises:
        SystemExit: If the subprocess command returns a non-zero exit code.

    """
    try:
        subprocess.run(["pandoc", "-f", "typst", "-t", "latex", ".pandoc/temp.typ", "-o", ".pandoc/temp.tex"])
    except subprocess.CalledProcessError as e:
        raise SystemExit(e.returncode)
    
    
import subprocess

def tex2typ_call():
    """
    Converts a LaTeX file to a .typ file using pandoc.

    This function runs the pandoc command to convert a LaTeX file to a .typ file.
    It expects the LaTeX file to be located at '.pandoc/temp.tex' and saves the
    converted .typ file at '.pandoc/temp.typ'.

    Raises:
        SystemExit: If the pandoc command fails with a non-zero return code.

    """
    try:
        subprocess.run(["pandoc", "-f", "latex", "-t", "typst", ".pandoc/temp.tex", "-o", ".pandoc/temp.typ"])
    except subprocess.CalledProcessError as e:
        raise SystemExit(e.returncode)

def tex2typ(tex):
    """
    Convert LaTeX code to typ code.

    Args:
        tex (str): The LaTeX code to be converted.

    Returns:
        str: The converted typ code.

    Raises:
        SystemExit: If an error occurs during the conversion process.
    """
    tex = r"\begin{align}" + tex + r"\end{align}"
    tex_cache_write(tex)
    try:
        tex2typ_call()
    except subprocess.CalledProcessError as e:
        raise SystemExit(e.returncode)
    typ = typ_cache_read()
    typ = typ.strip("$ ").rstrip(" $\n")
    return typ

def typ2tex(typ):
    """
    Convert a mathematical expression in typographical format to LaTeX format.

    Args:
        typ (str): The mathematical expression in typographical format.

    Returns:
        str: The mathematical expression converted to LaTeX format.
    """
    typ = r"$ " + typ + r" $"
    typ_cache_write(typ)
    try:
        typ2tex_call()
    except subprocess.CalledProcessError as e:
        raise SystemExit(e.returncode)
    tex = tex_cache_read()
    tex = re.sub(r'^\\\[|\\\]$', '', tex, count=2)
    tex = re.sub(r'^\\begin{aligned}\n|\n\\end{aligned}\n$', '', tex, count=2)
    return tex
