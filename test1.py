import requests
from bs4 import BeautifulSoup

def print_grid_from_google_doc(url):
    """
    Fetch and parse Unicode character grid data from a Google Doc
    """
    try:
        print("Fetching document content...")
        
        # Get HTML content
        response = requests.get(url)
        response.raise_for_status()
        
        print("Document fetched successfully, parsing...")
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find tables
        tables = soup.find_all('table')
        if not tables:
            print("No tables found")
            return
        
        data = []
        max_x = 0
        max_y = 0
        
        for table in tables:
            rows = table.find_all('tr')
            
            for row_idx, row in enumerate(rows):
                cells = row.find_all(['td', 'th'])
                if len(cells) < 3:
                    continue
                
                # Correct column order: x-coordinate, character, y-coordinate
                x_cell = cells[0].get_text(strip=True)
                char_cell = cells[1].get_text(strip=True)
                y_cell = cells[2].get_text(strip=True)
                
                # Skip header row
                if row_idx == 0 and ('x' in x_cell.lower() or 'y' in y_cell.lower()):
                    print("Skipping header row")
                    continue
                
                # Try to parse coordinates
                try:
                    x = int(x_cell)
                    y = int(y_cell)
                    
                    data.append((char_cell, x, y))
                    max_x = max(max_x, x)
                    max_y = max(max_y, y)
                    
                    print(f"Found data point: '{char_cell}' at ({x}, {y})")
                    
                except ValueError:
                    print(f"Skipping invalid coordinate row: {x_cell}, {char_cell}, {y_cell}")
                    continue
        
        print(f"\nTotal data points found: {len(data)}")
        
        if not data:
            print("No valid data found")
            return
        
        # Create and print grid
        create_and_print_grid(data, max_x, max_y)
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

def create_and_print_grid(data, max_x, max_y):
    """Create and print the grid"""
    # Create grid
    grid = [[' '] * (max_x + 1) for _ in range(max_y + 1)]
    
    # Fill grid
    for char, x, y in data:
        if 0 <= y <= max_y and 0 <= x <= max_x:
            grid[y][x] = char
    
    print(f"\nGrid dimensions: {max_x + 1} (width) x {max_y + 1} (height)")
    print("Generated grid (correct orientation):")
    print("+" + "-" * (max_x + 1) + "+")
    
    # Reverse y-axis direction so y=0 is at the bottom
    for y in range(max_y, -1, -1):
        print('|' + ''.join(grid[y]) + '|')
    
    print("+" + "-" * (max_x + 1) + "+")
    
    # Also print without borders
    print("\nPlain text version:")
    for y in range(max_y, -1, -1):
        print(''.join(grid[y]))

# Run main function
url = "https://docs.google.com/document/d/e/2PACX-1vRPzbNQcx5UriHSbZ-9vmsTow_R6RRe7eyAU60xIF9Dlz-vaHiHNO2TKgDi7jy4ZpTpNqM7EvEcfr_p/pub"
print_grid_from_google_doc(url)