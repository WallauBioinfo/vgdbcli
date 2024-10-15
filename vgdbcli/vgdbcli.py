#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from vgdbcli.model import (
    RotinasNaoSegmentadas,
    RotinasSegmentadas,
    COLUNAS_METADADOS,
    COLUNAS_METADADOS_DTYPES,
    OUTPUT_HEADER,
    COLUNAS_OBRIGATORIAS_METADADO,
    PREFIXO_CONTROLES,
)
from vgdbcli.log import logger
from vgdbcli.utils import (
    calc_idade,
    format_code,
    check_informacao_obrigatoria,
    check_coluna_data,
    check_exclusao_amostras,
    padronize_paciente_genero,
    filtre_amostras_controle,
)
import pandas as pd
import numpy as np
import json

MENSAGEM_ERRO_JSON = """Erro ao extrair informações do arquivo json: {}
Confira se o arquivo json está seguindo o modelo proposto
Em caso de dúvidas, contate a equipe de desenvolvimento."""

MENSAGEM_ERRO_VIRALFLOW = """Erro ao obter resultados do viralflow: {}.
Cheque se o caminho passado em path_rotina no json de input existe.
Em caso de dúvidas, contate a equipe de desenvolvimento."""

MENSAGEM_ERRO_METADADOS = """Erro ao validar as informações de metadados: {}.
Cheque as informações presentes neste arquivo.
Em caso de dúvidas, contate a equipe de desenvolvimento."""

MENSAGEM_ERRO_VGDBCLI = """Erro ao criar o input para vgdbcli: {}.
Cheque as informações presentes nos arquivos de input.
Em caso de dúvidas, contate a equipe de desenvolvimento."""


class ModoGeneralista:
    def get_metadados_df(self, metadados_path: str) -> pd.DataFrame:
        logger.info("Validando informações de metadados.")
        metadados_df = pd.read_csv(
            metadados_path,
            sep=",",
            header=0,
            index_col=False,
            usecols=COLUNAS_METADADOS,
            dtype=COLUNAS_METADADOS_DTYPES,
        )
        assert not (
            metadados_df["cod_amostra"].isnull().any()
            or (metadados_df["cod_amostra"].str.strip() == "").any()
        ), "A coluna 'cod_amostra' contém valores NA ou vazios."
        check_informacao_obrigatoria(
            df=metadados_df, colunas_obrigatorias=COLUNAS_OBRIGATORIAS_METADADO
        )
        check_coluna_data(
            df=metadados_df, column_name= "data_coleta"
        )
        check_coluna_data(
            df=metadados_df, column_name= "paciente_nascimento"
        )
        metadados_df["paciente_genero"] = metadados_df["paciente_genero"].apply(
            padronize_paciente_genero
        )
        return metadados_df


class ModoNaoSegmentado(ModoGeneralista):
    def get_rotinas(self, json_path: str) -> RotinasNaoSegmentadas:
        logger.info("Obtendo informações de rotinas a partir do json de input.")
        rotinas_ns = RotinasNaoSegmentadas()
        with open(json_path) as json_file:
            json_data = json.load(json_file)
            for nome_rotina, dados in json_data.items():
                rotinas_ns.adicionar_rotina(nome_rotina, dados)
        return rotinas_ns

    def get_resultados_viralflow_df(
        self, rotinas_ns: RotinasNaoSegmentadas
    ) -> pd.DataFrame:
        logger.info("Obtendo resultados do viralflow.")
        dataframes = []
        for rotina in rotinas_ns.rotinas:
            dados_rotina = rotinas_ns.rotinas[rotina]
            virus = dados_rotina.virus
            data_rotina = dados_rotina.data_rotina
            primer = dados_rotina.primer
            protocolo = dados_rotina.protocolo
            summary_results = dados_rotina.resultados_viralflow

            run_results = pd.read_csv(
                summary_results,
                sep=",",
                header=0,
                index_col=False
            )
            run_results = filtre_amostras_controle(
                df=run_results, padroes=PREFIXO_CONTROLES
            )
            try:
                run_results = run_results[~run_results["taxon"].str.contains("_minor")]
            except Exception:
                pass
            run_results["corrida"] = rotina
            run_results["cod_amostra"] = run_results["cod"].apply(format_code)
            run_results["virus"] = virus
            run_results["data_corrida"] = data_rotina
            run_results["primer"] = primer
            run_results["protocolo"] = protocolo
            dataframes.append(run_results)

        results_df = pd.concat(dataframes, ignore_index=True)
        return results_df

    def create_ns_vgdbcli_input(
        self,
        resultados_viralflow_df: pd.DataFrame,
        metadados_df: pd.DataFrame,
        unidade: str,
        arquivo_output: str,
    ) -> None:
        logger.info("Criando input de virus não segmentados para vgdbcli.")
        vgdb_df = pd.merge(
            resultados_viralflow_df,
            metadados_df.rename(columns={"linhagem": "linhagem_meta"}),
            on="cod_amostra",
            how="left",
        )
        vgdb_df = check_exclusao_amostras(
            df=vgdb_df, colunas_obrigatorias=COLUNAS_OBRIGATORIAS_METADADO
        )
        # priorização da linhagem vinda dos metadados
        vgdb_df["linhagem"] = vgdb_df["linhagem_meta"].where(
            vgdb_df["linhagem_meta"].notna() & (vgdb_df["linhagem_meta"] != ""),
            vgdb_df["lineage"],
        )
        vgdb_df = vgdb_df.drop(columns=["linhagem_meta"])

        vgdb_df["Unidade (Sigla)"] = unidade
        vgdb_df["paciente_nascimento"] = pd.to_datetime(
            vgdb_df["paciente_nascimento"], format="mixed"
        )
        vgdb_df["idade"] = vgdb_df["paciente_nascimento"].apply(calc_idade)
        vgdb_df["ds_segmento"] = ""
        vgdb_df["submetido"] = np.where(
            vgdb_df["cod_submissao"].notna(), "TRUE", "FALSE"
        )

        vgdb_df = vgdb_df.rename(
            columns={
                "mean_depth_coverage": "avg_depth",
                "coverage_breadth": "cov",
            }
        )
        vgdb_df['idade'] = vgdb_df['idade'].astype('Int64')
        vgdb_df.to_csv(arquivo_output, columns=OUTPUT_HEADER, index=False, date_format='%Y-%m-%d', decimal=".")


