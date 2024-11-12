#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from typing import Dict

VIRUS_ACEITAVEIS = [
    "DENV-1",
    "DENV-2",
    "DENV-3",
    "DENV-4",
    "OROPOUCHE",
    "CHIKUNGUNYA",
    "ZIKV",
    "SARS-CoV-2",
    "MPOX1a",
    "MPOX1b",
    "MPOX2a",
    "MPOX2b",
    "VSR-A",
    "VSR-B",
    "FluA-H3",
    "FluA-H1",
    "FluB-Vic",
]

COLUNAS_METADADOS = [
    "cod_amostra",
    "uf",
    "municipio",
    "lab_origem",
    "data_coleta",
    "paciente_genero",
    "paciente_nascimento",
    "gal_fiocruz",
    "gal_lacen",
    "linhagem",
    "banco_de_dados",
    "cod_submissao",
    "gisaid_virus_name",
    "ds_fonte_coleta"
]

COLUNAS_METADADOS_DTYPES = {
    "cod_amostra": str,
    "uf": str,
    "municipio": str,
    "lab_origem": str,
    "data_coleta": str,
    "paciente_genero": str,
    "paciente_nascimento": str,
    "gal_fiocruz": str,
    "gal_lacen": str,
    "linhagem": str,
    "banco_de_dados": str,
    "cod_submissao": str,
    "gisaid_virus_name": str,
    "ds_fonte_coleta": str
}

COLUNAS_OBRIGATORIAS_METADADO = ["uf", "lab_origem", "data_coleta"]

OUTPUT_HEADER = output_header = [
    "Unidade (Sigla)",
    "cod_amostra",
    "virus",
    "uf",
    "municipio",
    "lab_origem",
    "data_coleta",
    "paciente_genero",
    "paciente_nascimento",
    "idade",
    "gal_fiocruz",
    "gal_lacen",
    "corrida",
    "data_corrida",
    "primer",
    "protocolo",
    "ds_segmento",
    "linhagem",
    "cov",
    "avg_depth",
    "submetido",
    "banco_de_dados",
    "cod_submissao",
    "gisaid_virus_name",
    "ds_fonte_coleta"
]

PREFIXO_CONTROLES = ["control", "cneg", "c-neg", "c_neg", "undetermined"]


def _check_virus(virus: str) -> None:
    if virus not in VIRUS_ACEITAVEIS:
        raise ValueError(
            f"O valor '{virus}' não é válido para o atributo 'virus'. "
            f"Os valores permitidos são: {', '.join(VIRUS_ACEITAVEIS)}"
        )

@dataclass
class AnaliseNaoSegmentada:
    """
    Modelo para validação do input do comando ns
    """

    virus: str
    data_rotina: str
    primer: str
    protocolo: str
    resultados_viralflow: str

    def __post_init__(self):
        _check_virus(self.virus)


@dataclass
class AnaliseSegmentada:
    """
    Modelo para validação do input do comando seg
    """

    virus: str
    data_rotina: str
    primer: str
    protocolo: str
    resultados_viralflow_segmentos: dict

    def __post_init__(self):
        _check_virus(self.virus)


@dataclass
class RotinasNaoSegmentadas:
    rotinas: Dict[str, AnaliseNaoSegmentada] = field(default_factory=dict)

    def adicionar_rotina(self, nome_rotina: str, dados_rotina: Dict) -> None:
        self.rotinas[nome_rotina] = AnaliseNaoSegmentada(**dados_rotina)


@dataclass
class RotinasSegmentadas:
    rotinas: Dict[str, AnaliseSegmentada] = field(default_factory=dict)

    def adicionar_rotina(self, nome_rotina: str, dados_rotina: Dict) -> None:
        self.rotinas[nome_rotina] = AnaliseSegmentada(**dados_rotina)
