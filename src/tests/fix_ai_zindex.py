import os

for path in ['docs/index.html', 'index.html']:
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    html = html.replace('.ai-assistant-wrapper {\n            position: fixed;\n            bottom: 24px;\n            right: 24px;\n            z-index: 999;',
                        '.ai-assistant-wrapper {\n            position: fixed;\n            bottom: 24px;\n            right: 24px;\n            z-index: 10002;')
    
    html = html.replace('.ai-assistant-wrapper {\n                bottom: 80px;\n                right: 14px;\n            }',
                        '.ai-assistant-wrapper {\n                bottom: 95px;\n                right: 14px;\n                z-index: 10002;\n            }')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Fixed z-index and bottom in {path}")
