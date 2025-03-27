from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
import os
import io
from mammoth import extract_raw_text
from db_config import get_db_connection
import logging
from datetime import date

router = APIRouter()

@router.get("/openfile/", response_class=HTMLResponse)
async def get_document(final_doc_id: str, file: str, name:str):
    try:
        # Fetch file data from the database
        file_data = get_file_data_from_database(final_doc_id)
        if not file_data or not file_data.get("final_doc_url"):
            raise HTTPException(status_code=404, detail="File not found in the database")
        today = date.today()
        formatted_date = today.isoformat()
        print(formatted_date)
        
        if file.endswith(".docx"):
            folder_type = "doc"
        elif file.endswith(".txt"):
            folder_type = "text"
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type. Only .docx and .txt are allowed.")
        
        # Construct the full file path
        folder_path = os.path.join(os.getcwd(), "output", name, formatted_date, final_doc_id, folder_type)
        file_path = os.path.join(folder_path, file)
        print(os.path.exists(file_path))

        # Check if the file exists
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")

        # Read the file content
        with open(file_path, "rb") as f:
            file_buffer = f.read()

        # Process the file based on its type
        if file.endswith(".docx"):
            # Handle .docx files using Mammoth
            file_stream = io.BytesIO(file_buffer)
            result = extract_raw_text(file_stream)
            text = result.value
        elif file.endswith(".txt"):
            try:
                # Attempt to decode as UTF-8 first
                text = file_buffer.decode("utf-8")
            except UnicodeDecodeError:
                try:
                    # Fallback to decoding as ISO-8859-1 (Latin-1)
                    text = file_buffer.decode("iso-8859-1")
                except UnicodeDecodeError as e:
                    logging.error(f"Error decoding text file: {e}")
                    raise HTTPException(
                        status_code=500,
                        detail="Text file encoding not supported. Please ensure the file uses UTF-8 or a common encoding."
                    )
                    
        else:
            # Unsupported file type
            raise HTTPException(status_code=400, detail="Unsupported file type. Only .docx and .txt are allowed.")

        # Format the extracted or read text into HTML
        html_content = generate_html(format_text(text))

        # Return the HTML response
        return HTMLResponse(content=html_content, status_code=200)

    except HTTPException as e:
        raise e
    except Exception as e:
        logging.error(f"Error processing document: {e}")
        raise HTTPException(status_code=500, detail="Server error")


def get_file_data_from_database(final_doc_id: str):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT final_doc_url FROM final_document WHERE row_doc_id = %s"
        cursor.execute(query, (final_doc_id,))
        result = cursor.fetchone()
        conn.close()
        return result
    
    except Exception as e:
        logging.error(f"Database error: {e}")
        return None


def format_text(text):
    return "\n".join(
        f"<p>{line.strip()}</p>"
        for line in text.strip().split("\n") if line.strip()
    )


def generate_html(content):
    """
    Generate an HTML page to display the document content.
    """
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Document Viewer</title>
      <style>
        body {{
          font-family: Arial, sans-serif;
          line-height: 1.6;
          margin: 2rem auto;
          max-width: 800px;
          padding: 1rem;
          background-color: #f9f9f9;
          color: #333;
        }}
        p {{
          margin-bottom: 1.5rem;
        }}
      </style>
    </head>
    <body>
      <h1>Document Content</h1>
      {content}
    </body>
    </html>
    """