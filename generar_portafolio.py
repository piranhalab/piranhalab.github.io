#!/usr/bin/env python3
"""
Genera portafolio PDF de PiranhaLab para convocatoria Economía Creativa 2026.
Uso: python3 generar_portafolio.py
Salida: portafolio_piranhalab.pdf
"""

import base64
import os
from pathlib import Path
import weasyprint

BASE = Path(__file__).parent
IMG = BASE / "img"

def img_b64(path: Path) -> str:
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    ext = path.suffix.lstrip(".").lower()
    mime = "jpeg" if ext in ("jpg", "jpeg") else ext
    return f"data:image/{mime};base64,{data}"

logo   = img_b64(IMG / "plab-logo.png")
conv   = img_b64(IMG / "conversatorio.jpg")
prof   = img_b64(IMG / "profeticas-r.png")
tec    = img_b64(IMG / "tecnologias-cotidianas.jpeg")
edges  = img_b64(IMG / "edges.jpeg")

HTML = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<style>
  @page {{
    size: A4;
    margin: 2cm 2.2cm 2cm 2.2cm;
  }}

  * {{ margin: 0; padding: 0; box-sizing: border-box; }}

  body {{
    background: #ffffff;
    color: #111111;
    font-family: Helvetica, Arial, sans-serif;
    font-size: 9.5pt;
    line-height: 1.55;
  }}

  /* ── PORTADA ── */
  .cover {{
    height: 267mm;           /* aprox una A4 sin márgenes */
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    page-break-after: always;
    border-bottom: 1.5px solid #111;
  }}

  .cover-top {{
    display: flex;
    align-items: flex-start;
    gap: 1.2rem;
    padding-top: 0.5cm;
  }}

  .cover-logo {{
    width: 48px;
    height: 48px;
    object-fit: contain;
  }}

  .cover-brand {{
    font-size: 9pt;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    line-height: 1.2;
    opacity: 0.7;
  }}

  .cover-title {{
    font-size: 56pt;
    font-weight: 900;
    line-height: 0.9;
    letter-spacing: -0.03em;
    text-transform: uppercase;
    margin-top: auto;
    margin-bottom: 0.6cm;
  }}

  .cover-sub {{
    font-size: 10pt;
    opacity: 0.55;
    margin-bottom: 0.3cm;
    max-width: 55ch;
  }}

  .cover-meta {{
    font-size: 7.5pt;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    opacity: 0.35;
    margin-bottom: 0.5cm;
  }}

  /* ── SECCIONES ── */
  .section {{
    page-break-before: auto;
    margin-bottom: 1.2cm;
  }}

  .section-label {{
    font-size: 6.5pt;
    font-weight: 700;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    opacity: 0.35;
    margin-bottom: 0.15cm;
  }}

  .section-title {{
    font-size: 20pt;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: -0.02em;
    line-height: 1;
    border-bottom: 1.5px solid #111;
    padding-bottom: 0.25cm;
    margin-bottom: 0.5cm;
  }}

  /* ── INTRO TEXT ── */
  .intro-text {{
    font-size: 10pt;
    line-height: 1.7;
    max-width: 80ch;
    margin-bottom: 0.6cm;
  }}

  /* ── TIMELINE / EVENTOS ── */
  .timeline {{
    border-top: 1.5px solid #111;
    margin-top: 0.2cm;
  }}

  .event {{
    display: flex;
    border-bottom: 1px solid rgba(17,17,17,0.18);
    padding: 0.32cm 0;
    gap: 0.6cm;
    page-break-inside: avoid;
  }}

  .event-year {{
    font-size: 7pt;
    font-weight: 700;
    letter-spacing: 0.1em;
    opacity: 0.4;
    min-width: 1.4cm;
    padding-top: 0.05cm;
    text-transform: uppercase;
  }}

  .event-body {{
    flex: 1;
  }}

  .event-title {{
    font-size: 9pt;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 0.02em;
    margin-bottom: 0.1cm;
  }}

  .event-desc {{
    font-size: 8.5pt;
    opacity: 0.65;
    line-height: 1.5;
  }}

  /* ── PUBLICACIÓN ── */
  .pub-block {{
    border: 1.5px solid #111;
    padding: 0.5cm;
    margin-bottom: 0.5cm;
    page-break-inside: avoid;
  }}

  .pub-label {{
    font-size: 6.5pt;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    opacity: 0.4;
    margin-bottom: 0.2cm;
  }}

  .pub-title {{
    font-size: 9.5pt;
    font-weight: 700;
    margin-bottom: 0.15cm;
    line-height: 1.4;
  }}

  .pub-desc {{
    font-size: 8.5pt;
    opacity: 0.65;
    line-height: 1.5;
  }}

  .pub-link {{
    font-size: 7.5pt;
    font-weight: 700;
    letter-spacing: 0.05em;
    color: #111;
    word-break: break-all;
    margin-top: 0.2cm;
    display: block;
    opacity: 0.5;
  }}

  /* ── STATS BAR ── */
  .stats-row {{
    display: flex;
    border: 1.5px solid #111;
    margin-bottom: 0.5cm;
  }}

  .stat {{
    flex: 1;
    padding: 0.4cm 0.5cm;
    border-right: 1.5px solid #111;
  }}

  .stat:last-child {{ border-right: none; }}

  .stat-num {{
    font-size: 20pt;
    font-weight: 900;
    letter-spacing: -0.03em;
    line-height: 1;
  }}

  .stat-label {{
    font-size: 7pt;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    opacity: 0.4;
    margin-top: 0.1cm;
  }}

  /* ── IMAGES ── */
  .img-row {{
    display: flex;
    gap: 0.4cm;
    margin-bottom: 0.5cm;
    page-break-inside: avoid;
  }}

  .img-block {{
    flex: 1;
  }}

  .img-block img {{
    width: 100%;
    object-fit: cover;
    display: block;
    filter: grayscale(80%);
    border: 1px solid rgba(17,17,17,0.15);
  }}

  .img-caption {{
    font-size: 6.5pt;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    opacity: 0.4;
    margin-top: 0.15cm;
  }}

  /* ── LINKS ── */
  .links-block {{
    border: 1.5px solid #111;
    padding: 0.5cm;
    page-break-inside: avoid;
    margin-bottom: 0.5cm;
  }}

  .links-block .link-item {{
    font-size: 8pt;
    border-bottom: 1px solid rgba(17,17,17,0.15);
    padding: 0.2cm 0;
    display: flex;
    gap: 0.4cm;
    align-items: baseline;
  }}

  .links-block .link-item:last-child {{ border-bottom: none; }}

  .link-tag {{
    font-size: 6.5pt;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    opacity: 0.4;
    min-width: 3.5cm;
  }}

  .link-url {{
    word-break: break-all;
    opacity: 0.65;
  }}

  /* ── FOOTER PER PAGE ── */
  .page-footer {{
    font-size: 7pt;
    opacity: 0.3;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    border-top: 1px solid rgba(17,17,17,0.2);
    padding-top: 0.2cm;
    margin-top: 0.6cm;
  }}

  /* ── PILARES ── */
  .pilares {{
    display: flex;
    gap: 0;
    border: 1.5px solid #111;
    margin-bottom: 0.5cm;
    page-break-inside: avoid;
  }}

  .pilar {{
    flex: 1;
    padding: 0.4cm 0.5cm;
    border-right: 1.5px solid #111;
  }}

  .pilar:last-child {{ border-right: none; }}

  .pilar-num {{
    font-size: 6.5pt;
    font-weight: 700;
    letter-spacing: 0.2em;
    opacity: 0.35;
    text-transform: uppercase;
    margin-bottom: 0.15cm;
  }}

  .pilar-title {{
    font-size: 8.5pt;
    font-weight: 900;
    text-transform: uppercase;
    margin-bottom: 0.1cm;
  }}

  .pilar-desc {{
    font-size: 7.5pt;
    opacity: 0.6;
    line-height: 1.5;
  }}

  /* ── PAGE BREAK UTILITY ── */
  .pb {{ page-break-before: always; }}
