import requests
import json
from flask import session

""" 
Para requisições no MusicBrainz não é necessário login ou token de autenticação 
Api é aberta, basta apenas passar os parâmetros 
URLS serão separadas de acordo com a necessidade de pesquisa 
"""

# Pesquisa de artista 
#usando o MusicBrainz

def busArtista(artistName):

    requestURL = requests.get('https://musicbrainz.org/ws/2/artist/?query=artist:'+str(artistName)+'&fmt=json')

    retorno = json.loads(requestURL.content)

    if retorno['count'] != 0:
        artistIdReturn = retorno['artists'][0]['id']
        artistNameReturn = retorno['artists'][0]['name']
        artistType = retorno['artists'][0]['type']
    else:
        artistIdReturn = 'null'
        artistNameReturn = 'Ainda não conseguimos encontrar essa estrela para você! :('
        artistType = 'null'

    session['artistId'] = artistIdReturn
    session['artistName'] = artistNameReturn
    session['artistType'] = artistType

    return artistNameReturn 

def buscaDiscos():

    artistIdReturn = session['artistId']

    if artistIdReturn != 'null':

        requestURL = requests.get(f'https://musicbrainz.org/ws/2/artist/{artistIdReturn}/releases?inc=release-groups&fmt=json')

        retorno = json.loads(requestURL.content)

        albunsStudioName = []
        albunsStudioReleaseDate = []
        albunsStudioId = []
        albunsStudioRelease = []
        dataBr = []

        for release in retorno['release-groups']:
            if len(release['secondary-types']) == 0 and release['primary-type'] == 'Album':
                albunsStudioName.append(release['title'])
                albunsStudioReleaseDate.append(release['first-release-date'])
                albunsStudioId.append(release['id'])

        for data in albunsStudioReleaseDate:
            if '-' in data:
                ano, mes, dia = data.split('-')
                dataBr.append(f'{dia}-{mes}-{ano}')

        for i, (albunsStudioName, dataBr, albunsStudioId) in enumerate(zip(albunsStudioName, dataBr, albunsStudioId), start=1):
            dictAlbunsStudio = {'Nome': albunsStudioName, 'Lancamento': dataBr, 'Capas': f'https://coverartarchive.org/release-group/{albunsStudioId}/front'}
            albunsStudioRelease.append(dictAlbunsStudio)

        return albunsStudioRelease
    
    else:
        Erro = {'Erro': 'Nenhum artista encontrado'}
        return Erro