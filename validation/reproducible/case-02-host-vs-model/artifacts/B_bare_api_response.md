# E-commerce Product Price Scraper

Here's a robust Python function for scraping product pricing data:

```python
import requests
from bs4 import BeautifulSoup
import time
from typing import Dict, List, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def scrape_product_pricing(
    url: str,
    price_selector: str,
    name_selector: Optional[str] = None,
    timeout: int = 10,
    retry_attempts: int = 3
) -> Optional[Dict[str, str]]:
    """
    Scrape product pricing from an e-commerce product page.
    
    Args:
        url: The product page URL
        price_selector: CSS selector for the price element
        name_selector: CSS selector for the product name (optional)
        timeout: Request timeout in seconds
        retry_attempts: Number of retry attempts on failure
        
    Returns:
        Dictionary with product data or None if scraping fails
    """
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    for attempt in range(retry_attempts):
        try:
            logger.info(f"Attempting to scrape {url} (Attempt {attempt + 1}/{retry_attempts})")
            
            # Make the request
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()  # Raise exception for bad status codes
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract price
            price_element = soup.select_one(price_selector)
            if not price_element:
                logger.warning(f"Price element not found with selector: {price_selector}")
                return None
            
            price = price_element.get_text(strip=True)
            
            # Extract product name if selector provided
            product_name = None
            if name_selector:
                name_element = soup.select_one(name_selector)
                product_name = name_element.get_text(strip=True) if name_element else "N/A"
            
            result = {
                'url': url,
                'price': price,
                'product_name': product_name,
                'status': 'success'
            }
            
            logger.info(f"Successfully scraped: {result}")
            return result
            
        except requests.exceptions.Timeout:
            logger.error(f"Timeout error on attempt {attempt + 1}")
            if attempt < retry_attempts - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
                
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error: {e.response.status_code} - {e}")
            if e.response.status_code == 429:  # Too Many Requests
                logger.info("Rate limited. Waiting before retry...")
                time.sleep(5 * (attempt + 1))
            elif e.response.status_code in [403, 401]:
                logger.error("Access denied. Check if scraping is blocked.")
                return None
            elif attempt >= retry_attempts - 1:
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {e}")
            if attempt >= retry_attempts - 1:
                return None
                
        except Exception as e:
            logger.error(f"Unexpected error: {type(e).__name__} - {e}")
            return None
    
    return None


def scrape_multiple_products(
    products: List[Dict[str, str]],
    delay: float = 1.0
) -> List[Dict[str, str]]:
    """
    Scrape multiple products with rate limiting.
    
    Args:
        products: List of dicts with 'url', 'price_selector', and optional 'name_selector'
        delay: Delay between requests in seconds
        
    Returns:
        List of scraped product data
    """
    results = []
    
    for i, product in enumerate(products):
        logger.info(f"Scraping product {i + 1}/{len(products)}")
        
        result = scrape_product_pricing(
            url=product['url'],
            price_selector=product['price_selector'],
            name_selector=product.get('name_selector')
        )
        
        if result:
            results.append(result)
        
        # Rate limiting - be respectful
        if i < len(products) - 1:
            time.sleep(delay)
    
    return results


# Example usage
if __name__ == "__main__":
    # Example 1: Single product
    product_data = scrape_product_pricing(
        url="https://example-store.com/product/12345",
        price_selector=".price-current",
        name_selector="h1.product-title"
    )
    
    if product_data:
        print(f"Product: {product_data['product_name']}")
        print(f"Price: {product_data['price']}")
    
    # Example 2: Multiple products
    products_to_scrape = [
        {
            'url': 'https://example-store.com/product/12345',
            'price_selector': '.price-current',
            'name_selector': 'h1.product-title'
        },
        {
            'url': 'https://example-store.com/product/67890',
            'price_selector': '.price-current',
            'name_selector': 'h1.product-title'
        }
    ]
    
    results = scrape_multiple_products(products_to_scrape, delay=2.0)
    
    print(f"\nScraped {len(results)} products successfully")
    for result in results:
        print(f"- {result['product_name']}: {result['price']}")
```

## Key Features:

1. **Proper User-Agent**: Mimics a real browser to avoid basic bot detection
2. **Error Handling**: Catches timeouts, HTTP errors, and connection issues
3. **Retry Logic**: Automatic retries with exponential backoff
4. **Rate Limiting**: Delays between requests to be respectful
5. **Logging**: Comprehensive logging for debugging
6. **Flexible Selectors**: CSS selectors for different site structures
7. **Type Hints**: Better code documentation and IDE support

## Usage Tips:

```python
# Install dependencies first
# pip install requests beautifulsoup4

# To find the right CSS selectors:
# 1. Open browser DevTools (F12)
# 2. Right-click the price element → Inspect
# 3. Use the selector tool or copy CSS selector
```

## Important Notes:

- Always respect `robots.txt`
- Add delays between requests (1-2 seconds minimum)
- Monitor for rate limiting (429 status codes)
- Consider using a session for multiple requests
- Some sites may require additional headers or cookies
- For JavaScript-heavy sites, consider using Selenium or Playwright instead