</style>
</head>
<body>

<!-- ═══════════════════════════════════════
     PORTADA
═══════════════════════════════════════ -->
<div class="cover">
  <div class="cover-top">
    <img class="cover-logo" src="{logo}" alt="Logo PiranhaLab">
    <div class="cover-brand">Piranha<br>Lab</div>
  </div>

  <div>
    <div class="cover-title">Portafolio<br>de<br>Trayectoria</div>
    <p class="cover-sub">
      PiranhaLab es un laboratorio de experimentación entre arte, tecnología y educación.
      Activo desde 2019. Operamos desde Ciudad de México con presencia en todo el territorio nacional.
    </p>
    <div class="cover-meta">
      Convocatoria Economía Creativa 2026 — Vertiente B &nbsp;·&nbsp;
      Secretaría de Cultura / DGVC &nbsp;·&nbsp; Mayo 2026
    </div>
  </div>
</div>


<!-- ═══════════════════════════════════════
     QUIÉNES SOMOS
═══════════════════════════════════════ -->
<div class="section pb">
  <p class="section-label">01</p>
  <h2 class="section-title">Quiénes Somos</h2>

  <p class="intro-text">
    PiranhaLab es un laboratorio de arte, tecnología y cultura libre activo desde 2019.
    Producimos infraestructura cultural experimental: instalaciones sonoras, herramientas
    de código abierto, talleres de soberanía tecnológica y archivo distribuido.
    El hilo conductor es la cultura libre como práctica — no como declaración de principios,
    sino como método de trabajo.
  </p>

  <p class="intro-text">
    PiranhaLab no es una persona: es la capa colectiva que atraviesa varios proyectos.
    En siete años hemos desarrollado proyectos de arte sonoro y medios audiovisuales
    experimentales, impartido talleres de software libre y síntesis sonora, y construido
    herramientas propias de código abierto en colaboración con instituciones culturales y
    comunidades educativas de todo el país.
  </p>

  <div class="pilares">
    <div class="pilar">
      <div class="pilar-num">Pilar 01</div>
      <div class="pilar-title">DIY / DIWO</div>
      <p class="pilar-desc">Hacer por unx mismx y hacer junto a otrxs como proceso de enseñanza-aprendizaje.</p>
    </div>
    <div class="pilar">
      <div class="pilar-num">Pilar 02</div>
      <div class="pilar-title">Software Libre</div>
      <p class="pilar-desc">Democratizar la expresión y el pensamiento crítico. Traspasar la frontera entre consumo y creación.</p>
    </div>
    <div class="pilar">
      <div class="pilar-num">Pilar 03</div>
      <div class="pilar-title">Educación Experimental</div>
      <p class="pilar-desc">Talleres y programas que fomentan el pensamiento crítico y la creación colaborativa.</p>
    </div>
  </div>

  <div class="stats-row">
    <div class="stat">
      <div class="stat-num">7</div>
      <div class="stat-label">Años de trayectoria</div>
    </div>
    <div class="stat">
      <div class="stat-num">+20</div>
      <div class="stat-label">Actividades documentadas</div>
    </div>
    <div class="stat">
      <div class="stat-num">+600</div>
      <div class="stat-label">Participantes directos</div>
    </div>
    <div class="stat">
      <div class="stat-num">+150</div>
      <div class="stat-label">Visualizaciones streaming</div>
    </div>
  </div>
