# pdf-citation-highlighter
### Description
**A Python application that highlights the provided citation on a given page of a PDF file.** 

The highlight color and port are configurable. The default highlight color can be overridden by the URL parameter.

The application is intended to run on MediaWiki sites. It provides a MediaWiki template for building PDF citation links. It uses a Cargo table with the allowed PDF URLs to prevent exploits.

### Requirements
* Nginx
* Python
  * pipx
  * Flask
  * Flask-Cors
  * python-dotenv
  * PyMuPDF
  * gunicorn
  * requests
* MediaWiki
  * [Extension:Cargo](https://www.mediawiki.org/wiki/Extension:Cargo)
  * [Extension:PageExchange](https://www.mediawiki.org/wiki/Extension:Page_Exchange)
  * [Extension:Widgets](https://www.mediawiki.org/wiki/Extension:Widgets)

### Installation
#### Clone the repository
Navigate to the webroot of your wiki server and run:
```bash
git clone https://github.com/richbodo/mw_pdf_highlights.git pdfcite
```
#### Install the required Python dependencies:
Install `pipx` to install the Python app in an isolated environment, e.g., in Debian:
```bash
sudo apt install pipx
```
Navigate to the application directory and create a virtual environment by running:
```bash
virtualenv venv
cd venv
source bin/activate
```
Install required modules:
```bash
./bin/pip install -r ../requirements.txt
```
In the environments lacking superuser permissions, use the above with the `--prefer-binary` switch.

#### Install MediaWiki extensions for your current core branch.
Navigate to the MediaWiki extensions directory and run:
```bash
git clone https://github.com/wikimedia/mediawiki-extensions-Cargo.git -b REL1_39 Cargo
git clone https://github.com/wikimedia/mediawiki-extensions-PageExchange.git -b REL1_39 PageExchange
git clone https://github.com/wikimedia/mediawiki-extensions-Widgets.git -b REL1_39 Widgets 
```
Make sure the `Widgets/compiled_templates` is writable by the webserver:
```bash
chgrp www-data Widgets/compiled_templates
chmod g+w Widgets/compiled_templates
```
Download and install Widgets dependencies:
```bash
cd Widgets
composer update --no-dev
```
Enable extensions in the MediaWiki config file (`LocalSettings.php`):
```bash
wfLoadExtension( 'Cargo' );
wfLoadExtension( 'PageExchange' );
wfLoadExtension( 'Widgets' );
```
Create necessary database tables by running from the MediaWiki root:
```bash
php maintenance/update.php
```
### Application Settings
We can create a file to modify the application settings:
```bash
cp app/config.env.example app/config/.env
```
Set the desired values for the following variables:
```bash
HIGHLIGHT_COLOR=#00FF33
PORT=5000
```

### System Configuration
We need to configure:
* **Nginx** web server to serve the application in the wiki path.
* The MediaWiki **LocalSettings.php** to import the template for links generation.

#### Nginx

#### MediaWiki
Add the following lines to LocalSettings.php, below the inclusion of Page Exchange:
```bash
$wgPageExchangePackageFiles[]  = 'https://example.com/pdfcite/mediawiki/pdf-citation-highlighter.json';
```
Update database tables by running from the MediaWiki root:
```bash
php maintenance/update.php
```
Navigate to `Special:Packages` and install the **PDF Citation Highlighter** package. It will create necessary templates and documentation. 

### Running the application

The recommended way for production environments is to run the application as a system service. 

```bash
sudo cp pdf-citation-highlighter.service /etc/systemd/system/
sudo systemctl enable --now pdf-citation-highlighter.service
```
In the development environments, the application can be managed manually using the following script:

```bash
sudo ./pdf-citation-highlighter.sh start|stop|restart
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
