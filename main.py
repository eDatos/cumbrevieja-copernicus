import scrap

if links := scrap.get_links():
    vectors_url, pdf_url = links
    scrap.download_vectors(vectors_url)
    scrap.download_pdf(pdf_url)
