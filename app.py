import requests

from flask import Flask, render_template,request
from doc import documents



app = Flask(__name__)

def convert_to_rules_data(documents):
    rules_data = {}
    for doc in documents:
        # Replace "/edit" at the end of each link with "/export?format=txt"
        export_link = doc['link'].replace('/edit', '/export?format=txt')
        rules_data[doc['title']] = export_link
    return rules_data

# Convert the list of dictionaries to the desired format
rules_data = convert_to_rules_data(documents)
print(f"Number of rules: {len(rules_data)}")  # This should match the length of the documents list



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calc')
def calc():
    return render_template('calc.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').lower()
    results = {key: value for key, value in rules_data.items() if query in key.lower()}
    return render_template('index.html', results=results)


@app.route('/rule/<rule_id>')
def rule_content(rule_id):
    # Get the corresponding link from rules_data based on rule_id
    link = rules_data.get(rule_id)

    if link:
        response = requests.get(link)
        if response.status_code == 200:
            content = response.text  # Get content as plain text
        else:
            content = "Failed to retrieve content."
    else:
        content = "Rule not found."

    return render_template('rule.html', content=content, title=rule_id)




@app.route('/content')
def content():
    return render_template('content.html', rules=rules_data)



if __name__ == '__main__':
   app.run(debug=True)