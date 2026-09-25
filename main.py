from idlelib import window

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import Select

options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False,
    "profile.password_manager_leak_detection": False
})

driver = webdriver.Chrome(options=options)


def login_test():
    driver.get("https://the-internet.herokuapp.com/login")
    try:
        campo_usario = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.ID, "username"))

        )
        campo_usario.send_keys("tomsmith")
        campo_senha = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.ID, "password"))
        )
        campo_senha.send_keys("SuperSecretPassword!")
        botao_login = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.radius"))
        )
        botao_login.click()

        mensgem = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.flash"))
        )
        titulo = mensgem.text

        assert "You logged into a secure area!" in titulo, 'Login nao realizado'
    except TimeoutException:
        print("Acabou tempo de procura")
    except NoSuchElementException:
        print("Nao achou 1 ou nenhum elemento")








def check_box_test():
    driver.get("https://the-internet.herokuapp.com/checkboxes")
    checkbox = driver.find_elements(By.XPATH, '//input[@type="checkbox"]')
    print(len(checkbox))
    print(checkbox[0].is_selected())
    print(checkbox[1].is_selected())

    try:
        if not checkbox[0].is_selected():
            checkbox[0].click()

        if checkbox[1].is_selected():
            checkbox[1].click()

        assert checkbox[0].is_selected(), 'Check 1 nao selecionado'
        assert not checkbox[1].is_selected(), 'Check 2  continua selecionado '

    except NoSuchElementException:
        print("No checkbox")




def dropdown_test():
    driver.get("https://the-internet.herokuapp.com/dropdown")
    dropdown = driver.find_element(By.ID, "dropdown")
    dropdown_select = Select(dropdown)
    dropdown_select.select_by_index(1)
    dropdown_select.select_by_value("2")
    opcao = dropdown_select.first_selected_option
    print(opcao.text)

    assert opcao.text == "Option 2", 'Esta selecioanda a 1 era para ser a 2'




def janela_test():
    driver.get("https://the-internet.herokuapp.com/windows")
    click_janela = driver.find_element(By.XPATH, '//a[@href="/windows/new"]')
    aba_original = driver.current_window_handle
    click_janela.click()
    driver.switch_to.window(driver.window_handles[1])
    h3 = driver.find_element(By.TAG_NAME, 'h3')
    p = h3.text
    assert p == 'New Window', 'Outro Texto'
    driver.close()
    driver.switch_to.window(aba_original)




def iframe_test():
    driver.get("https://the-internet.herokuapp.com/iframe")
    iframe = driver.find_element(By.ID, "mce_0_ifr")
    driver.switch_to.frame(iframe)
    p = driver.find_element(By.TAG_NAME, "p")
    texto = p.text
    assert texto == "Your content goes here.", 'Outro texto'
    driver.switch_to.default_content()
    h3 = driver.find_element(By.TAG_NAME, "h3")
    h3_text = h3.text
    assert h3_text == "An iFrame containing the TinyMCE WYSIWYG Editor", 'Outro texto'




def js_alertas_test():
    driver.get("https://the-internet.herokuapp.com/javascript_alerts")
    js_alerta = driver.find_element(By.XPATH, '//button[@onclick="jsAlert()"]')
    js_alerta.click()
    alerta = WebDriverWait(driver,5).until(
        EC.alert_is_present()
    )
    print(alerta.text)
    alerta.accept()

    js_confirm = driver.find_element(By.XPATH, '//button[@onclick="jsConfirm()"]')
    js_confirm.click()
    alerta_confirm = WebDriverWait(driver, 5).until(
        EC.alert_is_present()
    )
    alerta_confirm.accept()

    js_Prompt = driver.find_element(By.XPATH, '//button[@onclick="jsPrompt()"]')
    js_Prompt.click()
    alerta_prompt = WebDriverWait(driver, 5).until(
        EC.alert_is_present()
    )
    alerta_prompt.send_keys("Heavy")
    alerta_prompt.accept()

    result = driver.find_element(By.ID, "result")
    texto = result.text
    print(texto)
    assert texto == "You entered: Heavy", 'texto errado'



try:
    login_test()
    check_box_test()
    dropdown_test()
    janela_test()
    iframe_test()
    js_alertas_test()
finally:
    driver.quit()