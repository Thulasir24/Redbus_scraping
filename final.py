from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import mysql.connector
from mysql.connector import Error


def initialize_driver():
    """Initialize the WebDriver."""
    options = Options()
    options.headless = True  # Run browser in headless mode (no GUI)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


def scrape_redbus_data(url):
    """Scrape bus data from the Redbus website."""
    driver = initialize_driver()
    driver.get(url)

    # Wait for the page to load
    time.sleep(5)

    bus_data = []

    # Find all bus elements
    buses = driver.find_elements(By.CSS_SELECTOR, "div.bus-container")  # Adjust selector as needed

    for bus in buses:
        try:
            route_name = bus.find_element(By.CSS_SELECTOR, "div[class='travels lh-24 f-bold d-color']").text
        except Exception as e:
            route_name = "N/A"
            print(f"Error finding route name: {e}")

        try:
            bus_type = bus.find_element(By.CSS_SELECTOR, "div[class='bus-type']").text
        except Exception as e:
            bus_type = "N/A"
            print(f"Error finding bus type: {e}")

        try:
            departing_time = bus.find_element(By.CSS_SELECTOR, "div[class='dp-time f-19 d-color f-bold']").text
        except Exception as e:
            departing_time = "N/A"
            print(f"Error finding departing time: {e}")

        try:
            duration = bus.find_element(By.CSS_SELECTOR, "div[class='dur l-color l-bold']").text
        except Exception as e:
            duration = "N/A"
            print(f"Error finding duration: {e}")

        try:
            reaching_time = bus.find_element(By.CSS_SELECTOR, "div[class='ar-time f-19 d-color f-bold']").text
        except Exception as e:
            reaching_time = "N/A"
            print(f"Error finding reaching time: {e}")

        try:
            star_rating = bus.find_element(By.CSS_SELECTOR, "div[class='rtng-container f-12 clearfix']").text
        except Exception as e:
            star_rating = "N/A"
            print(f"Error finding star rating: {e}")

        try:
            price = bus.find_element(By.CSS_SELECTOR, "span[class='f-19 f-bold']").text
        except Exception as e:
            price = "N/A"
            print(f"Error finding price: {e}")

        try:
            seat_availability = bus.find_element(By.CSS_SELECTOR, "div[class='seat-left m-top-16']").text
        except Exception as e:
            seat_availability = "N/A"
            print(f"Error finding seat availability: {e}")

        bus_data.append({
            'route_name': route_name,
            'bus_type': bus_type,
            'departing_time': departing_time,
            'duration': duration,
            'reaching_time': reaching_time,
            'star_rating': star_rating,
            'price': price,
            'seat_availability': seat_availability
        })

    driver.quit()
    return bus_data


def store_data_in_database(bus_data):
    """Store scraped data in MySQL database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your MySQL username
            password="tulsitulsi",  # Replace with your MySQL password
            database="redbus_data"  # Replace with your MySQL database name
        )

        cursor = connection.cursor()

        # Create table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS bus_routes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            route_name VARCHAR(255),
            bus_type VARCHAR(255),
            departing_time VARCHAR(255),
            duration VARCHAR(255),
            reaching_time VARCHAR(255),
            star_rating VARCHAR(255),
            price VARCHAR(255),
            seat_availability VARCHAR(255)
        )
        """)

        # Insert data into table
        for data in bus_data:
            cursor.execute("""
            INSERT INTO bus_routes (route_name, bus_type, departing_time, duration, reaching_time, star_rating, price, seat_availability)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (data['route_name'], data['bus_type'], data['departing_time'], data['duration'],
                  data['reaching_time'], data['star_rating'], data['price'], data['seat_availability']))

        connection.commit()
        print("Data stored successfully.")

    except Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def main():
    url = "https://www.redbus.in/"  # Replace with the actual URL you want to scrape
    bus_data = scrape_redbus_data(url)
    store_data_in_database(bus_data)


if __name__ == "__main__":
    main()
