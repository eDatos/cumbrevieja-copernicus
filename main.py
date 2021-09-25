import scrap

vectors_url, pdf_url = scrap.get_links()
scrap.download_vectors(vectors_url)
