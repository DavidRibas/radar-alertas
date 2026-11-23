import json
import os

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    json_path = os.path.join(base_dir, 'docs', 'data', 'oportunidades.json')
    docs_path = os.path.join(base_dir, 'docs', 'index.html')
    root_path = os.path.join(base_dir, 'index.html')

    with open(json_path, 'r', encoding='utf-8') as f:
        items = json.load(f)

    json_str = json.dumps(items, ensure_ascii=False, indent=8)

    for path in [docs_path, root_path]:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        start_tag = 'let OPORTUNIDADES = ['
        idx_start = content.find(start_tag)
        assert idx_start != -1, f'start_tag not found in {path}'

        # find closing bracket of OPORTUNIDADES
        idx_end = content.find('];', idx_start)
        assert idx_end != -1, f'closing bracket not found in {path}'

        new_content = content[:idx_start] + 'let OPORTUNIDADES = ' + json_str + content[idx_end+1:]

        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f'Sincronizado {path} con éxito ({len(items)} oportunidades).')

if __name__ == '__main__':
    main()
