# D3XT3COGNITION

<img width="1099" height="264" alt="image" src="https://github.com/user-attachments/assets/c4ec1ca9-d645-48a3-97a1-4fd2786060e8" />


**DEXTER** is a Python-based website information gathering framework for penetration testers, bug bounty hunters, and security researchers who need a structured first look at a target before vulnerability assessment.

DEXTER combines passive and active reconnaissance signals into one command-line workflow. It focuses on collecting, fingerprinting, correlating, and presenting useful website intelligence such as headers, cookies, metadata, technologies, CMS hints, JavaScript assets, endpoints, DNS, TLS, WAF indicators, WordPress details, and optional external-tool results through **two scanning modes**: **Basic Scan** and **Deep Scan**.

> DEXTER is an information gathering framework. It is **not** an exploit framework, **not** a vulnerability scanner, and **not** a replacement for tools such as Nuclei.

## Purpose

Modern reconnaissance often requires running many tools manually, then correlating their outputs by hand. DEXTER is designed to reduce that friction by providing a single CLI that can gather and organize website intelligence.

The intended workflow is:

```text
Information Gathering -> Fingerprinting -> Correlation -> Knowledge -> Pentest Preparation
```

DEXTER helps answer questions such as:

* What web server, language, CMS, framework, or library is likely being used?
* Are security headers present or missing?
* Are interesting endpoints, forms, emails, scripts, comments, robots, or sitemap entries exposed?
* Is the site likely using WordPress, and if so, what themes/plugins can be observed?
* Are DNS, TLS, WAF, or external reconnaissance signals worth reviewing before deeper testing?

## Features

### Basic Scan

The default scan performs fast website reconnaissance using internal engines:

* HTTP headers
* Cookies
* Page metadata and meta tags
* Security headers
* Technologies and versions
* CMS and framework hints
* JavaScript libraries
* Endpoints and forms
* Interesting HTML comments
* Email addresses found in page source
* Evidence and confidence signals
* Local fingerprint matching
* Knowledge correlation

Example:

```bash
dexter scan example.com
```

### Deep Scan

Deep scan enables additional reconnaissance engines and external adapters where available:

* DNS inspection
* TLS inspection
* robots.txt parsing
* sitemap parsing
* JavaScript asset collection
* CMS and WordPress enrichment
* WAF detection
* Confidence scoring
* Optional external tools:

  * httpx
  * WhatWeb
  * WPScan
  * WAFW00F
  * Katana
  * Subfinder

Example:

```bash
dexter scan example.com --deep
```

If an external tool is not installed, DEXTER will report that clearly and continue with the rest of the scan.

## Commands

## `scan`

Main command for reconnaissance and streaming results to the terminal.

### Basic scan

```bash
python -m dexter scan example.com
```

### Deep scan

DNS, TLS, WAF, CMS, and external adapters:

```bash
python -m dexter scan example.com --deep
```

### Scan and save reports

Save output as JSON, Markdown, TXT, and HTML:

```bash
python -m dexter scan example.com --save
```

### Deep scan and save reports

```bash
python -m dexter scan example.com --deep --save
```

### Scan without the summary panel

```bash
python -m dexter scan example.com --no-summary
```

### If installed via `pip install -e .`

```bash
dexter scan example.com --deep --save
```

## `report`

Runs scan + automatically saves all report formats to disk.

### Basic report

```bash
python -m dexter report example.com
```

### Deep report

```bash
python -m dexter report example.com --deep
```

### Custom output folder

```bash
python -m dexter report example.com --deep --output /tmp/hasil-scan
```

### Via pip-installed command

```bash
dexter report example.com --deep -o ./my-reports
```

### Report output structure

Reports are saved to:

```text
reports/
└── example.com/
    └── 20250709_142301/
        ├── report.json
        ├── report.md
        ├── report.txt
        └── report.html
```

## `version`

Show the installed version.

```bash
python -m dexter version
dexter version
```

## `help`

View available options for every command.

```bash
python -m dexter --help
python -m dexter scan --help
python -m dexter report --help
```

## Example Output

DEXTER is designed to produce structured reconnaissance output such as:

```text
Target
example.com

Technology
Apache
PHP
WordPress
jQuery
Cloudflare

Versions
Apache 2.4.63
PHP 8.3.29
WordPress 6.5

CMS
WordPress

Security Headers
Content-Security-Policy: Missing
Strict-Transport-Security: Present
X-Frame-Options: Present

Endpoints
https://example.com/wp-json/
https://example.com/wp-content/themes/astra/style.css

WordPress
Detected: true
Theme: astra
REST API: enabled
XMLRPC: detected

DNS / TLS / WAF
Available in deep scan mode
```

Actual output depends on the target, network conditions, and installed external tools.

## Architecture

DEXTER is built with a modular pipeline:

```text
CLI
|
Scanner
|
Registry
|
Engines
|
Context
|
Results
|
Renderer
```

External tools are integrated through adapters:

```text
Scanner
|
Adapter Manager
|
Adapters
|
httpx / WhatWeb / WPScan / Katana / Subfinder / WAFW00F
```

### Core Concepts

