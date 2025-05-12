from project import limpar_nome, gerar_nuvem, transcrever_audio
import pytest


def test_limpar_nome():
    nome = 'Vídeo: "Como fazer?" <Tutorial>'
    esperado = 'Vídeo_ _Como fazer__ _Tutorial_'
    assert limpar_nome(nome) == esperado

def test_gerar_nuvem():
    texto = "palavra palavra palavra código python transcrição"
    try:
        gerar_nuvem(texto)
    except Exception:
        pytest.fail("gerar_nuvem() lançou uma exceção inesperada")


def test_transcricao_armstrong():
    texto = transcrever_audio("audios/one_small_step.mp3")
    texto = texto.lower()
    assert "one small step" in texto
    assert "man" in texto