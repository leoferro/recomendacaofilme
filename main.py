from recsys import recomenda_filme, pesquisa_filme, encontra_pelo_nome
import streamlit as st


if __name__ == '__main__':
    st.title('Recomendação de filme')
    texto_filme = st.text_input('Busque um filme')
    busca_filme = pesquisa_filme(texto_filme)
    filme_encontrado=''
    if texto_filme!='':
        if len(busca_filme)>0:
            filme_encontrado = st.selectbox('Filmes encontrados:',
                     busca_filme)
        else:
            st.subheader('Filme não encontrado')
    if filme_encontrado!='':
        id_filme = encontra_pelo_nome(filme_encontrado)
        film, rec = recomenda_filme(id_filme)
        st.dataframe(rec)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
