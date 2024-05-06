# pdf-citation-highlighter

### Running The Application

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. The application can be run with the following command:

```bash
python server.py
```

### API Endpoint

The API endpoint is a GET endpoint that requires three parameters:

- `url`: The URL of the PDF to be displayed
- `page`: The page number to be scanned
- `search`: The search string to be scanned on the specified page and highlighted

#### Example Usage

To use the API endpoint, send a GET request to the `/` endpoint with the required parameters. For example:

```bash
GET /?url=https://example.com/pdf.pdf&page=6&search=keyword#page=6
```

This will scan page 6 of the PDF at **https://example.com/pdf.pdf** for the search string keyword and highlight the results.

#### Opening a Specific Page

Note that we need to also specify `#page=6` at the end of the URL to open the PDF on the specified page.
