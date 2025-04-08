# =============================
# 💻 Interface do Streamlit
# =============================
if __name__ == "__main__":
    st.set_page_config(layout="wide")  # Deixa a tela mais larga para comportar as colunas

    # Cria três colunas: propaganda esquerda, conteúdo principal, propaganda direita
    col1, col2, col3 = st.columns([1, 4, 1])  # proporção: 1 parte lateral, 4 partes centro

    with col1:
        st.markdown("### 📢 Propaganda")
        st.image("https://via.placeholder.com/120x600?text=Sua+Propaganda+AQUI", use_column_width=True)
        st.markdown("Anuncie conosco! ✉️")

    with col2:
        st.title("PlagIA - PEAS.Co")

        st.subheader("📋 Registro de Usuário - Apenas para validação")
        nome = st.text_input("Nome completo")
        email = st.text_input("E-mail")

        if st.button("Salvar Dados"):
            if nome and email:
                salvar_email_google_sheets(nome, email, "N/A")
            else:
                st.warning("⚠️ Por favor, preencha todos os campos.")

        # Upload do PDF após registro
        arquivo_pdf = st.file_uploader("Faça upload de um arquivo PDF SEM OS NOMES DOS AUTORES E TÍTULO DA REVISTA, PARA GARANTIR AVALIAÇÃO SOMENTE DO TEXTO", type=["pdf"])

        if st.button("Processar PDF"):
            if arquivo_pdf is not None:
                texto_usuario = extrair_texto_pdf(arquivo_pdf)
                referencias = buscar_referencias_crossref(texto_usuario)

                referencias_com_similaridade = []
                for ref in referencias:
                    texto_base = ref["titulo"] + " " + ref["resumo"]
                    link = ref["link"]
                    similaridade = calcular_similaridade(texto_usuario, texto_base)
                    referencias_com_similaridade.append((ref["titulo"], similaridade, link))

                referencias_com_similaridade.sort(key=lambda x: x[1], reverse=True)

                if referencias_com_similaridade:
                    codigo_verificacao = gerar_codigo_verificacao(texto_usuario)
                    salvar_email_google_sheets(nome, email, codigo_verificacao)

                    st.success(f"Código de verificação gerado: **{codigo_verificacao}**")

                    # Gerar e exibir link para download do relatório
                    pdf_file = gerar_relatorio_pdf(referencias_com_similaridade, nome, email, codigo_verificacao)
                    with open(pdf_file, "rb") as f:
                        st.download_button("📄 Baixar Relatório de Plágio", f, "relatorio_plagio.pdf")
                else:
                    st.warning("Nenhuma referência encontrada.")
            else:
                st.error("Por favor, carregue um arquivo PDF.")

        # Texto explicativo ao final da página
        st.markdown("""
        ---
        A PEAS.Co trabalha sem recursos governamentais ou privados, apenas de doações. Nos ajude com um PIX de qualquer valor: **peas8810@gmail.com**.
        
        Tem alguma ideia de programa com IA? Nos envie um e-mail que tentaremos fazer juntos!

        Nosso avançado programa de detecção de plágio utiliza inteligência artificial para comparar textos com uma ampla base de dados composta pelos 100 maiores indexadores e repositórios globais, analisando cuidadosamente as similaridades encontradas.

        Para mais informações sobre práticas de integridade acadêmica, acesse [plagiarism.org](https://plagiarism.org).  
        **Powered By - PEAS.Co**
        """)

        st.header("Verificar Autenticidade")
        codigo_digitado = st.text_input("Digite o código de verificação:")

        if st.button("Verificar Código"):
            if verificar_codigo_google_sheets(codigo_digitado):
                st.success("✅ Documento Autêntico e Original!")
            else:
                st.error("❌ Código inválido ou documento falsificado.")

    with col3:
        st.markdown("### 📢 Propaganda")
        st.image("https://via.placeholder.com/120x600?text=Anuncie+Aqui", use_column_width=True)
        st.markdown("Entre em contato 📞")
