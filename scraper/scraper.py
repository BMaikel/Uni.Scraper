import csv
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

URLS_UNI = [
    "https://resultados.admision.uni.edu.pe/dia1.html",
    "https://resultados.admision.uni.edu.pe/dia2.html",
    "https://resultados.admision.uni.edu.pe/dia3.html"
]

URL_UNALM = "https://resultados.lamolina.edu.pe/resultados"

def extract_table(driver):
    """Extrae los datos de la tabla y detecta los encabezados dinámicamente."""

    soup = BeautifulSoup(driver.page_source, "html.parser")
    table = soup.find("table", {"id": "tbl_resultados_voca"})

    headers = []
    thead = table.find("thead")

    if thead:
        headers = [th.text.strip() for th in thead.find_all("th")]

    data = []
    tbody = table.find("tbody")

    if tbody:
        for row in tbody.find_all("tr"):
            cols = row.find_all("td")
            if len(cols) > 0:
                row_data = {headers[i]: cols[i].text.strip() if i < len(cols) else "N/A" for i in range(len(headers))}
                data.append(row_data)

    return headers, data

def scrape_uni_results(driver, url, filename):
    """Realiza el scraping de una página y guarda los datos en un archivo CSV."""

    driver.get(url)
    sleep(3)
    wait = WebDriverWait(driver, 10)

    try:
        select_element = wait.until(EC.presence_of_element_located((By.NAME, "tbl_resultados_voca_length")))
        select = Select(select_element)
        select.select_by_value("100")

    except Exception as e:
        print(f"Error al seleccionar cantidad de resultados: {e}")
        return

    results = []
    headers = []

    while True:
        try:
            headers, page_data = extract_table(driver)
            results.extend(page_data)

            next_button = driver.find_element(By.ID, "tbl_resultados_voca_next")
            if "disabled" in next_button.get_attribute("class"):
                break
            
            next_button.click()
            sleep(1)

        except Exception as e:
            print(f"Error al hacer clic en siguiente: {e}")
            break

    if results:
        save_to_csv(results, headers, filename)


def save_to_csv(data, headers, filename):
    """Guarda los datos en un archivo CSV con encabezados dinámicos."""

    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
        print(f"Los datos se han guardado en {filename}")

    except Exception as e:
        print(f"Error al guardar el archivo CSV: {e}")


def scrape_unalm_results(driver, url, filename):
    """Realiza el scraping de resultados unalm y guarda los datos en un archivo CSV."""

    driver.get(url)

    sleep(3)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "button-lista-2"))
    ).click()
    sleep(1)

    carreras = driver.find_elements(By.CLASS_NAME, "ingresantes-carrera")
    
    all_data = []

    for i in range(len(carreras)):
        carreras[i].click()
        sleep(3)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        contenedor = soup.find("div", {"id": "contenedor-ingresantes"})

        if contenedor:
            filas = contenedor.find_all("div", recursive=False)  # Obtener solo los divs de primer nivel

            for fila in filas:
                columnas = [col.text.strip() for col in fila.find_all("div", recursive=False)]
                if columnas:
                    all_data.append(columnas)

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(all_data)

    print(f"Datos guardados en {filename}")


def scrape_uni_pages(driver):
    """Recorre todas las URLs y guarda los datos en archivos separados."""

    for i, url in enumerate(URLS_UNI, start = 1):
        filename = f"data/resultados_dia{i}.csv"
        print(f"Scraping {url} y guardando en {filename} ...")
        scrape_uni_results(driver, url, filename)
    

def scrape_unalm(driver):
    """Recorre todas las URLs y guarda los datos en archivos separados."""
    scrape_unalm_results(driver, URL_UNALM, "test")
    
