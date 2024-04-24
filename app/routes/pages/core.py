from flask import Blueprint, request, make_response, render_template
import fitz
import requests
from urllib.parse import urlparse

core_bp = Blueprint("core", __name__, url_prefix="/")

@core_bp.route('/')
def home_route():
    url = request.args.get('url')
    search_string = request.args.get('search')


    page_number = int(request.args.get('page', '1')) - 1

    file_name = urlparse(url).path.split('/')[-1]

    if not url or not search_string:
        return render_template("error/500.html")

    data = None
    doc = None
    try:
        response = requests.get(url)
        data = response.content

        doc = fitz.open(stream=data)

        if page_number >= 0 and page_number < doc.page_count:
            page = doc[page_number]
            rects = page.search_for(search_string)

            if rects:
                page.add_highlight_annot(rects)

        data = doc.tobytes(compression_effort=1)

    except Exception as e:
        return render_template("error/500.html")
    
    finally:
        if doc:
            doc.close()

    response = make_response(data)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename="{file_name}"'

    return response
