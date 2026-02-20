




from bs4 import BeautifulSoup

def parse_summary(summary: str):
    soup = BeautifulSoup(summary, "html.parser")

    # Extract status
    #edge case of no status --> may be error or some garbage entry in the rss feed 
    #does this take the First B tag that is found in the file HTML element. otherwise the logic can fail.
    status_tag = soup.find("b")
    #if no status if found then make the status as undefined 
    status = status_tag.text.replace("Status:", "").strip()


    # Extract product
    #edge case where no product is mentioned -- Here return the product as undefined product.
    #case where multiple products are mentioned -- Here return the list of products separated by a comma and these product values will be enclosed in a UL tag which wraps up the all ul tags.
    product = soup.find("li").text.strip()

    # Extract plain message text
    # As but the structure that I got, I'm okay with this logic.
    text_parts = soup.get_text(separator="\n").split("\n")
    text_parts = [t.strip() for t in text_parts if t.strip()]
    
    # message is second meaningful line
    message = text_parts[1]

    return f"Product: {product}\nStatus: {status}, {message}"