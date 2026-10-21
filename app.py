import time
from pathlib import Path

import pandas as pd
import streamlit as st

from generator import generate_marketing_copy
from batch import process_batch, validate_batch_data
from prompts import SUPPORTED_PLATFORMS, SUPPORTED_TONES

st.set_page_config(page_title="CopyCraft AI", page_icon="âœ¨", layout="wide")

css_path = Path(__file__).with_name("style.css")
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


# SIDEBAR NAVIGATION

with st.sidebar:
    st.markdown("## CopyCraft")
    st.caption("AI Writing Studio")
    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Create Copy",
            "Batch Generate",
            "History",
            "About"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### Generation Settings")

    temperature = st.slider(
        "Temperature (Creativity)",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1
    )

    top_p = st.slider(
        "Top-P (Diversity)",
        min_value=0.1,
        max_value=1.0,
        value=0.9,
        step=0.1
    )

    st.info(
        "Adjust creativity and diversity to customize "
        "your marketing copy."
    )

    st.divider()
    st.caption("AI-Powered Marketing")
    st.caption("Powered by Google Gemini")


# MINIMALIST HERO BANNER

st.markdown(
    """
<div class="hero-banner">
<div class="hero-eyebrow">COPYCRAFT / AI WRITING STUDIO</div>
<div class="hero-title">Create content that converts.</div>
<p class="hero-description">
Generate professional marketing copy tailored to your
product, platform, and brand voice.
</p>
</div>
""",
    unsafe_allow_html=True
)



st.divider()

# PAGE NAVIGATION

if page == "Create Copy":

    st.markdown("### AI Copywriting Workspace")

    left_col, right_col = st.columns([1, 1], gap="large")

    # LEFT PANEL â€” CONTENT GENERATION

    with left_col:
        st.markdown("### Create Marketing Copy")
        st.caption(
            "Enter your product details to generate professional marketing content."
        )

        with st.form("copywriting_form"):
            product_name = st.text_input(
                "Product Name *",
                placeholder="e.g. Wireless Headphones"
            )

            description = st.text_area(
                "Product Description *",
                placeholder="Describe your product's features and benefits...",
                height=155
            )

            platform_col, tone_col = st.columns(2)

            with platform_col:
                platform = st.selectbox(
                    "Target Platform",
                    SUPPORTED_PLATFORMS
                )

            with tone_col:
                tone = st.selectbox(
                    "Writing Tone",
                    SUPPORTED_TONES
                )
            submitted = st.form_submit_button(
                "Generate Copy",
                type="primary",
                use_container_width=True
            )

    # GENERATION LOGIC

    if submitted:
        if not product_name.strip() or not description.strip():
            st.warning(
                "Please enter a product name and description."
            )
        else:
            with st.spinner("Generating marketing content..."):
                try:
                    start_time = time.perf_counter()

                    result = generate_marketing_copy(
                        product_name=product_name.strip(),
                        description=description.strip(),
                        platform=platform,
                        tone=tone,
                        temperature=temperature,
                        top_p=top_p
                    )

                    generation_time = (
                        time.perf_counter() - start_time
                    )

                    st.session_state["generated_copy"] = result
                    st.session_state["last_platform"] = platform
                    st.session_state["generation_time"] = generation_time

                    st.session_state.setdefault(
                        "history", []
                    ).append({
                        "product": product_name.strip(),
                        "platform": platform,
                        "tone": tone,
                        "content": result,
                        "time_seconds": round(generation_time, 2)
                    })

                    st.rerun()

                except Exception as error:
                    st.error(
                        f"Generation failed: {error}"
                    )

    # RIGHT PANEL â€” GENERATED CONTENT

    with right_col:
        st.markdown("### Generated Content")

        st.caption(
            "Your personalized marketing content will appear here."
        )

        if "generated_copy" in st.session_state:

            st.success("Generated successfully")

            st.caption(
                f"Generated in "
                f"{st.session_state.get('generation_time', 0):.2f} seconds"
            )

            st.markdown(
                f"**Platform:** "
                f"{st.session_state.get('last_platform', 'N/A')}"
            )

            st.text_area(
                "Generated Content",
                value=st.session_state["generated_copy"],
                height=340
            )

            st.download_button(
                "Download Copy",
                data=st.session_state["generated_copy"],
                file_name="copycraft_marketing_copy.txt",
                mime="text/plain",
                use_container_width=True
            )

        else:

            st.markdown(
                """
<div class="output-card">
<h3>Nothing generated yet</h3>
<p>
Enter your product details, select a platform and tone,
then click Generate Copy to get started.
</p>
</div>
""",
                unsafe_allow_html=True
            )


