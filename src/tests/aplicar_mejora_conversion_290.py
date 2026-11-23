import json
import os

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    json_path = os.path.join(base_dir, 'docs', 'data', 'oportunidades.json')
    docs_path = os.path.join(base_dir, 'docs', 'index.html')
    root_path = os.path.join(base_dir, 'index.html')

    # 1. Configurar Las Rozas como Muestra Gratuita Desbloqueada
    with open(json_path, 'r', encoding='utf-8') as f:
        items = json.load(f)

    for it in items:
        if it['id'] == 'INM-SUB-AT-2026-23R2886001483':
            it['desbloqueado'] = True
            it['pdfMuestra'] = 'assets/Dictamen_Verificado_Final.pdf'
            it['badgeVisual'] = '🔓 MUESTRA GRATUITA DESBLOQUEADA'
            it['tag'] = 'MUESTRA AUDITADA GRATIS'
            it['tagClass'] = 'tag-directa'
            it['ctaLabel'] = '📄 Descargar Dictamen Oficial (PDF Gratis)'
            print('Configurada oportunidad de muestra gratuita:', it['id'])
            break

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

    # 2. Actualizar docs/index.html y root index.html
    for path in [docs_path, root_path]:
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()

        # Inyectar OPORTUNIDADES en el HTML
        json_str = json.dumps(items, ensure_ascii=False, indent=8)
        start_tag = 'let OPORTUNIDADES = ['
        idx_start = html.find(start_tag)
        assert idx_start != -1
        idx_end = html.find('];', idx_start)
        assert idx_end != -1
        html = html[:idx_start] + 'let OPORTUNIDADES = ' + json_str + html[idx_end+1:]

        # 3. Actualizar plantilla de tarjeta dentro de filtrarOportunidades
        idx_lock_start = html.find('<!-- Candado de Expediente -->')
        assert idx_lock_start != -1, 'lock start not found'
        idx_lock_end = html.find('</article>', idx_lock_start)
        assert idx_lock_end != -1, 'lock end not found'
        # find closing div of lock-box right before button.btn-share-wa
        idx_share_wa = html.find('<button class="btn-share-wa"', idx_lock_start)
        assert idx_share_wa != -1, 'share wa not found'

        new_lock_box = '''<!-- Candado de Expediente -->
                        <div class="lock-box" style="${item.desbloqueado ? 'border-color: rgba(16,185,129,0.5); background: rgba(16,185,129,0.06);' : ''}">
                            <div class="lock-header">
                                <div class="lock-title-wrap">
                                    <span>${item.desbloqueado ? '🔓' : '🔒'}</span>
                                    <span>${item.desbloqueado ? 'Expediente Oficial de Muestra Desbloqueado' : 'Dictamen Pericial y Expediente Oficial'}</span>
                                </div>
                                <span class="lock-badge" style="${item.desbloqueado ? 'background:rgba(16,185,129,0.25); color:#34d399; border-color:rgba(16,185,129,0.5); font-weight:800;' : ''}">
                                    ${item.desbloqueado ? 'MUESTRA GRATIS' : '2,90 €'}
                                </span>
                            </div>

                            <div class="lock-data-preview">
                                ${item.desbloqueado ? `
                                    <span style="color:#34d399; font-weight:700;">Expediente: ${item.expedienteReal}</span>
                                    <span style="color:#94a3b8;">Estado: Auditoría legal completa con Dictamen Oficial en PDF</span>
                                ` : `
                                    <span>Expediente: EXP-••••••••••••• (Oculto)</span>
                                    <span>Entrega: Dictamen en PDF + Plantilla tramitada + Enlace directo</span>
                                `}
                            </div>

                            <div class="lock-actions">
                                ${item.desbloqueado ? `
                                    <a href="${item.pdfMuestra || 'assets/Dictamen_Verificado_Final.pdf'}" download class="btn-unlock-single" style="text-decoration:none; background: linear-gradient(135deg, #059669, #10b981); display:flex; align-items:center; justify-content:center; gap:8px;">
                                        <span>📄 Descargar Dictamen Oficial en PDF (Muestra Gratis)</span>
                                    </a>
                                    <a href="${item.enlaceBoeReal}" target="_blank" class="btn-unlock-pro-link" style="color:#38bdf8; text-decoration:none; text-align:center; display:block;">
                                        🚀 Acceder a la Sede Oficial Directa →
                                    </a>
                                ` : `
                                    <button class="btn-unlock-single" onclick="abrirModalDesbloqueo('${item.id}')">
                                        <span>📄 ${ctaBtnText}</span>
                                    </button>
                                    <button class="btn-unlock-pro-link" onclick="abrirModalPro()">
                                        ⭐ O accede sin límites con el Plan PRO (14,99 €/mes)
                                    </button>
                                `}
                            </div>
                        </div>
                        '''

        html = html[:idx_lock_start] + new_lock_box + html[idx_share_wa:]

        # 4. Actualizar modalUnlock
        idx_modal_start = html.find('<div class="modal-overlay" id="modalUnlock">')
        assert idx_modal_start != -1, 'modalUnlock not found'
        idx_modal_next = html.find('<!-- Modal del Plan PRO Inversor -->', idx_modal_start)
        assert idx_modal_next != -1, 'modalPro comment not found'

        new_modal_unlock = '''<div class="modal-overlay" id="modalUnlock">
        <div class="modal-box" style="max-width: 490px;">
            <button class="modal-close" onclick="cerrarModales()">✕</button>
            <div class="modal-header">
                <div class="modal-icon">📄</div>
                <h3 class="modal-title">Dictamen Pericial Oficial + Expediente</h3>
                <p class="modal-sub">Descarga inmediata del Informe Técnico en PDF y acceso a la sede oficial</p>
            </div>

            <div class="modal-item-info">
                <div class="modal-item-thumb" id="modalItemImg"></div>
                <div class="modal-item-details">
                    <div class="modal-item-name" id="modalItemTitle">Piso en Las Rozas (Madrid)</div>
                    <div class="modal-item-meta" id="modalItemMeta">Salida: 116.956 € • Ahorro: +272.000 €</div>
                </div>
            </div>

            <!-- Entregables Claros de Alto Valor -->
            <div class="modal-deliverables-box" style="background: rgba(255,255,255,0.03); border: 1px solid var(--border-glass); border-radius: 12px; padding: 14px; margin: 16px 0; text-align: left;">
                <div style="display: flex; gap: 10px; margin-bottom: 10px; align-items: flex-start;">
                    <span style="font-size: 18px;">📑</span>
                    <div>
                        <strong style="font-size: 13px; color: var(--text-main);">Dictamen Pericial de Cargas en PDF</strong>
                        <p style="font-size: 11.5px; color: var(--text-muted); margin-top: 2px;">Certificado de cargas 0,00 € (Art. 674 LEC) y situación jurídica auditada.</p>
                    </div>
                </div>
                <div style="display: flex; gap: 10px; margin-bottom: 10px; align-items: flex-start;">
                    <span style="font-size: 18px;">📝</span>
                    <div>
                        <strong style="font-size: 13px; color: var(--text-main);">Plantilla Oficial y Guía Paso a Paso</strong>
                        <p style="font-size: 11.5px; color: var(--text-muted); margin-top: 2px;">Instrucciones para presentar la solicitud o puja sin errores y no quedar excluido.</p>
                    </div>
                </div>
                <div style="display: flex; gap: 10px; align-items: flex-start;">
                    <span style="font-size: 18px;">🔗</span>
                    <div>
                        <strong style="font-size: 13px; color: var(--text-main);">Acceso Directo a la Sede Oficial del Estado</strong>
                        <p style="font-size: 11.5px; color: var(--text-muted); margin-top: 2px;">Enlace telemático oficial sin comisiones de agencias ni intermediarios.</p>
                    </div>
                </div>
            </div>

            <!-- Sello de Garantía 100% -->
            <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.35); border-radius: 10px; padding: 10px 14px; margin-bottom: 16px; font-size: 11.5px; color: #34d399; text-align: left; display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 16px;">🛡️</span>
                <span><strong>Garantía de Autenticidad 100%:</strong> Si los datos no proceden del Boletín Oficial del Estado o sede pública oficial, te reembolsamos tus 2,90 € al instante.</span>
            </div>

            <a href="https://buy.stripe.com/5kQaEYd2S2Bd5OvfnfcQU02" target="_blank" class="btn-pay-single" style="text-decoration:none; display:flex; align-items:center; justify-content:center; gap:8px;">
                <span>Descargar Dictamen y Expediente • 2,90 €</span>
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

    '''

        html = html[:idx_modal_start] + new_modal_unlock + html[idx_modal_next:]

        # 5. CSS en modo claro para deliverables
        extra_modal_css = '''
        body.theme-light .modal-deliverables-box {
            background: #f8fafc !important;
            border-color: #e2e8f0 !important;
        }
        body.theme-light .modal-deliverables-box strong {
            color: #0f172a !important;
        }
        body.theme-light .modal-deliverables-box p {
            color: #64748b !important;
        }
'''
        if 'body.theme-light .modal-deliverables-box' not in html:
            idx_style = html.find('</style>')
            assert idx_style != -1
            html = html[:idx_style] + extra_modal_css + '\n    ' + html[idx_style:]

        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f'Actualizado {path} con muestra gratuita y nuevo modal de conversión.')

if __name__ == '__main__':
    main()