class ModoSegmentado(ModoGeneralista):
    def get_rotinas(self, json_path: str) -> RotinasSegmentadas:
        logger.info("Obtendo informações de rotinas a partir do json de input.")
        rotinas_seg = RotinasSegmentadas()
        with open(json_path) as json_file:
            json_data = json.load(json_file)
            for nome_rotina, dados in json_data.items():
                rotinas_seg.adicionar_rotina(nome_rotina, dados)
        return rotinas_seg

    def get_resultados_viralflow_df(
        self, rotinas_ns: RotinasSegmentadas
    ) -> pd.DataFrame:
        logger.info("Obtendo resultados do viralflow.")
        dataframes = []
        for rotina in rotinas_ns.rotinas:
            dados_rotina = rotinas_ns.rotinas[rotina]
            virus = dados_rotina.virus
            data_rotina = dados_rotina.data_rotina
            primer = dados_rotina.primer
            protocolo = dados_rotina.protocolo
            for (
                segmento,
                path_rotina,
            ) in dados_rotina.resultados_viralflow_segmentos.items():
                run_results = pd.read_csv(
                    path_rotina,
                    sep=",",
                    header=0,
                    index_col=False
                )
                run_results = filtre_amostras_controle(
                    df=run_results, padroes=PREFIXO_CONTROLES
                )
                try:
                    run_results = run_results[
                        ~run_results["taxon"].str.contains("_minor")
                    ]
                except Exception:
                    pass
                run_results["corrida"] = rotina
                run_results["cod_amostra"] = run_results["cod"].apply(format_code)
                run_results["virus"] = virus
                run_results["data_corrida"] = data_rotina
                run_results["primer"] = primer
                run_results["protocolo"] = protocolo
                run_results["ds_segmento"] = segmento
                dataframes.append(run_results)

        results_df = pd.concat(dataframes, ignore_index=True)
        return results_df

    def create_seg_vgdbcli_input(
        self,
        resultados_viralflow_df: pd.DataFrame,
        metadados_df: pd.DataFrame,
        unidade: str,
        arquivo_output: str,
    ) -> None:
        logger.info("Criando input de virus segmentados para vgdbcli.")
        vgdb_df = pd.merge(
            resultados_viralflow_df,
            metadados_df.rename(columns={"linhagem": "linhagem_meta"}),
            on="cod_amostra",
            how="left",
        )
        vgdb_df = check_exclusao_amostras(
            df=vgdb_df, colunas_obrigatorias=COLUNAS_OBRIGATORIAS_METADADO
        )
        # priorização da linhagem vinda dos metadados
        vgdb_df["linhagem"] = vgdb_df["linhagem_meta"].where(
            vgdb_df["linhagem_meta"].notna() & (vgdb_df["linhagem_meta"] != ""),
            vgdb_df["lineage"],
        )
        
        vgdb_df = vgdb_df.drop(columns=["linhagem_meta"])

        vgdb_df["Unidade (Sigla)"] = unidade
        vgdb_df["paciente_nascimento"] = pd.to_datetime(
            vgdb_df["paciente_nascimento"], format="mixed"
        )
        vgdb_df["idade"] = vgdb_df["paciente_nascimento"].apply(calc_idade)
        vgdb_df["submetido"] = np.where(
            vgdb_df["cod_submissao"].notna(), "TRUE", "FALSE"
        )

        vgdb_df = vgdb_df.rename(
            columns={
                "mean_depth_coverage": "avg_depth",
                "coverage_breadth": "cov",
            }
        )
        vgdb_df = vgdb_df.sort_values(by=['virus', 'cod_amostra', 'ds_segmento'])
        vgdb_df.to_csv(arquivo_output, columns=OUTPUT_HEADER, index=False, decimal=".")
