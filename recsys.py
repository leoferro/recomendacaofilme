import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


import kagglehub
from kagglehub import KaggleDatasetAdapter


path = kagglehub.dataset_download("ashukr/movie-rating-data")

#Importação de dados
#url = 'https://drive.google.com/file/d/18aipKx0BvJtmFNszS1jbwFZOOEgdrma4/view?usp=sharing'
#url='https://drive.google.com/uc?id=' + url.split('/')[-2]
#dfrat = pd.read_csv(url)
dfrat = pd.read_csv(path+"/ratings.csv")

#url = 'https://drive.google.com/file/d/15h49XIuMDEtf5PAbNKFJ41vZgmSmjT3n/view?usp=sharing'
#url='https://drive.google.com/uc?id=' + url.split('/')[-2]
#dfmov = pd.read_csv(url)
dfmov = pd.read_csv(path+"/movies.csv")


users = dfrat.groupby('userId').agg(cnt = ('movieId','count' ))
valor = users.cnt.quantile(.5)
users = users[ users.cnt > valor]


dfrat = dfrat.merge(users, on = 'userId').drop('cnt', axis=1)
#Criação da tabela de relação entre usuario filme e depois filme e filme
df = pd.pivot_table(dfrat,
                    values= 'rating',
                    index = 'movieId',
                    columns = 'userId',
                    fill_value=0)

cos = pd.DataFrame(cosine_similarity(df))
cos.index=df.index
cos.columns = df.index


def retorna_filme(n:int) -> pd.DataFrame:
    '''
    :param n: Entra o id do filme
    :return: DataFrame da linha correspondete ao filme
    '''
    return dfmov[dfmov['movieId']==n]

def recomenda_filme(n:int, quantidade:int=5) ->pd.DataFrame:
    '''
    :param n: Int - Id do filme
    :param quantidade: Quantidade de recomendações, 5 como padrão.
    :return: DataFrame com os filmes
    '''
    tops = cos.sort_values(n, ascending=False)[n]
    filmes = dfmov[dfmov['movieId'].isin(tops.keys())]
    filmes.loc[:,'proximidade'] = filmes.movieId.apply(lambda x: tops[x])
    return (retorna_filme(n).title.values[0],filmes.sort_values('proximidade', ascending=False).iloc[1:quantidade+1])

def pesquisa_filme(palavra:str)->list:
    palavra = palavra.lower()
    existe = dfmov.title.apply(lambda x : True if palavra in x.lower() else False)
    return dfmov[existe].title.values

def encontra_pelo_nome(nome:str)->int:
    return dfmov[dfmov['title']==nome].movieId.values[0]
