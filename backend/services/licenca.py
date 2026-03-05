"""
Serviço de Licenciamento do Restaurante.
Atualmente em modo DEV (sempre válido).
Validação RSA pronta e comentada para viabilização comercial futura.
"""

from typing import Dict, Any, Tuple
from fastapi import HTTPException, status
import logging

# from cryptography.exceptions import InternalError

logger = logging.getLogger(__name__)


class LicencaService:
    """Valida a licença do software."""

    # Em produção real as chaves públicas viriam de um arquivo encriptado
    # ou de uma chave embedada no código ofuscado.
    _PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
(AQUI_VIRA_A_CHAVE_PUBLICA_NO_FUTURO)
-----END PUBLIC KEY-----"""

    @classmethod
    def verificar(cls) -> Tuple[bool, str]:
        """
        Verifica a licença do software.
        Retorna: (E_Valida, Mensagem_De_Status)
        """
        # --- MODO DEV ATUAL (A) ---
        return True, "Licença DEV válida"

        # --- MODO PRODUÇÃO FUTURO (B) ---
        # Como usar:
        # 1. Gerar um par RSA (criptografia assimétrica).
        # 2. A API central de Vendas/Licenças do dev gera uma licença JSON (com os dados do cliente e vencimento).
        # 3. Assina esse JSON usando a CHAVE PRIVADA (que só você tem e nunca fica neste código).
        # 4. Envia payload base64 + assinatura_rsa_base64 pro restaurante (salvo no SQLite em Configuracao).
        # 5. Aqui no código, usamos a CHAVE PÚBLICA (embedada) para checar se:
        #    a) a assinatura corresponde ao JSON (ninguém adulterou).
        #    b) a data_vencimento no JSON ainda é válida.

        # --- CÓDIGO COMENTADO ---
        # import json
        # import base64
        # from datetime import datetime, timezone
        # from cryptography.hazmat.primitives import hashes
        # from cryptography.hazmat.primitives.asymmetric import padding
        # from cryptography.hazmat.primitives.serialization import load_pem_public_key
        # from database import SessionLocal
        # from models import Configuracao
        #
        # db = SessionLocal()
        # try:
        #     licenca_conf = db.query(Configuracao).filter_by(chave="licenca_assinatura").first()
        #     if not licenca_conf or not licenca_conf.valor_json:
        #         return False, "Licença não encontrada."
        #
        #     payload_b64 = licenca_conf.valor_json.get("payload")
        #     signature_b64 = licenca_conf.valor_json.get("signature")
        #
        #     if not payload_b64 or not signature_b64:
        #         return False, "Formato de licença inválido."
        #
        #     try:
        #         payload_bytes = base64.b64decode(payload_b64)
        #         signature_bytes = base64.b64decode(signature_b64)
        #
        #         public_key = load_pem_public_key(cls._PUBLIC_KEY.encode())
        #
        #         # 5a. Valida a assinatura
        #         public_key.verify(
        #             signature_bytes,
        #             payload_bytes,
        #             padding.PKCS1v15(),
        #             hashes.SHA256()
        #         )
        #
        #         # 5b. Valida os dados da licença
        #         dados = json.loads(payload_bytes)
        #         data_vencimento = datetime.fromisoformat(dados['vencimento'])
        #
        #         if datetime.now(timezone.utc) > data_vencimento:
        #             return False, f"Licença expirada em {dados['vencimento']}."
        #
        #         return True, f"Licença válida ({dados['cliente']})."
        #
        #     except Exception as e:
        #         logger.error(f"Falha ao validar licença RSA: {e}")
        #         return False, "Assinatura de licença inválida!"
        # finally:
        #     db.close()


def require_valida_licenca():
    """Dependency para rotas que precisam garantir software licenciado."""
    valida, _ = LicencaService.verificar()
    if not valida:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Licença do software expirada ou inválida. Contate o suporte.",
        )
