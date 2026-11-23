import os

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    docs_path = os.path.join(base_dir, 'docs', 'index.html')
    root_path = os.path.join(base_dir, 'index.html')

    old_fn = '''        function aplicarFiltroRapido(tipo) {
            if (filtroRapidoActual === tipo) {
                limpiarFiltrosRapidos();
                return;
            }
            filtroRapidoActual = tipo;
            document.querySelectorAll('.chip-btn').forEach(b => b.classList.remove('active'));
            const btnLimpiar = document.getElementById('btnLimpiarChips');
            if (btnLimpiar) btnLimpiar.style.display = 'inline-flex';

            if (tipo === 'bolsas') {
                const btn = document.getElementById('chipBolsas');
                if (btn) btn.classList.add('active');
                categoriaActual = 'empleo';
                actualizarTabsUI('empleo');
            } else if (tipo === 'coches_baratos') {
                const btn = document.getElementById('chipCoches');
                if (btn) btn.classList.add('active');
                categoriaActual = 'vehiculo';
                actualizarTabsUI('vehiculo');
            } else if (tipo === 'descuento_top') {
                const btn = document.getElementById('chipDescuentos');
                if (btn) btn.classList.add('active');
                categoriaActual = 'all';
                actualizarTabsUI('all');
            }
            filtrarOportunidades();
        }'''

    new_fn = '''        function aplicarFiltroRapido(tipo) {
            if (filtroRapidoActual === tipo) {
                limpiarFiltrosRapidos();
                return;
            }
            filtroRapidoActual = tipo;
            document.querySelectorAll('.chip-btn').forEach(b => b.classList.remove('active'));
            const btnLimpiar = document.getElementById('btnLimpiarChips');
            if (btnLimpiar) btnLimpiar.style.display = 'inline-flex';

            if (tipo === 'alquiler_vpo') {
                const btn = document.getElementById('chipVpo');
                if (btn) btn.classList.add('active');
                categoriaActual = 'vivienda';
                actualizarTabsUI('vivienda');
            } else if (tipo === 'decomisos_lujo') {
                const btn = document.getElementById('chipDecomisos');
                if (btn) btn.classList.add('active');
                categoriaActual = 'vehiculo';
                actualizarTabsUI('vehiculo');
            } else if (tipo === 'bolsas') {
                const btn = document.getElementById('chipBolsas');
                if (btn) btn.classList.add('active');
                categoriaActual = 'empleo';
                actualizarTabsUI('empleo');
            } else if (tipo === 'descuento_top') {
                const btn = document.getElementById('chipDescuentos');
                if (btn) btn.classList.add('active');
                categoriaActual = 'all';
                actualizarTabsUI('all');
            }
            filtrarOportunidades();
        }'''

    for path in [docs_path, root_path]:
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()
        assert old_fn in c, f'old_fn not found in {path}'
        c = c.replace(old_fn, new_fn)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c)

    print('aplicarFiltroRapido updated successfully in both files')

if __name__ == '__main__':
    main()
