import re
import os

def extract_html_from_txt(txt_path, output_path=None):
    """
    Extract HTML document from SEC .txt filing.

    Ags:
       txt_path: Path to the full-submission.txt file
       ouput_path: Where to save extracted HTML (optional)

    Returns:
       HTML content as string
    """
    with open(txt_path, 'r', encoding = 'utf-8', errors = 'ignore') as f:
        content = f.read()
    
    # Find the main HTML document (usually between <DOCUMENT> tags)
    # Look for TYPE="10-K" document
    pattern = r'<DOCUMENT>.*?<TYPE>10-K.*?<TEXT>(.*?)</TEXT>.*?</DOCUMENT>'
    # Match all characters, including newline characters
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)

    if match:
        text_content = match.group(1).strip()

        # Check if HTML is wrapped in XBRL tags
        if '<XBRL>' in text_content:
            # Extract HTML from inside XBRL tags
            xbrl_pattern = r'<XBRL>.*?(<html.*?</html>).*?</XBRL>' # Non-greedy match, stops at </html>s
            xbrl_match = re.search(xbrl_pattern, text_content, re.DOTALL | re.IGNORECASE)
            if xbrl_match:
                html_content = xbrl_match.group(1).strip()
            else:
                # Fallback: remove XBRL tags and only keep content
                html_content = re.sub(r'</?XBRL>', '', text_content)
        else:
            # No XBRL wrapper, look for HTML directly
            html_match = re.search(r'(<!DOCTYPE.*|<html.*)', text_content, re.DOTALL | re.IGNORECASE)
            html_content = html_match.group(1).strip() if html_match else text_content

        # Save if output path provided
        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"Extracted HTML to {output_path}")

        return html_content
    
    else:
        print(f"No 10-K document found in {txt_path}")
        return None

def process_all_filings(base_dir='sec-edgar-filings'):
    """
    Extract HTML from all downloads .txt files
    """
    for ticker in os.listdir(base_dir):
        ticker_path = os.path.join(base_dir, ticker, '10-K')

        if not os.path.exists(ticker_path):
            continue

        for filing in os.listdir(ticker_path):
            filing_path = os.path.join(ticker_path, filing)
            txt_file = os.path.join(filing_path, 'full-submission.txt')

            if os.path.exists(txt_file):
                html_output = os.path.join(filing_path, 'extracted-10k.html')
                extract_html_from_txt(txt_file, html_output)

process_all_filings()