import time  # To add delays for page loading
from selenium import webdriver  # To interact with the browser and automate the process
from selenium.webdriver.chrome.service import Service  # To manage the ChromeDriver service
from selenium.webdriver.chrome.options import Options  # To set up browser options, like headless mode
from selenium.webdriver.common.by import By  # For finding elements using various locators (XPath, tag name, etc.)
from webdriver_manager.chrome import ChromeDriverManager  # To manage and download the correct ChromeDriver


# The URL of the Google document with the data we want to scrape
url = "https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub"

# Setting up Chrome options for headless mode (no UI)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Running the browser in the background without opening a window

# Creating the Chrome driver service, using ChromeDriverManager to ensure we have the correct driver version
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)  # Initiating the browser with the specified options


# Define the function to scrape the Google Doc and parse the table data
def parse_google_doc(url):
    driver.get(url)  # Navigate to the URL
    time.sleep(5)  # Wait for the page to load completely (can be adjusted based on the page's loading time)
    
    # Finding all the rows in the table using XPath
    rows = driver.find_elements(By.XPATH, '//*[@id="contents"]/div/table/tbody/tr')
    
    grid = []  # Initialize an empty list to represent the grid for placing block characters

    # These will store the maximum x and y coordinates found in the table, to determine the grid's size
    max_x = 0  
    max_y = 0

    # Loop through each row, starting from the second row (index 1), skipping the header
    for row in rows[1:]:  # We skip the first row (index 0) as it is the header or irrelevant
        columns = row.find_elements(By.TAG_NAME, 'td')  # Get the table cells in each row
        
        x = int(columns[0].text.strip())  # Extract the x-coordinate from the first cell (convert to integer)
        y = int(columns[2].text.strip())  # Extract the y-coordinate from the third cell (convert to integer)
        block_char = columns[1].text.strip()  # Extract the block character (█ or ▀) from the second cell

        # Update the maximum x and y values for grid dimensions
        max_x = max(max_x, x)  # Track the largest x-coordinate
        max_y = max(max_y, y)  # Track the largest y-coordinate

        # Extend the grid if necessary to fit the current y-coordinate
        while len(grid) <= y:
            grid.append([])  # Add a new row if there are not enough rows yet
        
        # Extend the row to fit the current x-coordinate
        while len(grid[y]) <= x:
            grid[y].append(" ")  # Add empty space to the row if it's not wide enough

        # Place the block character at the specified (x, y) coordinates
        grid[y][x] = block_char

    # Print two newlines for separation before the grid
    print("\n" * 2)

    # Loop through the rows of the grid in reverse (to print from top to bottom)
    for row in range(max_y + 1):
        print("".join(grid[max_y - row][:max_x + 1]))  # Join the cells in each row and print it as a string


# Call the function to parse the Google Doc and print the grid
parse_google_doc(url)

# Add a couple of newlines after the output for better readability
print("\n" * 2)

# Quit the browser after the task is complete
driver.quit()
