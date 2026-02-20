from bs4 import BeautifulSoup

def parse_summary(summary: str):
    soup = BeautifulSoup(summary, "html.parser")

    #find status 
    status = "Undefined"

    for b_tag in soup.find_all("b"):
        if "Status:" in b_tag.get_text():
            status = b_tag.get_text().replace("Status:", "").strip()
            break

# find the affected components
    products = []

    ul_tag = soup.find("ul")
    if ul_tag:
        for li in ul_tag.find_all("li"):
            products.append(li.get_text().strip())

    if not products:
        product_str = "Undefined Product"
    else:
        product_str = ", ".join(products)

# message
    message = "No message available"

    affected_section = soup.find("b", string=lambda x: x and "Affected components" in x)
    if affected_section:
        ul = affected_section.find_next("ul")
        if ul:
            ul.decompose()

    text_parts = soup.get_text(separator="\n").split("\n")
    text_parts = [t.strip() for t in text_parts if t.strip()]

    for line in text_parts:
        if (
            "Status:" not in line and
            "Affected components" not in line
        ):
            message = line
            break

  
    return f"Product: {product_str}\nStatus: {status}, {message}"