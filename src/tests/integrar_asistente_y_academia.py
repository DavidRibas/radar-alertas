import os

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    docs_path = os.path.join(base_dir, 'docs', 'index.html')
    root_path = os.path.join(base_dir, 'index.html')

    for p in [docs_path, root_path]:
        with open(p, 'r', encoding='utf-8') as f:
            html = f.read()

        # 1. Actualizar texto del enlace en el navbar
        old_nav_link = '<a href="javascript:void(0)" onclick="abrirModalTutorial()" class="nav-link" style="color: #38bdf8;">▶ Vídeo Tutorial</a>'
        new_nav_link = '<a href="javascript:void(0)" onclick="abrirModalTutorial()" class="nav-link" style="color: #38bdf8; font-weight: 700;">🎓 Mini-Curso & Guías</a>'
        if old_nav_link in html:
            html = html.replace(old_nav_link, new_nav_link)

        # 2. Actualizar modalTutorial para convertirlo en la Academia con 3 pestañas
        idx_mod_tut_start = html.find('<div class="modal-overlay" id="modalTutorial">')
        assert idx_mod_tut_start != -1, f"modalTutorial not found in {p}"
        idx_mod_tut_end = html.find('</div>\n    </div>', idx_mod_tut_start) + 17

        new_modal_tutorial = """<div class="modal-overlay" id="modalTutorial">
        <div class="modal-box" style="max-width: 580px; padding: 24px; border-color: rgba(56, 189, 248, 0.4); box-shadow: 0 0 50px rgba(0,0,0,0.8);">
            <button class="modal-close" onclick="cerrarModalTutorial()">✕</button>
            <div class="modal-header" style="margin-bottom: 16px;">
                <div style="font-size: 13px; font-weight: 800; color: #38bdf8; letter-spacing: 1px; text-transform: uppercase;">🎓 ACADEMIA RADARALERTAS</div>
                <h3 class="modal-title" style="font-size: 22px; margin-top: 4px;">Mini-Curso Rápido de Inversión</h3>
                <p class="modal-sub">Aprende a cazar oportunidades oficiales sin intermediarios y con riesgo cero</p>
            </div>

            <!-- Selector de Pestañas del Mini-Curso -->
            <div style="display: flex; gap: 8px; margin-bottom: 16px; border-bottom: 1px solid var(--border-glass); padding-bottom: 10px; overflow-x: auto;">
                <button class="tab-curso-btn active" id="tabCursoVideo" onclick="cambiarTabCurso('video')">🎥 Vídeo (53s)</button>
                <button class="tab-curso-btn" id="tabCursoSubastas" onclick="cambiarTabCurso('subastas')">📘 Subastas en 4 Pasos</button>
                <button class="tab-curso-btn" id="tabCursoEmpleo" onclick="cambiarTabCurso('empleo')">💼 Empleo & Vivienda</button>
            </div>

            <!-- Pestaña 1: Vídeo Tutorial -->
            <div id="cursoPanelVideo" class="curso-panel active">
                <div style="position: relative; border-radius: 14px; overflow: hidden; background: #000; box-shadow: 0 8px 25px rgba(0,0,0,0.6); margin-bottom: 14px;">
                    <video id="videoTutorialPlayer" controls playsinline preload="metadata" style="width: 100%; border-radius: 14px; display: block; max-height: 55vh; object-fit: contain;">
                        <source src="assets/tutorial_radaralertas.mp4" type="video/mp4">
                        Tu navegador no soporta reproducción de vídeo HTML5.
                    </video>
                </div>
                <p style="font-size: 12px; color: var(--text-muted); text-align: center;">Aprende en menos de 1 minuto cómo se analizan y adjudican los expedientes del Estado.</p>
            </div>

            <!-- Pestaña 2: Guía Subastas en 4 Pasos -->
            <div id="cursoPanelSubastas" class="curso-panel" style="display: none; text-align: left;">
                <div style="display: flex; flex-direction: column; gap: 12px; max-height: 55vh; overflow-y: auto; padding-right: 6px;">
                    <div style="background: rgba(255,255,255,0.03); border: 1px solid var(--border-glass); border-radius: 10px; padding: 12px;">
                        <strong style="color: #38bdf8; font-size: 13px;">1. Identifica el Tipo de Subasta</strong>
                        <p style="font-size: 12px; color: var(--text-muted); margin-top: 3px;">
                            • <strong>Judiciales (BOE):</strong> Embargos hipotecarios y concursos de acreedores.<br>
                            • <strong>Decomisos (PNSD):</strong> Bienes incautados sin deudas del dueño anterior.
                        </p>
                    </div>
                    <div style="background: rgba(255,255,255,0.03); border: 1px solid var(--border-glass); border-radius: 10px; padding: 12px;">
                        <strong style="color: #10b981; font-size: 13px;">2. La Protección del Artículo 674 LEC</strong>
                        <p style="font-size: 12px; color: var(--text-muted); margin-top: 3px;">
                            El Mandamiento Judicial cancela por ley todas las cargas y deudas posteriores. Con el dictamen pericial de cargas sabes de antemano que compras a 0,00 € de deudas.
                        </p>
                    </div>
                    <div style="background: rgba(255,255,255,0.03); border: 1px solid var(--border-glass); border-radius: 10px; padding: 12px;">
                        <strong style="color: #f59e0b; font-size: 13px;">3. Cómo Pujar Telemáticamente con Cl@ve</strong>
                        <p style="font-size: 12px; color: var(--text-muted); margin-top: 3px;">
                            Entras en subastas.boe.es, consignas el 5% de depósito desde tu banco online y firmas con tu móvil. Si no ganas, el juzgado te devuelve el 100% íntegro.
                        </p>
                    </div>
                    <div style="background: rgba(255,255,255,0.03); border: 1px solid var(--border-glass); border-radius: 10px; padding: 12px;">
                        <strong style="color: #ec4899; font-size: 13px;">4. Adjudicación y Llaves</strong>
                        <p style="font-size: 12px; color: var(--text-muted); margin-top: 3px;">
                            Tras el decreto de adjudicación, el juzgado emite el testimonio que sustituye a la escritura notarial y te otorga la posesión legal.
                        </p>
                    </div>
                </div>
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
    </div>"""

        if idx_mod_tut_start != -1:
            html = html[:idx_mod_tut_start] + new_modal_tutorial + html[idx_mod_tut_end:]

        # 3. Insertar el Asistente IA Flotante (Widget de Chat No Intrusivo)
        ai_widget_html = """
    <!-- Botón Flotante del Asistente IA de Dudas (Derecha) -->
    <div class="ai-assistant-wrapper">
        <button id="btnOpenAiChat" class="floating-ai-btn" onclick="toggleChatAsistente()" title="¿Dudas sobre cómo pujar o las cargas? Habla con el Asistente">
            <span class="ai-btn-pulse"></span>
            <span class="ai-btn-icon">🤖</span>
            <span class="ai-btn-label">¿Dudas? Asistente IA</span>
        </button>

        <!-- Ventana de Chat del Asistente -->
        <div id="aiChatWindow" class="ai-chat-window" style="display: none;">
            <div class="ai-chat-header">
                <div class="ai-header-info">
                    <span class="ai-header-avatar">🤖</span>
                    <div>
                        <strong>Asistente Jurídico Oficial</strong>
                        <span class="ai-status-online">● En línea 24/7</span>
                    </div>
                </div>
                <button class="ai-close-btn" onclick="toggleChatAsistente()">✕</button>
            </div>

            <div class="ai-chat-body" id="aiChatMessages">
                <div class="ai-msg ai-msg-bot">
                    <p>¡Hola! 👋 Soy el <strong>Asistente Pericial de RadarAlertas</strong>.</p>
                    <p style="margin-top: 6px;">Resuelvo al instante cualquier duda sobre cómo funcionan las subastas, cómo recuperar tu fianza o las bolsas de empleo.</p>
                    <p style="margin-top: 6px; font-size: 11px; color: var(--text-muted);">Pulsa una duda rápida o escribe tu consulta:</p>
                </div>

                <div class="ai-faq-chips" id="aiFaqChips">
                    <button class="ai-chip" onclick="enviarPreguntaRapida('fianza')">💰 ¿Cómo recupero la fianza del 5%?</button>
                    <button class="ai-chip" onclick="enviarPreguntaRapida('cargas')">🛡️ ¿Qué pasa con las deudas o multas?</button>
                    <button class="ai-chip" onclick="enviarPreguntaRapida('empleo')">💼 ¿Cómo entrar a empleo sin examen?</button>
                    <button class="ai-chip" onclick="enviarPreguntaRapida('kit')">📦 ¿Qué incluye el Kit de 2,90 €?</button>
                </div>
            </div>

            <div class="ai-chat-footer">
                <input type="text" id="aiInputText" placeholder="Pregunta sobre fianzas, pujas, cargas..." onkeydown="if(event.key==='Enter') enviarMensajeUsuario()">
                <button id="aiBtnSend" onclick="enviarMensajeUsuario()">➤</button>
            </div>
        </div>
    </div>
        """

        if 'id="btnOpenAiChat"' not in html:
            idx_body_end = html.find('</body>')
            assert idx_body_end != -1
            html = html[:idx_body_end] + ai_widget_html + html[idx_body_end:]

        # 4. Estilos CSS para el Asistente IA y la Academia
        extra_css = """
        /* === ESTILOS ASISTENTE IA FLOTANTE (DERECHA) === */
        .ai-assistant-wrapper {
            position: fixed;
            bottom: 24px;
            right: 24px;
            z-index: 999;
        }
        .floating-ai-btn {
            background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
            color: #ffffff;
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 11px 18px;
            border-radius: 999px;
            font-size: 13px;
            font-weight: 800;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4);
            transition: all 0.25s ease;
            position: relative;
        }
        .floating-ai-btn:hover {
            transform: translateY(-3px) scale(1.03);
            box-shadow: 0 12px 30px rgba(59, 130, 246, 0.6);
        }
        .ai-btn-pulse {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #10b981;
            box-shadow: 0 0 8px #10b981;
        }
        .ai-chat-window {
            position: absolute;
            bottom: 60px;
            right: 0;
            width: 350px;
            height: 480px;
            background: #0f172a;
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 18px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.6);
            display: flex;
            flex-direction: column;
            overflow: hidden;
            animation: fadeInChat 0.25s ease forwards;
        }
        body.theme-light .ai-chat-window {
            background: #ffffff;
            border-color: #cbd5e1;
            box-shadow: 0 20px 40px rgba(15, 23, 42, 0.15);
        }
        @keyframes fadeInChat {
            from { opacity: 0; transform: translateY(12px) scale(0.96); }
            to { opacity: 1; transform: translateY(0) scale(1); }
        }
        .ai-chat-header {
            background: #1e293b;
            padding: 12px 14px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }
        body.theme-light .ai-chat-header {
            background: #f1f5f9;
            border-color: #e2e8f0;
        }
        .ai-header-info {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .ai-header-avatar {
            font-size: 22px;
        }
        .ai-header-info strong {
            font-size: 12.5px;
            color: #ffffff;
            display: block;
        }
        body.theme-light .ai-header-info strong {
            color: #0f172a;
        }
        .ai-status-online {
            font-size: 10.5px;
            color: #10b981;
            font-weight: 700;
        }
        .ai-close-btn {
            background: transparent;
            border: none;
            color: #94a3b8;
            font-size: 16px;
            cursor: pointer;
            padding: 4px;
        }
        .ai-chat-body {
            flex: 1;
            padding: 14px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .ai-msg {
            max-width: 88%;
            padding: 10px 12px;
            border-radius: 12px;
            font-size: 12px;
            line-height: 1.45;
        }
        .ai-msg-bot {
            align-self: flex-start;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: #e2e8f0;
            border-bottom-left-radius: 2px;
        }
        body.theme-light .ai-msg-bot {
            background: #f8fafc;
            border-color: #e2e8f0;
            color: #1e293b;
        }
        .ai-msg-user {
            align-self: flex-end;
            background: #2563eb;
            color: #ffffff;
            border-bottom-right-radius: 2px;
            font-weight: 600;
        }
        .ai-faq-chips {
            display: flex;
            flex-direction: column;
            gap: 6px;
            margin-top: 6px;
        }
        .ai-chip {
            background: rgba(56, 189, 248, 0.1);
            border: 1px solid rgba(56, 189, 248, 0.3);
            color: #38bdf8;
            padding: 7px 10px;
            border-radius: 8px;
            font-size: 11.5px;
            font-weight: 700;
            cursor: pointer;
            text-align: left;
            transition: all 0.2s;
        }
        .ai-chip:hover {
            background: rgba(56, 189, 248, 0.2);
            transform: translateX(3px);
        }
        .ai-chat-footer {
            padding: 10px 12px;
            background: #1e293b;
            border-top: 1px solid rgba(255, 255, 255, 0.08);
            display: flex;
            gap: 8px;
        }
        body.theme-light .ai-chat-footer {
            background: #f1f5f9;
            border-color: #e2e8f0;
        }
        .ai-chat-footer input {
            flex: 1;
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 8px 12px;
            color: #ffffff;
            font-size: 12px;
            outline: none;
        }
        body.theme-light .ai-chat-footer input {
            background: #ffffff;
            border-color: #cbd5e1;
            color: #0f172a;
        }
        .ai-chat-footer button {
            background: #2563eb;
            color: #ffffff;
            border: none;
            padding: 0 14px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 800;
        }

        /* Tabs de la Academia */
        .tab-curso-btn {
            background: transparent;
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: var(--text-muted);
            padding: 6px 12px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 700;
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.2s;
        }
        .tab-curso-btn.active {
            background: rgba(56, 189, 248, 0.15);
            border-color: #38bdf8;
            color: #38bdf8;
        }
        @media (max-width: 768px) {
            .ai-assistant-wrapper {
                bottom: 80px;
                right: 14px;
            }
            .floating-ai-btn {
                padding: 9px 14px;
                font-size: 11px;
            }
            .ai-chat-window {
                width: 310px;
                height: 420px;
                bottom: 50px;
                right: 0;
            }
        }
        """

        if '/* === ESTILOS ASISTENTE IA FLOTANTE' not in html:
            idx_style_end = html.find('</style>')
            assert idx_style_end != -1
            html = html[:idx_style_end] + extra_css + html[idx_style_end:]

        # 5. Funciones JavaScript para el Asistente IA y Pestañas del Curso
        js_code = """
        // Funciones del Mini-Curso / Academia
        function cambiarTabCurso(tab) {
            document.querySelectorAll('.tab-curso-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.curso-panel').forEach(p => p.style.display = 'none');
            
            const player = document.getElementById('videoTutorialPlayer');
            if (tab === 'video') {
                document.getElementById('tabCursoVideo').classList.add('active');
                document.getElementById('cursoPanelVideo').style.display = 'block';
            } else if (tab === 'subastas') {
                if (player) player.pause();
                document.getElementById('tabCursoSubastas').classList.add('active');
                document.getElementById('cursoPanelSubastas').style.display = 'block';
            } else if (tab === 'empleo') {
                if (player) player.pause();
                document.getElementById('tabCursoEmpleo').classList.add('active');
                document.getElementById('cursoPanelEmpleo').style.display = 'block';
            }
        }

        // Funciones del Asistente IA Flotante
        function toggleChatAsistente() {
            const chat = document.getElementById('aiChatWindow');
            if (!chat) return;
            if (chat.style.display === 'none' || !chat.style.display) {
                chat.style.display = 'flex';
            } else {
                chat.style.display = 'none';
            }
        }

        function agregarMensajeChat(texto, emisor = 'bot') {
            const container = document.getElementById('aiChatMessages');
            if (!container) return;
            const div = document.createElement('div');
            div.className = emisor === 'user' ? 'ai-msg ai-msg-user' : 'ai-msg ai-msg-bot';
            div.innerHTML = texto;
            container.appendChild(div);
            container.scrollTop = container.scrollHeight;
        }

        function enviarPreguntaRapida(tipo) {
            const faqContainer = document.getElementById('aiFaqChips');
            if (faqContainer) faqContainer.style.display = 'none';

            if (tipo === 'fianza') {
                agregarMensajeChat('¿Cómo funciona la fianza del 5% y cómo se recupera?', 'user');
                setTimeout(() => {
                    agregarMensajeChat(`
                        <p><strong>Garantía Oficial del 5%:</strong></p>
                        <p style="margin-top:4px;">Para participar en el BOE depositas un 5% de fianza en la cuenta del juzgado.</p>
                        <p style="margin-top:4px;">• <strong>Si ganas la subasta:</strong> El 5% se descuenta del precio final.</p>
                        <p style="margin-top:4px;">• <strong>Si no ganas:</strong> El juzgado te lo devuelve <strong>100% íntegro</strong> a tu cuenta bancaria (Art. 652 LEC). En nuestro Kit de 2,90 € incluimos la plantilla oficial tramitada para agilizar la devolución inmediata.</p>
                    `);
                }, 400);
            } else if (tipo === 'cargas') {
                agregarMensajeChat('¿Qué pasa si el inmueble o coche tiene deudas o multas?', 'user');
                setTimeout(() => {
                    agregarMensajeChat(`
                        <p><strong>Cancelación de Deudas por Ley:</strong></p>
                        <p style="margin-top:4px;">Por el <strong>Artículo 674 de la LEC</strong>, el mandamiento judicial cancela todas las cargas y deudas posteriores.</p>
                        <p style="margin-top:4px;">En vehículos de decomiso (PNSD) o subastas tributarias, se entregan libres de precintos y multas anteriores de la DGT.</p>
                    `);
                }, 400);
            } else if (tipo === 'empleo') {
                agregarMensajeChat('¿Cómo funcionan las bolsas de empleo sin examen?', 'user');
                setTimeout(() => {
                    agregarMensajeChat(`
                        <p><strong>Bolsas de Empleo Sin Oposición:</strong></p>
                        <p style="margin-top:4px;">Se convocan bajo modalidad de <em>Concurso de Méritos</em>. No tienes que estudiar ningún temario.</p>
                        <p style="margin-top:4px;">La plaza (+2.150 €/mes) se asigna por méritos oficiales (títulos o carnet). En el Radar tienes plazas abiertas de Hacienda, Trabajo y Defensa.</p>
                    `);
                }, 400);
            } else if (tipo === 'kit') {
                agregarMensajeChat('¿Qué incluye exactamente el Kit de 2,90 €?', 'user');
                setTimeout(() => {
                    agregarMensajeChat(`
                        <p><strong>Kit Completo de Seguridad (3 en 1):</strong></p>
                        <p style="margin-top:4px;">1. 📄 <strong>Informe Técnico de Cargas en PDF</strong> con certificado de deuda 0€.</p>
                        <p style="margin-top:4px;">2. 📱 <strong>Guía Visual con capturas</strong> para pujar con Cl@ve en 3 minutos.</p>
                        <p style="margin-top:4px;">3. 🛡️ <strong>Plantilla Oficial</strong> para la devolución de la fianza.</p>
                        <p style="margin-top:6px;"><a href="#catalogo" onclick="toggleChatAsistente()" style="color:#38bdf8; font-weight:700;">Ver Oportunidades en el Catálogo →</a></p>
                    `);
                }, 400);
            }
        }

        function enviarMensajeUsuario() {
            const input = document.getElementById('aiInputText');
            if (!input || !input.value.trim()) return;
            const query = input.value.trim();
            input.value = '';
            
            agregarMensajeChat(query, 'user');
            
            const qLower = query.toLowerCase();
            setTimeout(() => {
                if (qLower.includes('okupa') || qLower.includes('posesion') || qLower.includes('llave')) {
                    agregarMensajeChat('<strong>Sobre la Posesión Legal:</strong> El decreto judicial de adjudicación te otorga el derecho de lanzamiento legal (Art. 675 LEC) a través del juzgado sin necesidad de contratar pleitos privados.');
                } else if (qLower.includes('precio') || qLower.includes('pago') || qLower.includes('coste') || qLower.includes('cuanto')) {
                    agregarMensajeChat('Tienes <strong>1 oportunidad gratis por categoría</strong> en el radar para probar el sistema sin pagar. Cada Kit de expediente individual cuesta solo 2,90 € (pago único) o tarifa plana con el Plan PRO (14,99 €/mes).');
                } else if (qLower.includes('coche') || qLower.includes('vehiculo') || qLower.includes('macan') || qLower.includes('mercedes')) {
                    agregarMensajeChat('Los vehículos procedentes de decomisos (PNSD / Estado) se adjudican con mandamiento judicial que cancela precintos anteriores en la DGT. Puedes ver el Citroën C5 híbrido como muestra gratuita en el catálogo.');
                } else {
                    agregarMensajeChat('Entendido. En el portal dispones de la <strong>Auditoría Pericial Oficial</strong> de cada lote. Puedes explorar las muestras gratuitas en el catálogo o desbloquear el kit completo de cualquier expediente por solo 2,90 €.');
                }
            }, 500);
        }
        """

        if 'function cambiarTabCurso' not in html:
            idx_script_end = html.rfind('</script>')
            assert idx_script_end != -1
            html = html[:idx_script_end] + js_code + html[idx_script_end:]

        with open(p, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Actualizado con éxito: {p}")

if __name__ == '__main__':
    main()
