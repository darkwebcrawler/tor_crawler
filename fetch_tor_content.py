import subprocess
import re

def find_tor_links(content):
    # Simple regex to find links ending with .onion
    pattern = r'href=["\']?([^"\'>]*)\.onion["\']?'
    links = re.findall(pattern, content, re.IGNORECASE)
    return links

def get_tor_content(url):
    try:
        # Run torsocks curl command to fetch content
        command = ['torsocks', 'curl', '-s', url]  # -s option for silent mode
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
        
        # Decode the output from bytes to string
        content = result.stdout.decode('utf-8')
        
        # Print the fetched content
        print(f"Fetched content from {url}:")
        print(content[:5000])  # Print first 500 characters for example
        
        # Extract links ending with .onion from the fetched content
        links_ = find_tor_links(content)
        
        # Print the links ending with .onion
        print("\nLinks ending with .onion:")
        for link in links_:
            print(link)
        
        return links_, content
    
    except subprocess.CalledProcessError as e:
        print(f"Error fetching content from {url}: {e}")
        return [], ""
    except subprocess.TimeoutExpired:
        print(f"Timeout fetching content from {url}")
        return [], ""
    except Exception as e:
        print(f"An error occurred: {e}")
        return [], ""

if __name__ == "__main__":
    # URL to fetch content from
    url = "https://www.bbcnewsd73hkzno2ini43t4gblxvycyac5aw4gnv7t2rccijh7745uqd.onion/"
    
    # Call the get_tor_content function with the specified URL
    links, content = get_tor_content(url)
