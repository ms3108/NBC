import requests
from flask import Flask, render_template, request
from doc import documents

app = Flask(__name__)

# Dictionary to store rule titles and links
rules_data = {}

# Convert Google Docs links to exportable text format
def convert_to_rules_data(documents):
    for doc in documents:
        # Replace "/edit" at the end of each link with "/export?format=txt"
        export_link = doc['link'].replace('/edit', '/export?format=txt')
        rules_data[doc['title']] = export_link
    return rules_data

# Convert the list of dictionaries to the desired format
rules_data = convert_to_rules_data(documents)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/calc')
def calc():
    return render_template('calc.html')


@app.route('/content')
def content():
    # Pass rules_data to the template
    return render_template('content.html', rules=rules_data)


@app.route('/rule/<rule_id>')
def rule_content(rule_id):
    # Get the corresponding export link from rules_data based on the rule_id
    rule_url = rules_data.get(rule_id)

    if rule_url:
        # Pass the link to the template
        return render_template('rule.html', rule_id=rule_id, rule_url=rule_url)
    else:
        return "Rule not found", 404


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').lower()
    results = {key: value for key, value in rules_data.items() if query in key.lower()}
    return render_template('index.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)
