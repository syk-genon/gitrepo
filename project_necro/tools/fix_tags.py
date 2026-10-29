with open('project_necro/display.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('src="display_data.js"', 'src="display_data.js?v=7"')
text = text.replace('src="display.js"', 'src="display.js?v=7"')

with open('project_necro/display.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("HTML script tags updated to ?v=7")
