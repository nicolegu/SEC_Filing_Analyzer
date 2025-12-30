from bs4 import BeautifulSoup
import re

def explore_html_structure(html_path):
    """
    Explore the structure of an extracted HTML file to find Item 1A.
    """
    with open(html_path, 'r', encoding = 'utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Search for "Item 1A" or "Risk Factors"
    print('=== Searching for Item 1A / Risk Factors ===\n')

    # Method 1: Search in text
    item1a_elements = soup.find_all(string=re.compile(r'Item\s*1A', re.IGNORECASE))

    print(f"Found {len(item1a_elements)} elements containing 'Item 1A':\n")
    for i, elem in enumerate(item1a_elements[:3]):
        parent = elem.parent
        print(f"{i+1}. Tag: <{parent.name}>")
        print(f" Attributes: {parent.attrs}")
        print(f" Text preview: {str(elem)[:100]}...\n")

    # Method 2: Look for common section headers
    print("\n=== Common heading tags ===")
    for tag in ['h1', 'h2', 'h3', 'h4', 'span', 'p', 'div']:
        headers = soup.find_all(tag, string=re.compile(r'Item\s*1A|Risk\s*Factors', re.IGNORECASE))
        if headers:
            print(f"\n<{tag}> tags with Item 1A:")
            for h in headers[:2]: # Top 3 risk factors
                print(f"  - {h.get('class', 'no class')}: {h.get_text()[:80]}")

def extract_section(html_path, section_name='Item 1A', debug = True):
    """
    Extract a specific section from the 10-K HTML.

    Args:
        html_path: Path to extracted HTML file
        section_name: Section to extract (e.g., "Item 1A", "Item 7")

    Returns:
        Extracted text content
    """
    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    if debug:
        print(f"Looking for section: {section_name}")

    # Find the section header - look for bold span containing the item
    section_pattern = re.compile(rf'{section_name}[\.\s]*', re.IGNORECASE)

    # Find span with font-weight:700 (bold) containing the section name
    header_span = soup.find('span', string=section_pattern, style=re.compile(r'font-weight:\s*700'))

    if not header_span:
        if debug:
            print(f"Could not find bold span with '{section_name}'")
        return None
    
    if debug:
        print(f"Found header span: {header_span.get_text()[:50]}")
    
    # Get the parent div of header span
    header_div = header_span.find_parent('div')

    if not header_div:
        if debug:
            print(f"Could not find parent div")
        return None
    
    next_section_pattern = re.compile(r'Item\s*1[B-Z]|Item\s*[2-9]', re.IGNORECASE)
    text_content = []

    search_div = header_div

    for level in range(3):
        if debug:
            print(f"\nTrying level {level}...")
    
        siblings = []
        for sibling in search_div.find_next_siblings('div'):
            text = sibling.get_text(separator = ' ', strip = True)
            if text:
                siblings.append(sibling)
        
        if debug:
            print(f"Found {len(siblings)} sibling divs")
            if siblings:
                print(f"First sibling preview: {siblings[0].get_text()[:100]}")
        
        if siblings:
            for sibling in siblings:
                bold_spans = sibling.find_all('span', style = re.compile(r'font-weight:\s*700'))

                should_stop = False
                for span in bold_spans:
                    span_text = span.get_text(strip = True)
                    if next_section_pattern.search(span_text):
                        should_stop = True
                        if debug:
                            print(f"Stopped at: {span_text}")
                        break

                if should_stop:
                    break

                # Extract text
                text = sibling.get_text(separator = ' ', strip = True)
                if text:
                    text_content.append(text)

            if text_content:
                break

        parent = search_div.find_parent('div')
        if not parent:
            if debug:
                print("No more parent levels")
            break
        search_div = parent

    if debug:
        print(f"\n Collected {len(text_content)} text blocks")
        if text_content:
            print(f"First block preview: {text_content[0][:100]}")

    result = '\n\n'.join(text_content)
    return result if result else None



html_file = 'sec-edgar-filings/GS/10-K/0000886982-23-000003/extracted-10k.html'

# explore_html_structure(html_file)

risk_factors = extract_section(html_file, debug=True)

if risk_factors:
    print(f'\n=== Extracted Risk Factors ===')
    print(f"Total length: {len(risk_factors)} characters")
    print(risk_factors[:500])
