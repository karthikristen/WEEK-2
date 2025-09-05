# ---- TAB 3 ----
with tabs[2]:
    st.subheader("⚠️ Dangers of Radioactive Water")

    # Image
    st.image("radioactive_process.png", caption="Radioactive Contamination Process", use_column_width=True)

    # ---- Health Risks ----
    st.markdown(
        """
        <div style="background-color:#1a1a1a; padding:15px; border-radius:12px; margin-bottom:10px;">
        <h4 style="color:#FFD300;">☢️ Health Risks</h4>
        <ul style="color:#e8f5e9;">
        <li><b>Cancer:</b> Long-term exposure to radioactive elements like uranium and radium can increase cancer risk. 
        <a href="https://ensia.com/features/radioactive-contamination-drinking-water-radium-radon-uranium/?utm_source=chatgpt.com" target="_blank" style="color:#39FF14;">[Read More]</a></li>
        <li><b>Organ Damage:</b> Can lead to kidney and liver dysfunction. 
        <a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC3261972/?utm_source=chatgpt.com" target="_blank" style="color:#39FF14;">[Study]</a></li>
        <li><b>Genetic Mutations:</b> May affect future generations. 
        <a href="https://link.springer.com/chapter/10.1007/978-3-031-89591-3_10?utm_source=chatgpt.com" target="_blank" style="color:#39FF14;">[Reference]</a></li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---- Environmental Impact ----
    st.markdown(
        """
        <div style="background-color:#1a1a1a; padding:15px; border-radius:12px; margin-bottom:10px;">
        <h4 style="color:#FF7518;">🌍 Environmental Impact</h4>
        <ul style="color:#e8f5e9;">
        <li><b>Bioaccumulation:</b> Radioactive isotopes can accumulate in plants and animals. 
        <a href="https://ensia.com/features/radioactive-contamination-drinking-water-radium-radon-uranium/?utm_source=chatgpt.com" target="_blank" style="color:#39FF14;">[Read More]</a></li>
        <li><b>Ecosystem Disruption:</b> Contaminated water affects biodiversity.</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---- WHO Guidelines ----
    st.markdown(
        """
        <div style="background-color:#1a1a1a; padding:15px; border-radius:12px; margin-bottom:10px;">
        <h4 style="color:#39FF14;">🛡️ WHO Guidelines</h4>
        <ul style="color:#e8f5e9;">
        <li><a href="https://apps.who.int/iris/bitstream/handle/10665/44584/9789241548151_eng.pdf?utm_source=chatgpt.com" target="_blank" style="color:#FFD300;"><b>WHO Guidelines for Drinking-water Quality</b></a></li>
        <li><a href="https://cdn.who.int/media/docs/default-source/wash-documents/water-safety-and-quality/dwq-guidelines-4/gdwq4-with-add1-chap9.pdf?sfvrsn=6fc78cae_3&utm_source=chatgpt.com" target="_blank" style="color:#FFD300;"><b>Chapter 9: Radiological Aspects</b></a></li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---- Further Reading ----
    st.markdown(
        """
        <div style="background-color:#1a1a1a; padding:15px; border-radius:12px;">
        <h4 style="color:#FFD300;">📚 Further Reading</h4>
        <ul style="color:#e8f5e9;">
        <li><a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC3261972/?utm_source=chatgpt.com" target="_blank" style="color:#39FF14;">Health Effects of Naturally Radioactive Water Ingestion</a></li>
        <li><a href="https://www.ncbi.nlm.nih.gov/books/NBK234160/?utm_source=chatgpt.com" target="_blank" style="color:#39FF14;">Radioactive Contaminants in Drinking Water and Their Health Effects</a></li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info("ℹ️ Stay informed and take action to ensure safe drinking water.")
