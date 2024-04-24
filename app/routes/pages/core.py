from flask import Blueprint, request, make_response, render_template, current_app
import fitz
import requests
import mysql.connector
from urllib.parse import urlparse
from datetime import datetime, timedelta

core_bp = Blueprint("core", __name__, url_prefix="/")

def hex_to_rgb(hex_color: str):
    return tuple((int(hex_color.lstrip('#')[i:i+2], 16)/255) for i in (0, 2, 4))

def is_url_allowed(url):
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user=current_app.config["MYSQL_USER"],
            password=current_app.config["MYSQL_PASSWORD"],
            database=current_app.config["MYSQL_DBNAME"]
        )

        mycursor = mydb.cursor()

        mycursor.execute("SELECT File FROM mw_cargo__PDFCite")
        result = mycursor.fetchall()

        for row in result:
            if url == row[0]:
                mydb.close()
                return True

        mydb.close()
        return False

    except Exception as e:
        print("Error connecting to database:", e)
        return False
        
@core_bp.route('/')
def home_route():
    url = request.args.get('url')
    search_string = request.args.get('search')
    highlight = request.args.get('color')

    page_number = int(request.args.get('page', '1')) - 1

    file_name = urlparse(url).path.split('/')[-1]

    if not url or not search_string:
        return render_template("error/500.html")
        
    if not is_url_allowed(url):
        return render_template("error/403.html")

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
                annotation = page.add_highlight_annot(rects)

                if highlight:
                     annotation.set_colors(stroke=hex_to_rgb( "#" + highlight))
                else:
                     default_highlight_color = current_app.config["HIGHLIGHT_COLOR"]
                     annotation.set_colors(stroke=hex_to_rgb(default_highlight_color))

                annotation.update()

        data = doc.tobytes(compression_effort=1)

    except Exception as e:
        return render_template("error/500.html")
    
    finally:
        if doc:
            doc.close()

    response = make_response(data)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename="{file_name}"'
    
    expiry_time = datetime.now() + timedelta(hours=1)
    response.headers['Cache-Control'] = 'public, max-age=3600'
    response.headers['Expires'] = expiry_time.strftime('%a, %d %b %Y %H:%M:%S GMT')
    
    return response