* **CLI**: User-facing command interface.
* **Scanner**: Coordinates the scan flow.
* **ScanContext**: Stores target state, response data, shared session, and collected results.
* **Engines**: Internal modules that analyze HTTP responses, headers, HTML, DNS, TLS, CMS hints, and other signals.
* **Adapters**: Wrappers for external reconnaissance tools.
* **Renderer**: Displays scan results in readable terminal tables and panels.

## Project Structure

```text
dexter/
├── adapters/         External tool integrations
├── core/             Scanner, registry, context, adapter manager
├── engines/          Internal reconnaissance and correlation engines
├── fingerprints/     YAML fingerprints for CMS/framework/library detection
├── knowledge/        Software knowledge base entries
├── reports/          Report generation modules
├── templates/        HTML report template
├── ui/               CLI output rendering
└── cli.py            Typer CLI commands
```

## Installation

### Requirements

* Python 3.10 or newer
* pip
* Git

### Install from source

```bash
git clone https://github.com/D3XT3R404/D3XT3COGNITION.git
cd D3XT3COGNITION
python -m pip install -e .
```

### Development install with requirements

```bash
python -m pip install -r requirements.txt
```

### Verify installation

```bash
dexter version
```

You can also run it as a Python module:

```bash
python -m dexter scan example.com
```

## Usage

### Basic scan

```bash
dexter scan example.com
```

You may pass a domain or a full URL:

```bash
dexter scan https://example.com
dexter scan http://example.com
```

If no scheme is provided, DEXTER tries HTTPS first and can fall back to HTTP when needed.

### Deep scan

```bash
dexter scan example.com --deep
```

Deep scan may take longer because it can perform DNS, TLS, robots, sitemap, WordPress, WAF, and external-tool checks.

### Scan and save reports

```bash
dexter scan example.com --save
dexter scan example.com --deep --save
```

### Report command

```bash
dexter report example.com
dexter report example.com --deep
```

### Version

```bash
dexter version
```

## Optional External Tools

DEXTER works without external tools, but deep scan becomes more powerful when these binaries are installed and available in your `PATH`.

### httpx

Used for HTTP probing, titles, status codes, web server data, and technology hints.

Project:

```text
https://github.com/projectdiscovery/httpx
```

### WhatWeb

Used for web technology fingerprinting.

Project:

```text
https://github.com/urbanadventurer/WhatWeb
```

### WAFW00F

Used for WAF detection.

Project:

```text
https://github.com/EnableSecurity/wafw00f
```

### Katana

Used for crawling and endpoint discovery.

Project:

```text
https://github.com/projectdiscovery/katana
```

### Subfinder

Used for subdomain discovery.

Project:

```text
https://github.com/projectdiscovery/subfinder
```

### WPScan

Used for WordPress enrichment when WordPress is detected.

Project:

```text
https://github.com/wpscanteam/wpscan
```

Optional API token:

```bash
export WPSCAN_API_TOKEN="your-token"
```

Windows PowerShell:

```powershell
$env:WPSCAN_API_TOKEN="your-token"
```

## Development

Install in editable mode:

```bash
python -m pip install -e .
```

Run tests:

```bash
python -m pytest
```

Run a local scan:

```bash
dexter scan example.com
dexter scan example.com --deep
```

## Reports

The repository contains report modules for text, Markdown, JSON, and HTML output. The CLI report workflow is still being expanded, but the codebase already includes:

* `dexter/reports/text_report.py`
* `dexter/reports/markdown_report.py`
* `dexter/reports/json_report.py`
* `dexter/reports/html_report.py`
* `dexter/templates/report.html`

## Troubleshooting

### `python` is not recognized

Install Python 3.10+ and ensure it is available in your `PATH`.

Windows users can verify with:

```powershell
python --version
```

### `dexter` command is not found

Install the project in editable mode:

```bash
python -m pip install -e .
```

Then open a new terminal and try:

```bash
dexter version
```

### Deep scan shows missing tools

Install the optional external tools you want to use and ensure their binaries are available in your `PATH`.

DEXTER will continue scanning even when optional adapters are missing.

### Deep scan takes too long

Deep scan performs heavier checks and may call external tools. Start with a basic scan first:

```bash
dexter scan example.com
```

Then run deep scan only when needed:

```bash
dexter scan example.com --deep
```

### Basic scan returns little information

Some websites hide or minimize technology signals. Try:

```bash
dexter scan https://target.com --deep
```

Also verify the target is reachable from your network.

## Roadmap

Planned and possible future integrations:

* Nuclei
* Naabu
* Waybackurls
* Gau
* Hakrawler
* Assetfinder
* Shodan API
* BuiltWith API
* VirusTotal API
* More report export workflows
* Improved confidence scoring
* Richer fingerprint and knowledge base coverage

## Legal Notice

Use DEXTER only on targets you own or are authorized to test. Unauthorized scanning may violate laws, terms of service, or responsible disclosure rules.

DEXTER is intended for legitimate security research, penetration testing preparation, and bug bounty reconnaissance.

## License

This project includes a `LICENSE` file. Update it with your intended open-source license before public release if it is currently empty.
