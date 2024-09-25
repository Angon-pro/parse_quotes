import math
import time
import typing as tp

from datetime import datetime, timedelta

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains


class SeleniumParser:
    @staticmethod
    async def parse_content(url: str) -> None:
        driver: tp.Optional[webdriver.Firefox()] = None
        graph: tp.Any = None
        graph_width: int = 0
        graph_height: int = 0
        actions: tp.Optional[ActionChains] = None
        try:
            driver = webdriver.Firefox()
            driver.get(url)
            sleep_time: int = 5
            time.sleep(sleep_time)
            btn_sel: str = '#finfin-local-plugin-block-item-quote-chart-txchart-zoom > span:nth-child(5)'
            button: tp.Any = WebDriverWait(driver, sleep_time).until(
                ec.element_to_be_clickable((By.CSS_SELECTOR, btn_sel)))
            button.click()
            sleep_time = 1
            time.sleep(sleep_time)
            graph_sel: str = '#infinity-ui-main-chart > div > div.sc-jCHUfY.hEPfka > canvas'
            graph = driver.find_element(By.CSS_SELECTOR, graph_sel)
            width_sel: str = 'width'
            height_sel: str = 'height'
            graph_width = graph.size[width_sel]
            graph_height = graph.size[height_sel]
            actions = ActionChains(driver)
        except Exception as e:
            print(f"Error: {e}")
            if driver:
                driver.quit()
                return
        y_offset: int = int(graph_height / 2)
        x_offset: int = -(math.ceil(graph_width / 2))
        value_buff: str = ''
        week: int = -1
        for i in range(int(graph_width)):
            try:
                x_offset += 1
                actions.move_to_element_with_offset(graph, x_offset, y_offset).perform()
                sleep_time: float = .2
                time.sleep(sleep_time)
                value_sel: str = '#infinity-ui-main-chart > div > div.sc-bdvvtL.grcRoN > div:nth-child(3)'
                value: str = driver.find_element(By.CSS_SELECTOR, value_sel).text.replace('\n', '\t')
                if value == value_buff:
                    continue
                value_buff = value
                week += 1
                today: datetime.date = datetime.now().date()
                days_since_monday: int = today.weekday()
                last_monday: datetime.date = today - timedelta(days=days_since_monday)
                cur_last_monday: datetime.date = last_monday - timedelta(weeks=1)
                first_monday: datetime.date = cur_last_monday - timedelta(weeks=52)
                print(f"Date: {first_monday + timedelta(weeks=week)}, Quotes: {value}")
            except Exception as e:
                print(f"Error: {e}")
                continue
            finally:
                if i == graph_width - 1:
                    driver.quit()
