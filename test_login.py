import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestProctoringLogin:
    def setup_method(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")  # Запуск в фоне
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        # Получаем хост из переменных окружения или используем localhost
        selenium_host = os.getenv('SELENIUM_HOST', 'localhost')
        selenium_port = os.getenv('SELENIUM_PORT', '4444')
        
        self.driver = webdriver.Remote(
            command_executor=f"http://{selenium_host}:{selenium_port}/wd/hub",
            options=options
        )
        self.wait = WebDriverWait(self.driver, 10)
        
        # Создаем папку для результатов, если её нет
        self.results_dir = "/app/test_results"  # Путь внутри контейнера
        os.makedirs(self.results_dir, exist_ok=True)

    def teardown_method(self):
        self.driver.quit()

    def test_login_page_has_auth_text(self):
        # Открываем страницу
        self.driver.get("https://proctoring.moevm.info")
        
        # Проверяем наличие надписи "Авторизация"
        auth_element = self.wait.until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Авторизация')]"))
        )
        
        # Дополнительно проверяем, что элемент видим
        assert auth_element.is_displayed(), "Элемент с текстом 'Авторизация' не видим на странице"
        
        # Делаем скриншот с полным путем
        screenshot_path = os.path.join(self.results_dir, "login_page.png")
        self.driver.save_screenshot(screenshot_path)
        print(f"✓ Скриншот сохранен: {screenshot_path}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])