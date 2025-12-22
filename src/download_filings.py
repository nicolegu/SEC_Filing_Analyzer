from sec_edgar_downloader import Downloader
from config import company_name, email

def download_10K(tickers, company_name = 'Your Name/Company', email = 'your.email@example.com', limit = 5):
    """
    Download Form 10-K from tickers

    Args:
        tickers: List of ticker symbols
        limit: Number of most recent filings to download per ticker

    Returns:
        Dict with success/failure counts and failed tickers
    """

    dl = Downloader(company_name, email)

    successful = []
    failed = []

    for ticker in tickers:
        try:
            dl.get('10-K', ticker, limit = limit)
            successful.append(ticker)
            print('Download complete! Check edgar/filings/ticker/10-K/')

        except Exception as e:
            failed.append(ticker)
            print(f"Failed to download {ticker}: {str(e)}")

    print(f"\n=== Download Complete ===")
    print(f"Successful: {len(successful)}/{len(tickers)}")
    print(f"Files location: sec-edgar-filings/[TICKER]/10-K/")

    if failed:
        print(f"Failed tickers: {', '.join(failed)}")

    return {
        'successful': successful,
        'failed': failed,
        'total': len(tickers)
    }

tickers = ['JPM', 'BAC', 'C', 'WFC', 'GS', 'USB', 'PNC', 'MTB', 'CFG', 'OZK']
results = download_10K(
    tickers=tickers,
    company_name=company_name,
    email=email,
    limit=5
)
