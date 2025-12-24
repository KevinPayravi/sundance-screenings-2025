import time
import csv
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from urls import *

filmData = [["URL", "Film Name", "Category", "Description", "Tags", "Credits"]]
screeningData = [["URL", "Film Name", "Screening type", "Date", "Time", "Venue", "City"]]

def main():
    # Create CSS selectors
    css_select_title = ".sd_film_description h2.sd_textuppercase"
    css_select_category = ".sd_film_desc_label"
    css_select_description = ".sd_film_description_content"
    css_select_tags_container = ".short_cat_top"
    css_select_tag = ".sd_textuppercase"
    css_select_credits_container = ".sd_film_artists_credits_sec"
    css_select_credit_item = "li"
    css_select_credit_position = ".sd_film_artists_cr_pos"
    css_select_credit_name = ".sd_film_artists_cr_name p"

    css_select_screenings_container = (
        ".screening_sateligh_timing .screening_sateligh_timing_column_inner"
    )
    css_select_screenings = ".sd_screening_details"
    css_select_date = ".sd_film_desc_time"
    css_select_type = ".sd_film_type_text"
    css_select_venue = ".sd_film_desc_avail"
    css_select_city = ".sd_film_desc_city"

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-software-rasterizer")

    # Create instance of Chrome driver
    driver = webdriver.Chrome(options=chrome_options)

    try:
        for url in urls:
            # Open page
            print("\n==========\n")
            print(f'🔗  Opening {url}')
            driver.get(url)

            # Wait for JavaScript to execute
            time.sleep(2)

            # Get title
            try:
                title_element = driver.find_element(By.CSS_SELECTOR, css_select_title)
                title = title_element.get_attribute("textContent").strip()
                print(f'👀  Found "{title}"')
            except:
                title = "N/A"
                print("👀  Failed to find title")

            # Get category
            try:
                category_element = driver.find_element(By.CSS_SELECTOR, css_select_category)
                category = category_element.get_attribute("textContent").strip()
                print(f'📂  Category: {category}')
            except:
                category = "N/A"
                print("📂  Failed to find category")

            # Get description
            try:
                description_element = driver.find_element(By.CSS_SELECTOR, css_select_description)
                description = description_element.get_attribute("textContent").strip()
                print(f'📄  Description: {description[:75] + "..."}')
            except:
                description = "N/A"
                print("📄  Failed to find description")

            # Get tags
            try:
                tags_container_element = driver.find_element(By.CSS_SELECTOR, css_select_tags_container)
                tags_array = []
                for tag in tags_container_element.find_elements(
                    By.CSS_SELECTOR, css_select_tag
                ):
                    tag_text = tag.get_attribute("textContent").strip()
                    if (tag_text):
                        tags_array.append(tag.get_attribute("textContent").strip())
                tags = ", ".join(tags_array)
                print(f'🏷️  Tags: {tags}')
            except:
                tags = "N/A"
                print("🏷️  Failed to find tags")

            # Get credits
            try:
                credits_container_element = driver.find_element(By.CSS_SELECTOR, css_select_credits_container)
                credits = ""
                for credit in credits_container_element.find_elements(
                    By.CSS_SELECTOR, css_select_credit_item
                ):
                    position_element = credit.find_element(By.CSS_SELECTOR, css_select_credit_position)
                    position = position_element.get_attribute("textContent").strip().upper()
                    names = ""
                    for name in credit.find_elements(
                        By.CSS_SELECTOR, css_select_credit_name
                    ):
                        names += "\n" + name.get_attribute("textContent").strip()
                    credits += position + ":"
                    credits += names
                    credits += "\n\n"
            except:
                credits = "N/A"
                
            filmData.append(
                [
                    url,
                    title,
                    category,
                    description,
                    tags,
                    credits
                ]
            )

            print("\nScreenings:")

            # Get screenings container
            screenings_container_element = driver.find_element(
                By.CSS_SELECTOR, css_select_screenings_container
            )

            # Iterate through each screening
            for screening in screenings_container_element.find_elements(
                By.CSS_SELECTOR, css_select_screenings
            ):
                # Get type
                try:
                    type_element = screening.find_element(By.CSS_SELECTOR, css_select_type)
                    type = type_element.get_attribute("textContent").strip()
                    print(f'\n🎥  {type}')
                except:
                    type = "N/A"
                    print("🎥  Failed o find type")

                # Get date and time
                try:
                    timestamp_element = screening.find_element(
                        By.CSS_SELECTOR, css_select_date
                    )
                    timestamp = timestamp_element.get_attribute("textContent")
                    split = timestamp.split(",", 1)
                    day = split[0].strip()
                    start_time = split[1].strip()
                    print(f'📅  {day} at {start_time}')
                except:
                    day = "N/A"
                    start_time = "N/A"
                    print("📅  Failed to find date")

                # Get location
                try:
                    venue_element = screening.find_element(
                        By.CSS_SELECTOR, css_select_venue
                    )
                    venue = venue_element.get_attribute("textContent").strip()
                    city_element = screening.find_element(By.CSS_SELECTOR, css_select_city)
                    city = city_element.get_attribute("textContent").strip()
                    print(f'📍  {venue} in {city}')
                except:
                    venue = "N/A"
                    city = "N/A"
                    print("📍  Failed to find venue / city")

                screeningData.append(
                    [
                        url,
                        title,
                        type,
                        day,
                        start_time,
                        venue,
                        city,
                    ]
                )

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close driver
        driver.quit()

        # Output CSVs
        timestamp = time.time()
        timestamp_formatted = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d-%H:%M:%S')
        
        csv_file_path_screenings = f'output-screenings-{timestamp_formatted}.csv'
        with open(csv_file_path_screenings, "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerows(screeningData)
        print(f'\n\n✅  CSV file "{csv_file_path_screenings}" has been created')

        csv_file_path_films = f'output-films-{timestamp_formatted}.csv'
        with open(csv_file_path_films, "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerows(filmData)
        print(f'✅  CSV file "{csv_file_path_films}" has been created')


if __name__ == "__main__":
    main()
