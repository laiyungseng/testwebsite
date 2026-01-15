import json
import datetime
from jinja2 import Environment, FileSystemLoader
from playwright.sync_api import sync_playwright

def agent_2_generate_report(analysis_json):
    """
    Takes JSON data from Agent 1 and creates a PDF report.
    """
    
    # 1. Parse the Input Data
    # In a real scenario, 'analysis_json' comes from your LLM response
    data = analysis_json 

    # 2. Setup Jinja2 Environment (The Templating Engine)
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('template.html')

    # 3. Prepare Data for Chart.js (Split into labels and values)
    # We extract lists so JavaScript can read them easily
    chart_labels = [item['name'] for item in data['metrics']]
    chart_data = [item['score'] for item in data['metrics']]

    # 4. Render the HTML (Inject data into the template)
    html_content = template.render(
        client_name=data['client_name'],
        client_url=data['client_url'],
        report_date=datetime.date.today().strftime("%B %d, %Y"),
        overall_score=data['overall_score'],
        executive_summary=data['executive_summary'],
        metrics=data['metrics'],
        chart_labels=chart_labels,
        chart_data=chart_data
    )

    # 5. Use Playwright to Print the PDF (The Headless Browser)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        # Load the rendered HTML directly
        page.set_content(html_content, wait_until="domcontentloaded")
        
        # Wait a moment to ensure fonts/charts render (even with animation off)
        page.wait_for_timeout(500) 
        
        # Print to PDF
        output_filename = f"Report_{data['client_name'].replace(' ', '_')}.pdf"
        page.pdf(
            path=rf"C:\Users\PC\Desktop\program\test website\pdf\{output_filename}",
            format="A4",
            print_background=True, # Essential for colors/gradients!
            margin={"top": "1cm", "right": "1cm", "bottom": "1cm", "left": "1cm"}
        )
        browser.close()
        
    print(f"✅ Success! Report saved as: {output_filename}")

# --- MOCK AGENT 1 OUTPUT (Testing the Pipeline) ---
# This simulates exactly what your LLM should output
mock_llm_response = {
    "client_name": "Urban Coffee Roasters",
    "client_url": "www.urbancoffee.com",
    "overall_score": 78,
    "executive_summary": "The website has a strong visual identity but suffers from significant layout shifts on mobile devices. SEO meta-tags are well implemented, but server response time is lagging.",
    "metrics": [
        {"name": "Mobile UX", "score": 65},
        {"name": "SEO Health", "score": 92},
        {"name": "Load Speed", "score": 55},
        {"name": "Accessibility", "score": 88}
    ]
}

# Run the Agent 2 function
if __name__ == "__main__":
    agent_2_generate_report(mock_llm_response)