</div>


<!-- ═══════════════════════════════════════
     TRAYECTORIA 2019–2026
═══════════════════════════════════════ -->
<div class="section pb">
  <p class="section-label">02</p>
  <h2 class="section-title">Trayectoria 2019 – 2026</h2>

  <div class="timeline">

    <div class="event">
      <div class="event-year">2019</div>
      <div class="event-body">
        <div class="event-title">Ciclo PADID / CCD — Centro Cultural Digital, CDMX</div>
        <div class="event-desc">
          5 talleres, 2 conversatorios y 2 conciertos en colaboración con el Centro Cultural Digital
          de la Secretaría de Cultura. Promedio de 25 participantes por actividad.
          El taller con mayor demanda registró más de 100 solicitudes de inscripción.
          Concierto final con más de 100 asistentes.
        </div>
      </div>
    </div>

    <div class="event">
      <div class="event-year">2019</div>
      <div class="event-body">
        <div class="event-title">PiranhaHíbrida — Colaboración con Híbridas y Quimeras, El Rule, CDMX</div>
        <div class="event-desc">
          Concierto colaborativo en el espacio cultural El Rule. Asistencia de 25 personas.
        </div>
      </div>
    </div>

    <div class="event">
      <div class="event-year">2020</div>
      <div class="event-body">
        <div class="event-title">Ciclo de Conciertos EDGES — Colaboración con Centro Multimedia / CENART</div>
        <div class="event-desc">
          5 conciertos virtuales en espacios tridimensionales diseñados por el colectivo.
          Colaboración con el Centro Multimedia del CENART.
          Promedio de 25 asistentes por evento, pico de 50 participantes simultáneos.
          Experiencia sistematizada en publicación académica (ver sección Publicaciones).
        </div>
      </div>
    </div>

    <div class="event">
      <div class="event-year">2020</div>
      <div class="event-body">
        <div class="event-title">Muestra VIDEOTITLAN — Sede e infraestructura virtual, Videos Caseros</div>
        <div class="event-desc">
          Participación como sede e infraestructura virtual en la muestra de video latinoamericano VIDEOTITLAN.
          Presentación de más de 20 proyectos de video con asistencia de 30 personas,
          más concierto de cierre.
        </div>
      </div>
    </div>

    <div class="event">
      <div class="event-year">2020</div>
      <div class="event-body">
        <div class="event-title">Streaming Navegaciones Guiadas 3.5 — CCD (con Doreen Ríos)</div>
        <div class="event-desc">
          Más de 150 visualizaciones en transmisión en vivo producida en colaboración con el
          Centro Cultural Digital y la curadora Doreen Ríos.
        </div>
      </div>
    </div>

    <div class="event">
      <div class="event-year">2020</div>
      <div class="event-body">
        <div class="event-title">Concierto Virtual Underborders</div>
        <div class="event-desc">
          Asistencia de 60 personas en concierto virtual internacional.
        </div>
      </div>
    </div>

    <div class="event">
      <div class="event-year">2020</div>
      <div class="event-body">
        <div class="event-title">Concierto Pruebas Proféticas</div>
        <div class="event-desc">
          Asistencia de 30 personas. Presentación en vivo de trabajo audiovisual experimental.
        </div>
      </div>
    </div>

    <div class="event">
      <div class="event-year">2020</div>
      <div class="event-body">
        <div class="event-title">Hackmitin — Taller de Gráficos Animados 3D con Three.js</div>
        <div class="event-desc">
          Asistencia de 20 personas. Taller práctico en el marco del Hackmitin,
          encuentro de tecnología libre y cultura digital.
        </div>
      </div>
    </div>

    <div class="event">
      <div class="event-year">2026</div>
      <div class="event-body">
        <div class="event-title">Congreso SEP / UNESCO — Educación, Arte y Cultura</div>
        <div class="event-desc">
          Participación en mesa sobre tecnología y educación en el Congreso Educación, Arte y Cultura,
          organizado por la SEP en colaboración con la UNESCO. Más de 100 profesoras y profesores
          de diferentes partes de la República Mexicana.
        </div>
      </div>
    </div>

    <div class="event">
      <div class="event-year">2026</div>
      <div class="event-body">
        <div class="event-title">Alas y Raíces — 2 Talleres para Promotores Culturales</div>
        <div class="event-desc">
          Programa Alas y Raíces, Coordinación Nacional de Desarrollo Cultural Infantil,
          Secretaría de Cultura. Dos talleres con 25 y 40 participantes respectivamente,
          dirigidos a promotores culturales de la región norte de México.
          Reunión Nacional de Cultura Infantil 2026, Puebla.
        </div>
      </div>
    </div>

  </div>
