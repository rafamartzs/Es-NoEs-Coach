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


def initialize_session_state() -> None:
    """Create durable, question-specific storage for the four IS / IS-NOT fields."""
    if "question_inputs" not in st.session_state:
        st.session_state["question_inputs"] = {
            qid: {
                "is_value": "",
                "is_not_value": "",
                "known_difference": "",
                "context": "",
            }
            for qid in QUESTION_SPECS
        }

    # If a future version adds questions, make sure existing sessions get them too.
    for qid in QUESTION_SPECS:
        st.session_state["question_inputs"].setdefault(
            qid,
            {
                "is_value": "",
                "is_not_value": "",
                "known_difference": "",
                "context": "",
            },
        )

    if "question_results" not in st.session_state:
        st.session_state["question_results"] = {}


def save_question_field(question_id: int, field_name: str, widget_key: str) -> None:
    """Persist a widget value outside Streamlit's temporary widget lifecycle."""
    st.session_state["question_inputs"][question_id][field_name] = st.session_state.get(
        widget_key, ""
    )


load_cloud_secrets()
initialize_session_state()

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
st.caption(
    "MVP v0.3 · IS / IS-NOT · El objetivo es mejorar la investigación, no llenar celdas por llenar."
)

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

# IMPORTANT: the question selector lives OUTSIDE the evaluation form/button flow.
# Changing it reruns the page immediately, so the four question-specific fields can
# load their own saved values.
selected_label = st.selectbox(
    "Pregunta del formato",
    list(question_options.keys()),
    key="selected_question_label",
)
question_id = question_options[selected_label]
spec = QUESTION_SPECS[question_id]

st.info(f"**Objetivo metodológico:** {spec['objective']}")

# These two fields describe the overall case, so they intentionally remain shared
# across all 13 questions.
problem_statement = st.text_area(
    "Problema general",
    placeholder="Ej. Scrap por altura de conmutador fuera de especificación",
    height=80,
    key="problem_statement",
)
defect_mode = st.text_input(
    "Modo de falla / defecto observado",
    placeholder="Ej. Altura de conmutador fuera de especificación",
    key="defect_mode",
)

st.caption(
    "Los cuatro campos siguientes son **independientes para cada pregunta**. "
    "Puedes cambiar de pregunta y volver después sin perder lo escrito."
)

saved = st.session_state["question_inputs"][question_id]

is_key = f"_q{question_id}_is_value"
is_not_key = f"_q{question_id}_is_not_value"
difference_key = f"_q{question_id}_known_difference"
context_key = f"_q{question_id}_context"

left, right = st.columns(2)
with left:
    is_value = st.text_area(
        "ES",
        value=saved["is_value"],
        placeholder="Ej. Inducido 013",
        height=100,
        key=is_key,
        on_change=save_question_field,
        args=(question_id, "is_value", is_key),
    )
with right:
    is_not_value = st.text_area(
        "NO ES",
        value=saved["is_not_value"],
        placeholder="Puedes escribir 'no sé' si aún no existe un contraste confirmado",
        height=100,
        key=is_not_key,
        on_change=save_question_field,
        args=(question_id, "is_not_value", is_not_key),
    )

known_difference = st.text_area(
    "Diferencia conocida entre ES y NO ES",
    value=saved["known_difference"],
    placeholder="Puede quedar en blanco o escribir 'no sé'. No es obligatorio conocerla todavía.",
    height=80,
    key=difference_key,
    on_change=save_question_field,
    args=(question_id, "known_difference", difference_key),
)
context = st.text_area(
    "Contexto adicional",
    value=saved["context"],
    placeholder="Máquina, turno, PN, proveedor, secuencia, evidencia disponible, información pendiente, etc.",
    height=130,
    key=context_key,
    on_change=save_question_field,
    args=(question_id, "context", context_key),
)

submitted = st.button("✨ Evaluar contraste", use_container_width=True, type="primary")

if submitted:
    # Save the current visible values immediately as an extra safeguard before the API call.
    st.session_state["question_inputs"][question_id].update(
        {
            "is_value": is_value,
            "is_not_value": is_not_value,
            "known_difference": known_difference,
            "context": context,
        }
    )

    if not os.getenv("OPENAI_API_KEY"):
        st.error(
            "No encuentro OPENAI_API_KEY. En Streamlit Community Cloud agrégala en App settings → Secrets."
        )
    elif not problem_statement.strip() or not defect_mode.strip() or not is_value.strip():
        st.warning(
            "Completa al menos Problema general, Modo de falla y ES. NO ES puede ser desconocido."
        )
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
            st.session_state["question_results"][question_id] = result
        except Exception as exc:
            st.error("No pude completar la evaluación.")
            with st.expander("Detalle técnico para diagnóstico"):
                st.code(f"{type(exc).__name__}: {exc}")

# Each question keeps its own latest AI evaluation too.
result = st.session_state["question_results"].get(question_id)
if result is not None:
    st.divider()
    st.subheader("Evaluación del coach")
    st.caption(selected_label)

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Estado de la información", STATUS_LABELS.get(result.status, result.status))
    with c2:
        st.metric(
            "Calidad del contraste",
            QUALITY_LABELS.get(result.contrast_quality, result.contrast_quality),
        )

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

st.divider()
st.caption(f"Modelo configurado: {os.getenv('OPENAI_MODEL', 'gpt-5.6-luna')}")
