from bs4 import BeautifulSoup

def parse_summary(summary: str):
    soup = BeautifulSoup(summary, "html.parser")

    # -----------------------------
    # 1️⃣ Extract Status Safely
    # -----------------------------
    status = "Undefined"

    # Look specifically for <b> tags containing "Status:"
    for b_tag in soup.find_all("b"):
        if "Status:" in b_tag.get_text():
            status = b_tag.get_text().replace("Status:", "").strip()
            break

    # -----------------------------
    # 2️⃣ Extract Products Safely
    # -----------------------------
    products = []

    ul_tag = soup.find("ul")
    if ul_tag:
        for li in ul_tag.find_all("li"):
            products.append(li.get_text().strip())

    if not products:
        product_str = "Undefined Product"
    else:
        product_str = ", ".join(products)

    # -----------------------------
    # 3️⃣ Extract Message Safely
    # -----------------------------
    message = "No message available"

    # Remove Affected components section before extracting message
    # So we don't mix component names into message
    affected_section = soup.find("b", string=lambda x: x and "Affected components" in x)
    if affected_section:
        # Remove the UL so it doesn't appear in text extraction
        ul = affected_section.find_next("ul")
        if ul:
            ul.decompose()

    text_parts = soup.get_text(separator="\n").split("\n")
    text_parts = [t.strip() for t in text_parts if t.strip()]

    # Find first meaningful line that is not status or "Affected components"
    for line in text_parts:
        if (
            "Status:" not in line and
            "Affected components" not in line
        ):
            message = line
            break

    # -----------------------------
    # Final Output
    # -----------------------------
    return f"Product: {product_str}\nStatus: {status}, {message}"