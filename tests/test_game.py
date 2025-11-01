import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time


@pytest.fixture
def setup_teardown():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    yield driver
    driver.quit()


def get_cells(driver):
    return driver.find_elements(By.CLASS_NAME, "cell")


def test_x_wins(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")
    moves = [0, 3, 1, 4, 2] 
    for m in moves:
        get_cells(driver)[m].click()
        time.sleep(0.2)
    msg = driver.find_element(By.ID, "msg").text
    assert "Player X wins!" in msg


def test_o_wins(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")
    moves = [0, 1, 3, 4, 8, 7]  
    for m in moves:
        get_cells(driver)[m].click()
        time.sleep(0.2)
    msg = driver.find_element(By.ID, "msg").text
    assert "Player O wins!" in msg


def test_draw(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")
    moves = [0, 1, 2, 4, 3, 5, 7, 6, 8] 
    for m in moves:
        get_cells(driver)[m].click()
        time.sleep(0.2)
    msg = driver.find_element(By.ID, "msg").text
    assert "DRAW" in msg.upper()


def test_restart_resets_board(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")
    get_cells(driver)[0].click() 
    time.sleep(0.2)
    driver.find_element(By.TAG_NAME, "button").click()
    time.sleep(0.5)
    assert all(cell.text == "" for cell in get_cells(driver)), "Board did not reset"


def test_cannot_overwrite_cell(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")
    get_cells(driver)[0].click()
    time.sleep(0.2)
    first_value = get_cells(driver)[0].text
    get_cells(driver)[0].click()
    time.sleep(0.2)
    second_value = get_cells(driver)[0].text
    assert first_value == second_value == "X", "Cell was overwritten"
