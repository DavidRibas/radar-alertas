import os

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    docs_path = os.path.join(base_dir, 'docs', 'index.html')
    root_path = os.path.join(base_dir, 'index.html')

    for p in [docs_path, root_path]:
        with open(p, 'r', encoding='utf-8') as f:
            html = f.read()

        # 1. Actualizar el selector de pestañas en el modal de la Academia
        old_tabs_nav = """<div style="display: flex; gap: 8px; margin-bottom: 16px; border-bottom: 1px solid var(--border-glass); padding-bottom: 10px; overflow-x: auto;">
                <button class="tab-curso-btn active" id="tabCursoVideo" onclick="cambiarTabCurso('video')">🎥 Vídeo (53s)</button>
                <button class="tab-curso-btn" id="tabCursoSubastas" onclick="cambiarTabCurso('subastas')">📘 Subastas en 4 Pasos</button>
                <button class="tab-curso-btn" id="tabCursoEmpleo" onclick="cambiarTabCurso('empleo')">💼 Empleo & Vivienda</button>
            </div>"""

        new_tabs_nav = """<div style="display: flex; gap: 8px; margin-bottom: 16px; border-bottom: 1px solid var(--border-glass); padding-bottom: 10px; overflow-x: auto;">
                <button class="tab-curso-btn active" id="tabCursoSubastas" onclick="cambiarTabCurso('subastas')">👶 Subastas para Dummies (Paso a Paso)</button>
                <button class="tab-curso-btn" id="tabCursoVideo" onclick="cambiarTabCurso('video')">🎥 Vídeo Rápido (53s)</button>
                <button class="tab-curso-btn" id="tabCursoEmpleo" onclick="cambiarTabCurso('empleo')">💼 Empleo & Vivienda</button>
            </div>"""

        if old_tabs_nav in html:
            html = html.replace(old_tabs_nav, new_tabs_nav)

        # 2. Reemplazar cursoPanelSubastas con el contenido completo "Para Dummies"
        idx_panel_sub = html.find('<div id="cursoPanelSubastas"')
        assert idx_panel_sub != -1
        idx_panel_emp = html.find('<!-- Pestaña 3: Empleo & Vivienda Protegida -->', idx_panel_sub)
        assert idx_panel_emp != -1

        new_panel_dummies = """<div id="cursoPanelSubastas" class="curso-panel active" style="display: block; text-align: left;">
                <div style="background: rgba(56, 189, 248, 0.08); border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 12px; padding: 12px 14px; margin-bottom: 14px;">
                    <strong style="color: #38bdf8; font-size: 13.5px;">💡 Guía para Dummies: De Cero a Inversor sin Miedo</strong>
                    <p style="font-size: 11.5px; color: var(--text-muted); margin-top: 2px;">Olvídate de términos raros de juzgados. Esto es todo lo que necesitas saber explicado en cristiano:</p>
                </div>

                <div style="display: flex; flex-direction: column; gap: 12px; max-height: 52vh; overflow-y: auto; padding-right: 6px;">
                    <!-- Paso 1 -->
                    <div style="background: rgba(255,255,255,0.03); border: 1px solid var(--border-glass); border-radius: 12px; padding: 14px;">
                        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                            <span style="background: #38bdf8; color: #000; font-weight: 900; font-size: 11px; padding: 2px 7px; border-radius: 20px;">PASO 1</span>
                            <strong style="color: #ffffff; font-size: 13.5px;">¿Por qué hay chollos del 70%? (El Origen)</strong>
                        </div>
                        <p style="font-size: 12px; color: var(--text-muted); line-height: 1.5;">
                            Una persona o empresa debe dinero a un banco, a Hacienda o a la Seguridad Social. Si la deuda es de 40.000 € y el piso vale 160.000 €, el juez saca el piso a subasta para cobrar esos 40.000 €. <strong>No buscan hacer negocio; buscan cobrar la deuda rápido.</strong> Por eso salen a precios de risa.
                        </p>
                    </div>

                    <!-- Paso 2 -->
                    <div style="background: rgba(255,255,255,0.03); border: 1px solid var(--border-glass); border-radius: 12px; padding: 14px;">
                        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                            <span style="background: #10b981; color: #000; font-weight: 900; font-size: 11px; padding: 2px 7px; border-radius: 20px;">PASO 2</span>
                            <strong style="color: #ffffff; font-size: 13.5px;">¿Heredo las deudas del dueño? (La Regla de Oro)</strong>
                        </div>
                        <p style="font-size: 12px; color: var(--text-muted); line-height: 1.5;">
                            <span style="color: #34d399; font-weight: 700;">¡NO!</span> La ley española (<strong>Art. 674 de la LEC</strong>) obliga al juez a emitir un <em>Mandamiento Judicial de Cancelación de Cargas</em>. Es un documento oficial que ordena al Registro de la Propiedad o a la DGT <strong>borrar todas las deudas, embargos y multas anteriores</strong>. Te lo entregan limpio como una patena.
                        </p>
                    </div>

                    <!-- Paso 3 -->
                    <div style="background: rgba(255,255,255,0.03); border: 1px solid var(--border-glass); border-radius: 12px; padding: 14px;">
                        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                            <span style="background: #f59e0b; color: #000; font-weight: 900; font-size: 11px; padding: 2px 7px; border-radius: 20px;">PASO 3</span>
                            <strong style="color: #ffffff; font-size: 13.5px;">La Fianza del 5% (Tu Dinero Está Blindado)</strong>
                        </div>
                        <p style="font-size: 12px; color: var(--text-muted); line-height: 1.5;">
                            Para pujar no necesitas pagar la casa entera. Solo depositas un <strong>5% de fianza</strong> en la cuenta judicial (por ejemplo, 2.000 € en un piso de 40.000 €).<br>
                            • <strong>Si ganas:</strong> Esos 2.000 € se descuentan del precio y tienes 40 días para pagar el resto.<br>
                            • <strong>Si NO ganas:</strong> El juzgado te devuelve tus 2.000 € al 100% en 24-48 horas a tu misma cuenta bancaria. <em>Riesgo: 0 €.</em>
                        </p>
                    </div>

                    <!-- Paso 4 -->
                    <div style="background: rgba(255,255,255,0.03); border: 1px solid var(--border-glass); border-radius: 12px; padding: 14px;">
                        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                            <span style="background: #a855f7; color: #ffffff; font-weight: 900; font-size: 11px; padding: 2px 7px; border-radius: 20px;">PASO 4</span>
                            <strong style="color: #ffffff; font-size: 13.5px;">Cómo Pujar desde el Sofá con tu Móvil</strong>
                        </div>
                        <p style="font-size: 12px; color: var(--text-muted); line-height: 1.5;">
                            Ya nadie va a los juzgados. Todo se hace por internet en la web oficial <strong>subastas.boe.es</strong>:<br>
                            1. Entras con tu <strong>Cl@ve PIN o Certificado Digital</strong> (lo mismo que usas para la Renta).<br>
                            2. Metes tu IBAN para el 5% de fianza.<br>
                            3. Pones tu puja máxima. La subasta dura 20 días. Si nadie supera tu puja... ¡es tuya!
                        </p>
                    </div>

                    <!-- Paso 5 -->
                    <div style="background: rgba(255,255,255,0.03); border: 1px solid var(--border-glass); border-radius: 12px; padding: 14px;">
                        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                            <span style="background: #ec4899; color: #ffffff; font-weight: 900; font-size: 11px; padding: 2px 7px; border-radius: 20px;">PASO 5</span>
                            <strong style="color: #ffffff; font-size: 13.5px;">Las Llaves y la Posesión (Te Ahorras Notario)</strong>
                        </div>
                        <p style="font-size: 12px; color: var(--text-muted); line-height: 1.5;">
                            Al ganar, el juez te entrega el <em>Decreto de Adjudicación</em>. Este papel judicial <strong>sustituye a la escritura del notario</strong> (te ahorras los 1.000 € de notaría). Vas al Registro de la Propiedad, lo inscribes a tu nombre y el juzgado te entrega la posesión y las llaves.
                        </p>
                    </div>
                </div>
            </div>

            <!-- Pestaña 1: Vídeo Tutorial -->
            <div id="cursoPanelVideo" class="curso-panel" style="display: none;">
                <div style="position: relative; border-radius: 14px; overflow: hidden; background: #000; box-shadow: 0 8px 25px rgba(0,0,0,0.6); margin-bottom: 14px;">
                    <video id="videoTutorialPlayer" controls playsinline preload="metadata" style="width: 100%; border-radius: 14px; display: block; max-height: 55vh; object-fit: contain;">
                        <source src="assets/tutorial_radaralertas.mp4" type="video/mp4">
                        Tu navegador no soporta reproducción de vídeo HTML5.
                    </video>
                </div>
                <p style="font-size: 12px; color: var(--text-muted); text-align: center;">Aprende en menos de 1 minuto cómo se analizan y adjudican los expedientes del Estado.</p>
            </div>

            """

        html = html[:idx_panel_sub] + new_panel_dummies + html[idx_panel_emp:]

        # 3. Añadir botón en el Asistente IA para explicarlo para dummies
        old_chip_kit = """<button class="ai-chip" onclick="enviarPreguntaRapida('kit')">📦 ¿Qué incluye el Kit de 2,90 €?</button>"""
        new_chip_kit = """<button class="ai-chip" onclick="enviarPreguntaRapida('dummies')">👶 ¿Cómo funciona una subasta para dummies?</button>
                    <button class="ai-chip" onclick="enviarPreguntaRapida('kit')">📦 ¿Qué incluye el Kit de 2,90 €?</button>"""
        if old_chip_kit in html:
            html = html.replace(old_chip_kit, new_chip_kit)

        # 4. Añadir respuesta en JavaScript para 'dummies'
        old_js_fianza = "if (tipo === 'fianza') {"
        new_js_dummies = """if (tipo === 'dummies') {
                agregarMensajeChat('¿Cómo funciona una subasta paso a paso para dummies?', 'user');
                setTimeout(() => {
                    agregarMensajeChat(`
                        <p><strong>Subastas para Dummies en 4 Pasos:</strong></p>
                        <p style="margin-top:4px;">1. 🎯 <strong>El Chollo:</strong> Se subasta para cobrar una deuda, no para ganar dinero (salen hasta un -70% más baratas).</p>
                        <p style="margin-top:4px;">2. 🛡️ <strong>Sin Deudas:</strong> El juez borra todas las hipotecas o multas anteriores por ley (Art. 674 LEC).</p>
                        <p style="margin-top:4px;">3. 💰 <strong>Fianza 5%:</strong> Solo depositas el 5% para pujar. Si no ganas, te devuelven el 100% en 24-48h.</p>
                        <p style="margin-top:4px;">4. 📱 <strong>Pujas Online:</strong> Con Cl@ve desde tu móvil en subastas.boe.es sin ir a ningún juzgado.</p>
                    `);
                }, 400);
            } else if (tipo === 'fianza') {"""

        if old_js_fianza in html and "tipo === 'dummies'" not in html:
            html = html.replace(old_js_fianza, new_js_dummies)

        with open(p, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Actualizado curso para dummies en {p}")

if __name__ == '__main__':
    main()
