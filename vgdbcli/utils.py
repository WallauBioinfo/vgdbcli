#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import pandas as pd
import re
import json
from vgdbcli.erros import ExecucaoInterrompidaPeloUsuario


def format_code(cod: str) -> str:
    regex = r"_S\d+_L\d+"
    return re.sub(regex, "", cod)


def calc_idade(data_nascimento: str) -> str:
    data_atual = datetime.now()
    idade = (
        data_atual.year
        - data_nascimento.year
        - (
            (data_atual.month, data_atual.day)
            < (data_nascimento.month, data_nascimento.day)
        )
    )
    return idade


def _check_info(df: pd.DataFrame, colunas_obrigatorias: list) -> tuple[dict, dict]:
    info_faltando = {}
    cod_amostras_faltantes = {}

    for column in colunas_obrigatorias:
        missing_rows = df[df[column].isnull()]

        if not missing_rows.empty:
            missing_count = len(missing_rows)
            info_faltando[column] = missing_count
            cod_amostras_faltantes[column] = list(set(missing_rows["cod_amostra"].tolist()))
    return info_faltando, cod_amostras_faltantes


def _salve_json_erros(tracking_de_erros: dict) -> str:
    output_tracking_erros = "vgdbcli.erros.json"
    with open(output_tracking_erros, "w") as output_file:
        json.dump(tracking_de_erros, output_file)
    return output_tracking_erros


def check_informacao_obrigatoria(df: pd.DataFrame, colunas_obrigatorias: list) -> None:
    info_faltando, cod_amostras_faltantes = _check_info(
        df=df, colunas_obrigatorias=colunas_obrigatorias
    )
    if info_faltando:
        summary = []
        total_missing = 0

        for column, count in info_faltando.items():
            summary.append(f"{count} linhas sem informação na coluna '{column}'")
            total_missing += count

        error_message = (
            f"\n\tForam encontrados {total_missing} linhas com informações faltando, sendo:\n\t"
            + "\n\t".join(summary)
        )

        output_tracking_erros = _salve_json_erros(
            tracking_de_erros=cod_amostras_faltantes
        )
        error_message += f"\n\tCheque o arquivo {output_tracking_erros} que contém a relação entre colunas sem informação e amostras"
        raise ValueError(error_message)

def check_coluna_data(df, column_name):
    try:
        pd.to_datetime(df[column_name], format='%Y-%m-%d', errors='raise')
    except Exception:
        raise ValueError(f"A coluna {column_name} deve ter datas no formato YYYY-MM-DD")


def _obter_decisao(frase):
    print(frase)
    while True:
        decisao = input().lower().strip()
        if decisao and decisao[0] in ["s", "n"]:
            return decisao[0]
        else:
            print("Você digitou uma opção inválida, digite s ou n:")


def check_exclusao_amostras(df: pd.DataFrame, colunas_obrigatorias: list) -> None:
    info_faltando, cod_amostras_faltantes = _check_info(
        df=df, colunas_obrigatorias=colunas_obrigatorias
    )
    if len(cod_amostras_faltantes) == 0:
        return df
    for coluna, amostras in cod_amostras_faltantes.items():
        frase = (
            f"A(s) amotra(s) {', '.join(amostras)} está/estão sem informação no arquivo de metadados providenciado.\n"
            + "Você deseja prosseguir com a execução do vgdbcli, sabendo que o arquivo gerado não terá informações da(s) amostra(s) mencioanda(s)?\n"
            + "Digite s ou n:"
        )
        decisao = _obter_decisao(frase)
        if decisao == "s":
            print("Prosseguindo com a execução")
            df_filtrado = df.dropna(subset=colunas_obrigatorias)
            return df_filtrado
        elif decisao.lower().strip()[0] == "n":
            output_tracking_erros = _salve_json_erros(
                tracking_de_erros=cod_amostras_faltantes
            )
            raise ExecucaoInterrompidaPeloUsuario(
                f"O Usuário optou por interromper a execução.\n"
                + f"Cheque o arquivo {output_tracking_erros} e corrija as informações faltantes no arquivo de metadados informado"
            )


def padronize_paciente_genero(paciente_genero: str) -> str:
    if pd.isna(paciente_genero):
        return ""
    elif paciente_genero.startswith(tuple(["M", "m"])):
        return "M"
    elif paciente_genero.startswith(tuple(["F", "f"])):
        return "F"
    return ""


def filtre_amostras_controle(df: pd.DataFrame, padroes: list) -> pd.DataFrame:
    padroes = "|".join(padroes)
    df_filtrado = df[~df["cod"].str.lower().str.contains(padroes, regex=True)]
    return df_filtrado