# BATCH GENERATION PAGE


# BATCH GENERATION PAGE

elif page == "Batch Generate":

    st.markdown("## Batch Content Generation")

    st.caption(
        "Upload a CSV file to generate marketing content "
        "for multiple products."
    )

    st.markdown("### Upload Product Data")

    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"],
        key="batch_csv"
    )

    st.caption(
        "Required columns: product_name, description, platform, tone"
    )

    if uploaded_file is not None:

        try:
            df = pd.read_csv(uploaded_file)

            validate_batch_data(df)

            st.success(
                f"CSV validated successfully. "
                f"{len(df)} products found."
            )

            st.markdown("### Product Preview")

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            st.markdown("### Generation Settings")

            st.write(
                f"Temperature: {temperature:.2f} | "
                f"Top-P: {top_p:.2f}"
            )

            generate_batch = st.button(
                "Generate Batch Content",
                type="primary",
                use_container_width=True
            )

            if generate_batch:

                progress_bar = st.progress(0)

                status_text = st.empty()

                def update_progress(current, total):
                    progress_bar.progress(current / total)

                    status_text.text(
                        f"Processing product {current} of {total}"
                    )

                with st.spinner(
                    "Generating marketing content..."
                ):

                    results = process_batch(
                        df=df,
                        temperature=temperature,
                        top_p=top_p,
                        progress_callback=update_progress
                    )

                st.session_state["batch_results"] = results

                st.success(
                    "Batch processing finished."
                )

            if "batch_results" in st.session_state:

                results = st.session_state["batch_results"]

                st.markdown("### Generation Results")

                successful = (
                    results["status"] == "Success"
                ).sum()

                failed = (
                    results["status"] == "Failed"
                ).sum()

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Total Products",
                        len(results)
                    )

                with col2:
                    st.metric(
                        "Successful",
                        int(successful)
                    )

                with col3:
                    st.metric(
                        "Failed",
                        int(failed)
                    )

                st.dataframe(
                    results,
                    use_container_width=True,
                    hide_index=True
                )

                csv_data = results.to_csv(
                    index=False
                ).encode("utf-8-sig")

                st.download_button(
                    "Download Batch Results",
                    data=csv_data,
                    file_name="copycraft_batch_results.csv",
                    mime="text/csv",
                    use_container_width=True
                )

        except Exception as error:

            st.error(
                f"Batch operation failed: {error}"
            )



# GENERATION HISTORY PAGE

elif page == "History":

    st.markdown("## Generation History")

    history = st.session_state.get("history", [])

    if history:
        for item in reversed(history):

            with st.expander(
                f"{item['product']} - {item['platform']}"
            ):

                st.caption(
                    f"Tone: {item['tone']} | "
                    f"Generation Time: {item['time_seconds']:.2f} seconds"
                )

                st.write(item["content"])

    else:
        st.info(
            "No generation history available yet. "
            "Generate marketing copy to create your first entry."
        )

    st.caption(
        "Generation history is stored for the current session only."
    )


# ABOUT PAGE

elif page == "About":

    st.markdown("## About CopyCraft AI")

    st.write(
        "CopyCraft AI is an automated copywriting and "
        "tone transformation application powered by "
        "Google Gemini."
    )

    st.markdown(
        """
### Current Features

- Platform-specific marketing copy generation
- Multiple writing tones
- Adjustable creativity controls
- AI-powered content generation
- Marketing copy downloads
- Session-based generation history
- CSV upload and preview

### Technology Stack

- Python
- Streamlit
- Google Gemini API
- Pandas

### Project Information

**Project:** Automated Copywriting and Tone Transformer

**Program:** DecodeLabs Generative AI Industrial Training

**Year:** 2026
"""
    )


# FOOTER

st.divider()

st.markdown(
    """
<div class="footer">
CopyCraft AI | Built with Python, Streamlit &amp; Google Gemini |
DecodeLabs 2026
</div>
""",
    unsafe_allow_html=True
)