</div>


<!-- ═══════════════════════════════════════
     IMÁGENES DOCUMENTALES
═══════════════════════════════════════ -->
<div class="section pb">
  <p class="section-label">03</p>
  <h2 class="section-title">Registro Fotográfico</h2>

  <div class="img-row">
    <div class="img-block">
      <img src="{conv}" alt="Conversatorio CCD" style="height:120px;">
      <div class="img-caption">Conversatorio — Centro Cultural Digital, 2019</div>
    </div>
    <div class="img-block">
      <img src="{prof}" alt="Pruebas Proféticas" style="height:120px;">
      <div class="img-caption">Concierto Pruebas Proféticas, 2020</div>
    </div>
  </div>

  <div class="img-row">
    <div class="img-block">
      <img src="{tec}" alt="Tecnologías Cotidianas" style="height:120px;">
      <div class="img-caption">Taller Tecnologías Cotidianas — Alas y Raíces, Puebla 2026</div>
    </div>
    <div class="img-block">
      <img src="{edges}" alt="Ciclo EDGES" style="height:120px;">
      <div class="img-caption">Ciclo EDGES — Conciertos Virtuales, 2020</div>
    </div>
  </div>
</div>


<!-- ═══════════════════════════════════════
     PUBLICACIONES Y REFERENCIAS
═══════════════════════════════════════ -->
<div class="section pb">
  <p class="section-label">04</p>
  <h2 class="section-title">Publicaciones y Referencias Académicas</h2>

  <div class="pub-block">
    <div class="pub-label">Capítulo de libro — UNAM, 2022</div>
    <div class="pub-title">
      Panorama. Escritura de espacios libres e inmersivos para el performance audiovisual
    </div>
    <p class="pub-desc">
      Ocelotl, E., Sotomayor, D. y Teixido, M. (2022). En <em>Algoritmos Arruinados.
      Perspectivas situadas de tecnología musical</em>. Universidad Nacional Autónoma de México (UNAM).
      ISBN 978-607-3062-11-4.
    </p>
    <span class="pub-link">https://www.repositorio.fam.unam.mx/handle/123456789/139</span>
  </div>

  <div class="pub-block">
    <div class="pub-label">Referencia externa</div>
    <div class="pub-title">
      Obra en De-construcción — Milena Pafundi
    </div>
    <p class="pub-desc">
      Referencia y documentación de participación de PiranhaLab en obra audiovisual.
    </p>
    <span class="pub-link">https://www.milenapafundi.com/Obra-en-De-construccion</span>
  </div>

  <div class="pub-block">
    <div class="pub-label">Registro institucional</div>
    <div class="pub-title">
      Conversatorio — La creación artística y el desarrollo tecnológico en el contexto del arte
      por computadora
    </div>
    <p class="pub-desc">
      Actividad documentada en la plataforma institucional del Centro Cultural Digital (Secretaría de Cultura).
    </p>
    <span class="pub-link">https://www.centroculturadigital.mx/actividad/Conversatorio-La-creacion-artistica-y-el-desarrollo-tecnologico-en-el-contexto-del-arte-por-computadora-SJbVDcQQN</span>
  </div>
