import os
from mcp.server.fastmcp import FastMCP
from pypdf import PdfReader

# Create an MCP server
mcp = FastMCP("PDF Document Server")

# Helper function to extract text from a PDF
def extract_text_from_pdf(file_path):
    if not os.path.exists(file_path):
        return f"Error: File {file_path} not found."
    
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

# Define resources for the documents
@mcp.resource("file:///DEVI_TRABALHO.pdf")
def devi_trabalho_resource() -> str:
    """Returns the full text of DEVI_TRABALHO.pdf"""
    return extract_text_from_pdf("DEVI_TRABALHO.pdf")

@mcp.resource("file:///Trabalho_Final.pdf")
def trabalho_final_resource() -> str:
    """Returns the full text of Trabalho Final.pdf"""
    # Using underscore for URI but file might have space
    return extract_text_from_pdf("Trabalho Final.pdf")

# Define a tool to search through the documents
@mcp.tool()
def search_documents(query: str) -> str:
    """
    Search for a keyword or phrase in all available PDF documents.
    Returns snippets of text where the query was found.
    """
    files = ["DEVI_TRABALHO.pdf", "Trabalho Final.pdf"]
    results = []
    
    for file_name in files:
        if not os.path.exists(file_name):
            continue
            
        try:
            reader = PdfReader(file_name)
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if query.lower() in text.lower():
                    # Find a snippet around the query
                    index = text.lower().find(query.lower())
                    start = max(0, index - 50)
                    end = min(len(text), index + len(query) + 50)
                    snippet = text[start:end].replace("\n", " ")
                    results.append(f"[{file_name} - Page {i+1}]: ...{snippet}...")
        except Exception as e:
            results.append(f"Error reading {file_name}: {str(e)}")
            
    if not results:
        return f"No matches found for '{query}'."
    
    return "\n".join(results)

if __name__ == "__main__":
    mcp.run()
