import hashlib


def generate_hash_rect_sec(*args):
    """
    Generates a unique hash value for a combination of parameters.
    """
    # Concatenate all arguments into a single string
    combined_string = "".join(str(arg) for arg in args)

    # Generate hash value for the combined string
    hash_value = hashlib.sha256(combined_string.encode()).hexdigest()

    return hash_value


def resizable_table(data: list[list[str]]) -> str:
    """
    Generate resizable HTML table code from a list of lists.

    Parameters:
        data (list of lists): A list of lists containing the data to be displayed in the table.
                              The first list should contain column headers, and subsequent lists
                              should contain row data.

    Returns:
        str: HTML code for the resizable table.
    """
    table_code = "<div style='overflow-x:auto;'>"
    table_code += "<table style='width:100%; border-collapse: collapse;'>"

    for row in data:
        table_code += "<tr>"
        for cell in row:
            table_code += (
                f"<td style='border: 1px solid black; padding: 8px;'>{cell}</td>"
            )
        table_code += "</tr>"

    table_code += "</table></div>"
    return table_code
