import os

import streamlit as st

from coach_agent import evaluate_case
from question_specs import QUESTION_SPECS


st.set_page_config(
    page_title="Problem Solving Coach",
    page_icon="🧠",
    layout="wide",
)


def load_cloud_secrets() -> None:
    """Copy Streamlit root-level secrets into environment variables when available."""
    try:
        if "OPENAI_API_KEY" in st.secrets:
            os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
        if "OPENAI_MODEL" in st.secrets:
            os.environ["OPENAI_MODEL"] = st.secrets["OPENAI_MODEL"]
    except FileNotFoundError:
        # Normal when running locally without .streamlit/secrets.toml.
        pass


load_cloud_secrets()

STATUS_LABELS = {
    "known": "✅ Conocido",
    "verify": "🔎 Por verificar",
    "pending": "⏳ Pendiente",
    "not_applicable": "➖ No aplica",
}

QUALITY_LABELS = {
    "excellent": "🟢 Excelente",
    "useful": "🟡 Útil",
    "weak": "🟠 Débil / mejorable",
    "invalid": "🔴 Inválido",
    "not_evaluable": "⚪ No evaluable todavía",
}


st.title("🧠 Problem Solving Coach")
st.caption("MVP v0.2 · IS / IS-NOT · El objetivo es mejorar la investigación, no llenar celdas por llenar.")

with st.expander("Principios del coach", expanded=False):
    st.markdown(
        """
- **No inventa información.** `No sé` es una respuesta válida.
- **No confunde desconocido con NO ES.**
- Si falta información, propone **cómo obtenerla o verificarla**.
- Una diferencia entre ES y NO ES es una **pista**, no una causa raíz demostrada.
- Busca el contraste técnicamente más cercano y conserva comparaciones secundarias útiles.
        """
    )

question_options = {
    f"{qid}. [{spec['dimension']}] {spec['name']}": qid
    for qid, spec in QUESTION_SPECS.items()
}

with st.form("evaluation_form"):
    selected_label = st.selectbox("Pregunta del formato", list(question_options.keys()))
    question_id = question_options[selected_label]
    spec = QUESTION_SPECS[question_id]

    st.info(f"**Objetivo metodológico:** {spec['objective']}")

    problem_statement = st.text_area(
        "Problema general",
        placeholder="Ej. Scrap por altura de conmutador fuera de especificación",
        height=80,
    )
    defect_mode = st.text_input(
        "Modo de falla / defecto observado",
        placeholder="Ej. Altura de conmutador fuera de especificación",
    )

    left, right = st.columns(2)
    with left:
        is_value = st.text_area(
            "ES",
            placeholder="Ej. Inducido 013",
            height=100,
        )
    with right:
        is_not_value = st.text_area(
            "NO ES",
            placeholder="Puedes escribir 'no sé' si aún no existe un contraste confirmado",
            height=100,
        )

    known_difference = st.text_area(
        "Diferencia conocida entre ES y NO ES",
        placeholder="Puede quedar en blanco o escribir 'no sé'. No es obligatorio conocerla todavía.",
        height=80,
    )
    context = st.text_area(
        "Contexto adicional",
        placeholder="Máquina, turno, PN, proveedor, secuencia, evidencia disponible, información pendiente, etc.",
        height=130,
    )

    submitted = st.form_submit_button("✨ Evaluar contraste", use_container_width=True)

if submitted:
    if not os.getenv("OPENAI_API_KEY"):
        st.error(
            "No encuentro OPENAI_API_KEY. En Streamlit Community Cloud agrégala en App settings → Secrets."
        )
    elif not problem_statement.strip() or not defect_mode.strip() or not is_value.strip():
        st.warning("Completa al menos Problema general, Modo de falla y ES. NO ES puede ser desconocido.")
    else:
        try:
            with st.spinner("La ingeniera virtual está revisando el contraste…"):
                result = evaluate_case(
                    question_id=question_id,
                    problem_statement=problem_statement.strip(),
                    defect_mode=defect_mode.strip(),
                    is_value=is_value.strip(),
                    is_not_value=is_not_value.strip() or "unknown",
                    known_difference=known_difference.strip(),
                    context=context.strip(),
                )
            st.session_state["last_result"] = result
            st.session_state["last_question"] = selected_label
        except Exception as exc:
            st.error("No pude completar la evaluación.")
            with st.expander("Detalle técnico para diagnóstico"):
                st.code(f"{type(exc).__name__}: {exc}")

result = st.session_state.get("last_result")
if result is not None:
    st.divider()
    st.subheader("Evaluación del coach")
    st.caption(st.session_state.get("last_question", ""))

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Estado de la información", STATUS_LABELS.get(result.status, result.status))
    with c2:
        st.metric("Calidad del contraste", QUALITY_LABELS.get(result.contrast_quality, result.contrast_quality))

    st.markdown("### Lo que sabemos")
    st.write(result.answer_summary)

    st.markdown("### 🥇 Contraste principal recomendado")
    st.success(result.primary_contrast)

    if result.secondary_contrasts:
        st.markdown("### 🥈 Contrastes secundarios / exploratorios")
        for item in result.secondary_contrasts:
            st.markdown(f"- {item}")

    if result.relevant_differences:
        st.markdown("### 🔍 Diferencias observadas")
        for item in result.relevant_differences:
            st.markdown(f"- {item}")

    if result.missing_information:
        st.markdown("### ⏳ Información pendiente o por verificar")
        for item in result.missing_information:
            st.markdown(f"- {item}")

    if result.suggested_actions:
        st.markdown("### 🧪 Acciones de investigación sugeridas")
        for number, action in enumerate(result.suggested_actions, start=1):
            with st.container(border=True):
                st.markdown(f"**{number}. {action.action}**")
                st.caption(f"Evidencia esperada: {action.evidence_expected}")

    st.markdown("### ➡️ Mejor siguiente pregunta")
    st.info(result.next_question)

    if result.methodological_warning and result.methodological_warning.lower() != "none":
        st.warning(result.methodological_warning)

    st.caption(f"Límite causal: {result.causal_boundary_note}")
