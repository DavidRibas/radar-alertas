import json
import os

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    json_path = os.path.join(base_dir, 'docs', 'data', 'oportunidades.json')
    docs_path = os.path.join(base_dir, 'docs', 'index.html')
    root_path = os.path.join(base_dir, 'index.html')

    with open(json_path, 'r', encoding='utf-8') as f:
        items = json.load(f)

    img_map = {
        'VPO-VIVE-2026-MAD01': 'assets/templates/vpo_edificio_moderno.jpg',
        'VPO-EMVS-2026-MAD02': 'assets/templates/vpo_ensanche_residencial.jpg',
        'VPO-HBCN-2026-BCN01': 'assets/templates/inmueble_eixample_bcn.jpg',
        'DEC-PNSD-2026-PORSCHE': 'assets/templates/porsche_macan_decomiso.jpg',
        'DEC-PNSD-2026-MERCEDES': 'assets/templates/mercedes_coupe_decomiso.jpg',
        'DEC-PNSD-2026-BARCO': 'assets/templates/barco_yate_decomiso.jpg'
    }

    for it in items:
        if it['id'] in img_map:
            it['img'] = img_map[it['id']]

    # Guardar en json
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

    # Inyectar en docs/index.html e index.html
    json_str = json.dumps(items, ensure_ascii=False, indent=8)

    for path in [docs_path, root_path]:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        start_tag = 'let OPORTUNIDADES = ['
        idx_start = content.find(start_tag)
        assert idx_start != -1, f'start_tag not found in {path}'

        idx_end = content.find('];', idx_start)
        assert idx_end != -1, f'closing bracket not found in {path}'

        new_content = content[:idx_start] + 'let OPORTUNIDADES = ' + json_str + content[idx_end+1:]

        with open(path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f'Actualizado {path} con imágenes verificadas.')

if __name__ == '__main__':
    main()