</div>


<!-- ═══════════════════════════════════════
     RECURSOS Y PRESENCIA EN LÍNEA
═══════════════════════════════════════ -->
<div class="section pb">
  <p class="section-label">05</p>
  <h2 class="section-title">Presencia en Línea y Recursos</h2>

  <div class="links-block">
    <div class="link-item">
      <span class="link-tag">Sitio web</span>
      <span class="link-url">https://piranhalab.cc/</span>
    </div>
    <div class="link-item">
      <span class="link-tag">YouTube — Videos</span>
      <span class="link-url">https://www.youtube.com/@piranhalab1257/videos</span>
    </div>
    <div class="link-item">
      <span class="link-tag">YouTube — Streams</span>
      <span class="link-url">https://www.youtube.com/@piranhalab1257/streams</span>
    </div>
    <div class="link-item">
      <span class="link-tag">Registro CCD</span>
      <span class="link-url">https://www.centroculturadigital.mx/actividad/Conversatorio-La-creacion-artistica-y-el-desarrollo-tecnologico-en-el-contexto-del-arte-por-computadora-SJbVDcQQN</span>
    </div>
    <div class="link-item">
      <span class="link-tag">Referencia externa</span>
      <span class="link-url">https://www.milenapafundi.com/Obra-en-De-construccion</span>
    </div>
    <div class="link-item">
      <span class="link-tag">Publicación UNAM</span>
      <span class="link-url">https://www.repositorio.fam.unam.mx/handle/123456789/139</span>
    </div>
    <div class="link-item">
      <span class="link-tag">Video documental</span>
      <span class="link-url">https://www.youtube.com/watch?v=W-keosDfPXU</span>
    </div>
  </div>
</div>


<!-- ═══════════════════════════════════════
     PROYECTOS EN CURSO
═══════════════════════════════════════ -->
<div class="section">
  <p class="section-label">06</p>
  <h2 class="section-title">Proyectos en Curso</h2>

  <div class="timeline">

    <div class="event">
      <div class="event-year">2026</div>
      <div class="event-body">
        <div class="event-title">Cartas Sonoras — Programa Alas y Raíces</div>
        <div class="event-desc">
          Taller para facilitadores que trabajan con infancias en contextos de privación de libertad.
          Escucha activa, captura sonora y composición colectiva con el teléfono móvil.
          Formato: videollamada, 2 horas. Impartido el 6 de mayo de 2026.
        </div>
      </div>
    </div>

    <div class="event">
      <div class="event-year">2026</div>
      <div class="event-body">
        <div class="event-title">Tecnologías Cotidianas para Documentar el Territorio</div>
        <div class="event-desc">
          Taller-laboratorio para promotores culturales. Formato presencial, 4 horas.
          Resultado: atlas tecnoafectivo con técnicas híbridas (dibujo + captura digital).
          Impartido en la Reunión Nacional de Cultura Infantil 2026, Puebla.
        </div>
      </div>
    </div>

  </div>

  <div class="page-footer">
    PiranhaLab &nbsp;·&nbsp; info@piranhalab.cc &nbsp;·&nbsp; piranhalab.cc &nbsp;·&nbsp;
    Portafolio de Trayectoria — Economía Creativa 2026 &nbsp;·&nbsp; Mayo 2026
  </div>
</div>

</body>
</html>
"""

output = BASE / "portafolio_piranhalab.pdf"
print("Generando PDF…")
wp = weasyprint.HTML(string=HTML, base_url=str(BASE))
wp.write_pdf(str(output))

size_mb = output.stat().st_size / 1_048_576
print(f"PDF generado: {output}")
print(f"Tamaño: {size_mb:.2f} MB {'✓ dentro del límite de 3 MB' if size_mb < 3 else '⚠ supera 3 MB'}")
