# Bibliotecas importadas
import requests
import pandas as pd

# Função para montar o banco de dados
def get_books(genero, total_books=1000):
    livros = []
    # É possível retornar apenas 40 livros por requisição na API 
    for start in range(0, total_books, 40):
        # Link da API
        url = f"https://www.googleapis.com/books/v1/volumes?q=subject:{genero}&maxResults=40&startIndex={start}"
        r = requests.get(url)
        data = r.json()

        if "items" not in data:
            break
        
    
        
        for item in data["items"]:
            # Acessando as principais "páginas" do JSON
            volume_info = item.get("volumeInfo", {})
            sale_info = item.get("saleInfo", {})
            access_info = item.get("accessInfo", {})

            # Acessando os componentes da leitura dos livros (imagem e texto) 
            reading_modes = volume_info.get("readingModes", {})
            active_modes = [k for k, v in reading_modes.items() if v is True or str(v).lower() == 'true']
            reading_modes_str = ", ".join(active_modes) if active_modes else None
            

            # Criando as linhas/colunas do database
            livros.append({
                "id": item.get("id"),
                "title": volume_info.get("title"),
                "authors": ", ".join(volume_info.get("authors", [])),
                "publisher": volume_info.get("publisher"),
                "published_date": volume_info.get("publishedDate"),
                "description": volume_info.get("description"),
                "reading_modes": reading_modes_str,
                "page_count": volume_info.get("pageCount"),
                "categories": volume_info.get("categories"),
                "language": volume_info.get("language"),
                "is_ebook": sale_info.get("isEbook"),
                "epub_is_available": access_info.get("epub", {}).get("isAvailable"),
                "pdf_is_available": access_info.get("pdf", {}).get("isAvailable"),
                "maturity_rating": volume_info.get("maturityRating"),
                "public_domain": access_info.get("publicDomain"),
                "image_links": volume_info.get("imageLinks", {}).get("thumbnail"),
                "preview_link": volume_info.get("previewLink")
            })
    
    return livros


# Principais gêneros do aplicativo
generos = ["romance", "science fiction", "fantasy", "horror", "action", "history", "theater", "poetry", "biography & autobiography", "thriller", "self-help", "science"]


livros = []

# Serão escolhidos cerca de 200 livros de cada gênero
for genero in generos:
    livros.extend(get_books(genero, 200))


livros = livros[:1000]


df = pd.DataFrame(livros)
df.to_csv("livros.csv", index=False, encoding="utf-8")


print("✅ Arquivo livros.csv criado com sucesso!")