import os
import pandas as pd
from config.logging import logger
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY


# Definir caminhos relativos à raiz do projeto
PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
DIRETORIO_DOWNLOADS = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "downloads"))
DIRETORIO_UPLOADS = os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "uploads"))

# Criar diretórios se não existirem
os.makedirs(DIRETORIO_DOWNLOADS, exist_ok=True)
os.makedirs(DIRETORIO_UPLOADS, exist_ok=True)


def obter_arquivo_mais_recente(diretorio, extensoes):
    """
        Retorna o caminho do arquivo mais recente dentro do diretório especificado.
        
        :param diretorio: Caminho do diretório onde buscar os arquivos.
        :param extensoes: Lista de extensões de arquivos para considerar.
        :return: Caminho do arquivo mais recente ou None se não houver arquivos.
    """
    try:
        arquivos = [f for f in os.listdir(diretorio) if f.lower().endswith(tuple(extensoes))]
        if not arquivos:
            logger.error(f"Nenhum arquivo {extensoes} encontrado em {diretorio}.")
            return None

        arquivo_recente = max(
            arquivos,
            key=lambda x: os.path.getctime(os.path.join(diretorio, x))
        )
        return os.path.join(diretorio, arquivo_recente)
    
    except Exception as e:
        logger.error(f"Erro ao obter o arquivo mais recente em {diretorio}: {e}")
        return None


def ler_arquivos():
    """
        Lê os arquivos mais recentes dos diretórios downloads e uploads.
        
        :return: DataFrames dos arquivos lidos ou None se ocorrer erro.
    """
    try:
        path_desativados = obter_arquivo_mais_recente(DIRETORIO_DOWNLOADS, [".csv"])
        path_cadastrados = obter_arquivo_mais_recente(DIRETORIO_UPLOADS, [".xls", ".csv"])

        if not path_desativados or not path_cadastrados:
            raise FileNotFoundError("Não foi possível encontrar os arquivos necessários.")

        df_desativados = pd.read_csv(
            path_desativados,
            encoding="utf-8",
            sep=";",
            dtype={
                "Telefone residencial": str,
                "Celular": str
            }
        )

        if path_cadastrados.endswith(".xls"):
            df_cadastrados = pd.read_excel(
                path_cadastrados, 
                engine="xlrd", 
                dtype={"TelefoneCelular": str})
        elif path_cadastrados.endswith(".xlsx"):
            df_cadastrados = pd.read_excel(
                path_cadastrados, 
                engine="openpyxl", 
                dtype={"TelefoneCelular": str})
        else:
            df_cadastrados = pd.read_csv(
                path_cadastrados, 
                encoding="utf-8", 
                sep=";", 
                dtype={"TelefoneCelular": str})

        return df_desativados, df_cadastrados
    
    except FileNotFoundError as e:
        logger.error(f"Erro ao ler arquivos: {e}")
    except pd.errors.ParserError as e:
        logger.error(f"Erro ao processar arquivos CSV/XLS: {e}")
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")

    return None, None

def encontrar_interseccao(df_desativados, df_cadastrados):
    """
    Encontra os elementos em comum nos dois datasets com base no Código e Nome,
    e retorna as colunas 'Código', 'Nome' e 'TelefoneCelular' combinada.

    :param df_desativados: DataFrame com os dados de desativados.
    :param df_cadastrados: DataFrame com os dados de cadastrados.
    :return: DataFrame com a interseção dos dois datasets.
    """
    try:
        df_cadastrados.drop("TelefoneCelular", axis=1, inplace=True)

        # Encontrar interseção com base no Código e Nome
        df_interseccao = pd.merge(df_desativados[["Nome", "Telefone residencial", "Celular"]],
                                  df_cadastrados[["Código", "Nome"]],
                                  on=["Nome"], how="inner")

        # Criar a coluna TelefoneCelular combinando 'Telefone residencial' e 'Celular'
        df_interseccao["TelefoneCelular"] = df_interseccao[["Telefone residencial", "Celular"]].apply(
            lambda x: ", ".join(x.dropna().astype(str)) if any(pd.notna(x)) else None, axis=1
        )

        # Selecionar as colunas finais
        df_interseccao = df_interseccao[["Código", "Nome", "TelefoneCelular"]]

        return df_interseccao

    except Exception as e:
        print(f"Erro ao encontrar interseção: {e}")
        return None
    
def df_para_pdf(df, nome_pdf="dataframe.pdf"):
    """
    Converte um DataFrame em um arquivo PDF e salva no diretório 'pdf'.
    """
    try:
        pdf_dir = os.path.join(PATH, "pdf")
        if not os.path.exists(pdf_dir):
            os.makedirs(pdf_dir)
        
        pdf_path = os.path.join(pdf_dir, nome_pdf)
        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=A4,
            rightMargin=30,
            leftMargin=30,
            topMargin=30,
            bottomMargin=30
        )
        
        elements = []
        styles = getSampleStyleSheet()
        justified_style = ParagraphStyle(
            name='Justified',
            parent=styles['Normal'],
            alignment=TA_JUSTIFY,
            fontName='Times-Roman',
            fontSize=12
        )
        
        data = []
        data.append(['ID', 'Código', 'Nome', 'TelefoneCelular'])
        
        for i, (_, row) in enumerate(df.iterrows(), 1):
            data_row = [
                str(i),
                str(row['Código']),
                Paragraph(str(row['Nome']), justified_style),
                str(row['TelefoneCelular'])
            ]
            data.append(data_row)
        
        page_width = A4[0]
        margin = 30
        available_width = page_width - (2 * margin)
        
        col_widths = [
            available_width * 0.1,  # 10% para ID
            available_width * 0.2,  # 20% para Código
            available_width * 0.4,  # 40% para Nome
            available_width * 0.3   # 30% para TelefoneCelular
        ]
        
        table = Table(data, colWidths=col_widths, repeatRows=1)
        
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),  # Cabeçalho em negrito
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),  # ID centralizado
            ('ALIGN', (1, 1), (1, -1), 'CENTER'),  # Código centralizado
            ('ALIGN', (3, 1), (3, -1), 'CENTER'),  # TelefoneCelular centralizado
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('WORDWRAP', (0, 0), (-1, -1), True),
        ]))
        
        elements.append(table)
        doc.build(elements)
        
        print(f"PDF salvo com sucesso em: {pdf_path}")
    
    except Exception as e:
        print(f"Erro ao gerar o PDF: {e}")
