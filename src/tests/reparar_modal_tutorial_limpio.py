import os

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    docs_path = os.path.join(base_dir, 'docs', 'index.html')
    root_path = os.path.join(base_dir, 'index.html')

    clean_modal_tutorial = """<div class="modal-overlay" id="modalTutorial">
        <div class="modal-box" style="max-width: 580px; max-height: 90vh; overflow-y: auto; padding: 24px; border-color: rgba(56, 189, 248, 0.4); box-shadow: 0 0 50px rgba(0,0,0,0.8);">
            <button class="modal-close" onclick="cerrarModalTutorial()">✕</button>
            <div class="modal-header" style="margin-bottom: 16px;">
                <div style="font-size: 13px; font-weight: 800; color: #38bdf8; letter-spacing: 1px; text-transform: uppercase;">🎓 ACADEMIA RADARALERTAS</div>
                <h3 class="modal-title" style="font-size: 22px; margin-top: 4px;">Mini-Curso Rápido de Inversión</h3>
                <p class="modal-sub">Aprende a cazar oportunidades oficiales sin intermediarios y con riesgo cero</p>
            </div>

            <!-- Selector de Pestañas del Mini-Curso -->
            <div style="display: flex; gap: 8px; margin-bottom: 16px; border-bottom: 1px solid var(--border-glass); padding-bottom: 10px; overflow-x: auto;">
                <button class="tab-curso-btn active" id="tabCursoSubastas" onclick="cambiarTabCurso('subastas')">👶 Subastas para Dummies</button>
                <button class="tab-curso-btn" id="tabCursoVideo" onclick="cambiarTabCurso('video')">🎥 Vídeos Tutoriales (2)</button>
                <button class="tab-curso-btn" id="tabCursoEmpleo" onclick="cambiarTabCurso('empleo')">💼 Empleo & Vivienda</button>
            </div>

            <!-- Pestaña 1: Guía Subastas para Dummies (Paso a Paso) -->
            <div id="cursoPanelSubastas" class="curso-panel active" style="display: block; text-align: left;">
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

            <!-- Pestaña 2: Vídeos Tutoriales Oficiales (Selector 2 Vídeos) -->
            <div id="cursoPanelVideo" class="curso-panel" style="display: none;">
                <!-- Selector de los 2 Vídeos -->
                <div style="display: flex; gap: 8px; justify-content: center; margin-bottom: 12px; overflow-x: auto;">
                    <button class="pill-video-sel active" id="btnSelVideoDummies" onclick="cambiarVideoTutorial('dummies')">
                        👶 Vídeo 1: Cómo Pujar en el BOE (60s)
                    </button>
                    <button class="pill-video-sel" id="btnSelVideoWeb" onclick="cambiarVideoTutorial('web')">
                        🌐 Vídeo 2: Cómo Funciona la Web (53s)
                    </button>
                </div>

                <div style="position: relative; border-radius: 14px; overflow: hidden; background: #000; box-shadow: 0 8px 25px rgba(0,0,0,0.6); margin-bottom: 12px;">
                    <video id="videoTutorialPlayer" controls playsinline preload="metadata" style="width: 100%; border-radius: 14px; display: block; max-height: 52vh; object-fit: contain;">
                        <source id="videoPlayerSource" src="assets/tutorial_dummies_paso_a_paso.mp4" type="video/mp4">
                        Tu navegador no soporta reproducción de vídeo HTML5.
                    </video>
                </div>
                <p id="videoTutorialDesc" style="font-size: 12px; color: #38bdf8; text-align: center; font-weight: 700;">
                    Tutorial Paso a Paso para Dummies: Cómo proceder en el BOE una vez que tienes la información.
                </p>
            </div>

            <!-- Pestaña 3: Empleo & Vivienda Protegida -->
            <div id="cursoPanelEmpleo" class="curso-panel" style="display: none; text-align: left;">
                <div style="display: flex; flex-direction: column; gap: 12px; max-height: 55vh; overflow-y: auto; padding-right: 6px;">
                    <div style="background: rgba(255,255,255,0.03); border: 1px solid var(--border-glass); border-radius: 10px; padding: 12px;">
                        <strong style="color: #38bdf8; font-size: 13px;">💼 Bolsas Sin Oposición (Concurso de Méritos)</strong>
                        <p style="font-size: 12px; color: var(--text-muted); margin-top: 3px;">
                            Los ministerios publican plazas de personal laboral fijo y temporal donde no hay examen memorístico. La admisión se basa en tu titulación, carnet o experiencia previa.
                        </p>
                    </div>
                    <div style="background: rgba(255,255,255,0.03); border: 1px solid var(--border-glass); border-radius: 10px; padding: 12px;">
                        <strong style="color: #10b981; font-size: 13px;">🏠 Alquiler Asequible Plan VIVE y EMVS (Desde 400 €)</strong>
                        <p style="font-size: 12px; color: var(--text-muted); margin-top: 3px;">
                            Son viviendas protegidas de obra nueva con precios regulados por la administración pública. El requisito principal es no superar los límites de ingresos de la unidad familiar (IPREM).
                        </p>
                    </div>
                </div>
            </div>

            <div style="margin-top: 18px; padding-top: 14px; border-top: 1px solid var(--border-glass); display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 12px; color: var(--text-muted);">¿Quieres auditar una oportunidad real?</span>
                <button onclick="cerrarModalTutorial(); window.location.hash='#catalogo';" style="background: linear-gradient(135deg, #059669, #10b981); color: #ffffff; border: none; padding: 8px 16px; border-radius: 8px; font-weight: 700; font-size: 12px; cursor: pointer;">
                    Ver Catálogo Auditado →
                </button>
            </div>
        </div>
    </div>\n\n    """

    for file_p in [docs_path, root_path]:
        with open(file_p, 'r', encoding='utf-8') as f:
            content = f.read()
        
        p_start = content.find('<div class="modal-overlay" id="modalTutorial">')
        assert p_start != -1
        p_end = content.find('<!-- Modal de Desbloqueo de Expediente Individual -->')
        assert p_end != -1
        
        new_content = content[:p_start] + clean_modal_tutorial + content[p_end:]
        with open(file_p, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Reparado con éxito: {file_p}")

if __name__ == '__main__':
    main()
