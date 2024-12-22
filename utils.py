from bs4 import BeautifulSoup

def parse_html_file(file_path: str) -> str:
    """
    Reads and parses the text content of a local HTML file.

    Args:
        file_path (str): Path to the local HTML file.

    Returns:
        str: Extracted plain text content from the HTML file.
    """
    try:
        # Open and read the HTML file
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Create a BeautifulSoup object
        soup = BeautifulSoup(html_content, 'html.parser')

        # Remove script, style, and meta elements
        for element in soup(['script', 'style', 'meta', 'noscript', 'link']):
            element.decompose()

        # Extract and return the plain text
        plain_text = soup.get_text(separator="\n", strip=True)
        return plain_text

    except Exception as e:
        return f"An error occurred: {e}"