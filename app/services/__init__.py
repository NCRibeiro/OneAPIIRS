"""
Módulo de inicialização dos serviços do APE Project.

Este pacote contém serviços internos que encapsulam regras de negócio,
transformações de dados legados e outras operações de apoio.
"""

from .transformer import cobol_to_json

__all__ = ["cobol_to_json"]
