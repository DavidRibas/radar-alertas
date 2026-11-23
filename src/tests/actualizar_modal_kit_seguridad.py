import os

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    docs_path = os.path.join(base_dir, 'docs', 'index.html')
    root_path = os.path.join(base_dir, 'index.html')

    for p in [docs_path, root_path]:
        with open(p, 'r', encoding='utf-8') as f:
            html = f.read()

        idx_start = html.find('<div class="modal-overlay" id="modalUnlock">')
        assert idx_start != -1, f"modalUnlock not found in {p}"
        idx_end = html.find('<!-- Modal del Plan PRO Inversor -->', idx_start)
        assert idx_end != -1, f"modalPro comment not found in {p}"

        new_modal_html = """<div class="modal-overlay" id="modalUnlock">
        <div class="modal-box" style="max-width: 490px;">
            <button class="modal-close" onclick="cerrarModales()">✕</button>
            <div class="modal-header">
                <div class="modal-icon">🛡️</div>
                <h3 class="modal-title">Kit Completo de Seguridad Oficial</h3>
                <p class="modal-sub">Todo lo que necesitas para participar desde tu móvil sin intermediarios ni riesgos</p>
            </div>

            <div class="modal-item-info">
                <div class="modal-item-thumb" id="modalItemImg"></div>
                <div class="modal-item-details">
                    <div class="modal-item-name" id="modalItemTitle">Piso en Las Rozas (Madrid)</div>
                    <div class="modal-item-meta" id="modalItemMeta">Salida: 116.956 € • Ahorro: +272.000 €</div>
                </div>
            </div>

            <!-- Entregables Claros de Alto Valor: Los 3 Pasos Anti-Riesgo -->
            <div class="modal-deliverables-box" style="background: rgba(255,255,255,0.03); border: 1px solid var(--border-glass); border-radius: 12px; padding: 14px; margin: 16px 0; text-align: left; display: flex; flex-direction: column; gap: 12px;">
                <div style="display: flex; gap: 10px; align-items: flex-start;">
                    <span style="font-size: 20px; line-height: 1;">📄</span>
                    <div>
                        <strong style="font-size: 13px; color: var(--text-main); display: block;">1. ANTES: Informe Pericial de Cargas</strong>
                        <p style="font-size: 11.5px; color: var(--text-muted); margin-top: 2px;">Verificación de cargas 0,00 €, IBI y situación jurídica auditada (Art. 674 LEC) para comprar sin trampas.</p>
                    </div>
                </div>
                <div style="display: flex; gap: 10px; align-items: flex-start;">
                    <span style="font-size: 20px; line-height: 1;">📱</span>
                    <div>
                        <strong style="font-size: 13px; color: var(--text-main); display: block;">2. DURANTE: Guía Visual "Pujar con Cl@ve"</strong>
                        <p style="font-size: 11.5px; color: var(--text-muted); margin-top: 2px;">Tutorial paso a paso con capturas para participar en 3 minutos desde el móvil sin gestorías.</p>
                    </div>
                </div>
                <div style="display: flex; gap: 10px; align-items: flex-start;">
                    <span style="font-size: 20px; line-height: 1;">🛡️</span>
                    <div>
                        <strong style="font-size: 13px; color: var(--text-main); display: block;">3. DESPUÉS: Garantía de Devolución del 5%</strong>
                        <p style="font-size: 11.5px; color: var(--text-muted); margin-top: 2px;">Plantilla legal oficial (Art. 652 LEC) para que el juzgado te devuelva el 100% de la fianza si no ganas.</p>
                    </div>
                </div>
            </div>

            <!-- Sello de Garantía 100% -->
            <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.35); border-radius: 10px; padding: 10px 14px; margin-bottom: 16px; font-size: 11.5px; color: #34d399; text-align: left; display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 16px;">🛡️</span>
                <span><strong>Garantía de Devolución 100%:</strong> Si el expediente no está activo en la sede oficial, te reembolsamos tus 2,90 € al instante.</span>
            </div>

            <a href="https://buy.stripe.com/5kQaEYd2S2Bd5OvfnfcQU02" target="_blank" class="btn-pay-single" style="text-decoration:none; display:flex; align-items:center; justify-content:center; gap:8px;">
                <span>🔓 Desbloquear Kit Completo • 2,90 €</span>
                <span>➔</span>
            </a>

            <!-- Métodos de Pago Apple Pay / Google Pay / Tarjeta -->
            <div style="display: flex; justify-content: center; align-items: center; gap: 12px; margin-top: 12px; font-size: 11px; color: #94a3b8;">
                <span>💳 Tarjeta</span>
                <span>🍎 Apple Pay</span>
                <span>⚡ Google Pay</span>
                <span style="color:#10b981;">🔒 Stripe SSL 256-bit</span>
            </div>

            <div class="modal-upsell-pro">
                <span>¿Buscas varias convocatorias o subastas al mes?</span>
                <a onclick="cerrarModales(); abrirModalPro();">⭐ Activa el Plan PRO Inversor por solo 14,99 €/mes (Desbloqueo ilimitado)</a>
            </div>
        </div>
    </div>

    """

        html = html[:idx_start] + new_modal_html + html[idx_end:]
        with open(p, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Actualizado modal en {p}")

if __name__ == '__main__':
    main()
