from requests import Session
from bs4 import BeautifulSoup
import pandas as pd
from IPython.display import display
import time


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}
productlinks = []
# Start the timer
start_time = time.time()

with Session() as session:
    # Get total number of pages
    lien="https://www.mytek.tn/informatique/serveurs.html"
    r = session.get(lien)
    soup1 = BeautifulSoup(r.content, 'lxml')
    if soup1.find('div', {'class': 'pages'}) is None:
        last_page_num=1

    else :
        page_list = soup1.find('div', {'class': 'pages'}).find('li', {'class': 'pages-item-next'}).find_previous_sibling('li').find('a')
        last_page_number = page_list.find('span', class_=None)
        last_page_num=int(last_page_number.text)    
            
        
    print(last_page_num)   

    # Loop through all pages
    for page_num in range(1, last_page_num+1):
        r = session.get(f"{lien}?p={page_num}")
        soup1 = BeautifulSoup(r.content, 'lxml')
        productlist = soup1.find_all("li", {'class': 'item product product-item'})
        productlinks += [link['href'] for product in productlist for link in product.find_all('a', class_='product photo product-item-photo', href=True)]
    print(len(productlinks))
    
    products = []
    for link in productlinks:
        r = session.get(link, headers=headers)
        soup = BeautifulSoup(r.content, 'lxml')
        name = soup.find('h1', {'class': 'page-title'}).text.strip()
        descriptiondiv = soup.find('div', itemprop="description")
        descriptionlist = descriptiondiv.find_all('p')
        description = ""
        for t in descriptionlist:
            description += t.text.strip() + '\n'
        prixx = soup.find('div', {'class': 'sidebar sidebar-additional'}).find('span', {'data-price-type': 'finalPrice'})  
        prix = prixx.text.strip()
        prixx_ap = soup.find('div', {'class': 'sidebar sidebar-additional'}).find('span', {'data-price-type': 'oldPrice'})
        prix_ap = prixx_ap.text.strip() if prixx_ap else 'none'
        promos = 'OUI' if prix_ap != 'none' else 'NON'
        ref = soup.find('div', itemprop="sku").text.strip()
        marquediv = soup.find('div', {'class': 'product info detailed'})
        m = ''
        if marquediv is not None:
            m = marquediv.find('td', {'data-th': 'Marque'})
            if m is not None:
                m = m.text.strip()


        c1=lien.split('/')[3]
        x='https://www.mytek.tn/'+c1+'.html'
        c3 = lien.split('https://www.mytek.tn/')[1].split('/', 1)[-1].split('/')[0]
        if lien.count('/') == 4:
            y=lien
            
            # Get the index of the fourth "/"
            fourth_slash_index = lien.find("/", lien.find("//") + 2)
            # Get the index of ".html"
            html_index = lien.find(".html")

            # Extract the substring between the fourth "/" and ".html"
            category = lien[fourth_slash_index + 1:html_index]
            ctg2= category.split("/")[-1]
            product = {
                'Source': "MyTEK",
                'site': "https://www.mytek.tn/",
                'Domaine':x,
                'Categorie 1':c1.capitalize(),  
                'Lien_Categorie2 ': y,
                'Categorie 2':ctg2.capitalize(),
                'Nom_Produit': name,
                'Lien_Produit': link,
                'Description_Produit': description,
                'Prix_Produit': prix,
                'Prix_Avant_Promos_Produit': prix_ap,
                'Promo_Produit': promos,
                'Reference_Produit': ref,
                'Marque_Produit': m
            }
            products.append(product)
        else:
            ctg3=soup1.find("span", {'data-ui-id': 'page-title-wrapper'}).text.strip()
            y='https://www.mytek.tn/'+c1+'/'+c3+'.html' 
            split_url = lien.split('/')
            ctg2 = split_url[4]
            l=lien
            product = {
                'Source': "MyTEK",
                'site': "https://www.mytek.tn/",
                'Domaine':x,
                'Categorie 1':c1.capitalize(),  
                'Lien_Categorie2 ': y,
                'Categorie 2':ctg2.capitalize(),
                'Lien_Categorie3 ': l,
                'Categorie 3':ctg3,
                'Nom_Produit': name,
                'Lien_Produit': link,
                'Description_Produit': description,
                'Prix_Produit': prix,
                'Prix_Avant_Promos_Produit': prix_ap,
                'Promo_Produit': promos,
                'Reference_Produit': ref,
                'Marque_Produit': m
            }
            products.append(product)
      
        


df = pd.DataFrame(products)
display(df)

# Calculate and print the elapsed time
elapsed_time = time.time() - start_time
# Convert seconds to minutes and seconds
mins, secs = divmod(elapsed_time, 60)

# Convert minutes to hours and minutes
hours, mins = divmod(mins, 60)

# Print the elapsed time
print(f"Time taken: {elapsed_time} seconds")
print(f"Time taken: {int(hours)} hours, {int(mins)} minutes, {secs:.2f} seconds")

# convert DataFrame to CSV file
#df.to_csv('Mytek_Each_Link.csv', index=False)

