import csv
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from bs4 import BeautifulSoup

def _page_uni(driver):
    driver.get("https://resultados.admision.uni.edu.pe/dia1.html")
    time.sleep(2)
    select_element = driver.find_element(By.NAME, value = 'tbl_resultados_voca_length')
    select = Select(select_element)
    select.select_by_value("100")
    time.sleep(2)

    with open("data/resultados_uni.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Código", "Nombre", "Puntaje"])

        def extract_table():
            soup = BeautifulSoup(driver.page_source, "html.parser")
            table = soup.find("table", {"id": "tbl_resultados_voca"})
            
            for row in table.find_all("tr")[1:]:
                cols = row.find_all("td")
                if len(cols) > 0:
                    codigo = cols[0].text.strip()
                    nombre = cols[1].text.strip()
                    puntaje = cols[2].text.strip().replace(',', '') 
                    writer.writerow([codigo, nombre, puntaje])

        extract_table()

        while True:
            try:
                next_button = driver.find_element(By.ID, "tbl_resultados_voca_next")
                if "disabled" in next_button.get_attribute("class"):
                    break
                
                next_button.click()
                time.sleep(1) 
                
                extract_table()
            
            except Exception as e:
                print(f"Error al hacer clic en siguiente: {e}")
                break

    driver.quit()
    print("Los datos se han guardado en resultados_uni.csv")