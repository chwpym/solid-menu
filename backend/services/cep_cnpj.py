"""
Serviço de consulta de CEP (ViaCEP) e CNPJ (BrasilAPI).
Com fallback graceful caso esteja offline.
"""

import httpx
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

# Timeout curto para falhar rápido caso o restaurante esteja sem internet
TIMEOUT = 3.0


def consultar_cep(cep: str) -> Optional[Dict[str, Any]]:
    """Consulta CEP no ViaCEP."""
    cep_limpo = "".join(filter(str.isdigit, cep))
    if len(cep_limpo) != 8:
        return None

    try:
        url = f"https://viacep.com.br/ws/{cep_limpo}/json/"
        response = httpx.get(url, timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            if "erro" not in data:
                return {
                    "endereco": data.get("logradouro", ""),
                    "bairro": data.get("bairro", ""),
                    "cidade": data.get("localidade", ""),
                    "estado": data.get("uf", ""),
                }
    except httpx.RequestError as e:
        logger.warning(f"Falha ao consultar CEP (possível modo offline): {e}")
    return None


def consultar_cnpj(cnpj: str) -> Optional[Dict[str, Any]]:
    """Consulta CNPJ na BrasilAPI."""
    cnpj_limpo = "".join(filter(str.isdigit, cnpj))
    if len(cnpj_limpo) != 14:
        return None

    try:
        url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_limpo}"
        response = httpx.get(url, timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            return {
                "razao_social": data.get("razao_social", ""),
                "nome_fantasia": data.get("nome_fantasia", ""),
                "endereco": f"{data.get('logradouro', '')}",
                "numero": data.get("numero", ""),
                "bairro": data.get("bairro", ""),
                "cidade": data.get("municipio", ""),
                "estado": data.get("uf", ""),
                "cep": data.get("cep", ""),
            }
    except httpx.RequestError as e:
        logger.warning(f"Falha ao consultar CNPJ (possível modo offline): {e}")
    return None
