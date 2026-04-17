"""
modules/chatbot.py
─────────────────────────────────────────────────────────────
Módulo de diálogo do Tótem Inteligente FlexMedia.

Responsabilidades:
  1. Receber a mensagem de texto do visitante
  2. Identificar a intenção (saudação, consulta de conteúdo,
     navegação, ajuda, despedida)
  3. Retornar uma resposta contextualizada
  4. Manter um contexto de sessão entre turnos

Arquitetura:
  - Baseado em regras com correspondência por palavras-chave
  - Contexto de sessão armazenado em dicionário (gerenciado
    pelo app.py via st.session_state)
  - Sem dependência de APIs externas — 100% local

Funções públicas:
  iniciar_conversa(nome)         → str (mensagem de boas-vindas)
  processar_mensagem(msg, ctx)   → tuple[str, dict] (resposta, ctx atualizado)
─────────────────────────────────────────────────────────────
"""

import re
from datetime import datetime

# ─────────────────────────────────────────────────────────────
# BASE DE CONHECIMENTO DO TÓTEM
# ─────────────────────────────────────────────────────────────

CONTEUDO = {
    "arte": {
        "descricao": (
            "Nossa galeria de Arte reúne obras dos séculos XVIII ao XXI, "
            "com destaque para pinturas, esculturas e instalações interativas. "
            "Você encontrará trabalhos de artistas brasileiros e internacionais, "
            "organizados por movimento — do Barroco ao Contemporâneo."
        ),
        "destaques": [
            "Galeria Modernista — Piso 1, Ala Norte",
            "Instalação 'Luz e Memória' — Piso 2 (interativa)",
            "Acervo de Gravuras Brasileiras — Piso 3",
        ],
        "horario": "Terça a domingo, das 10h às 18h.",
        "dica": "Dica: chegue cedo aos fins de semana — as instalações interativas têm fila!",
    },
    "ciencia": {
        "descricao": (
            "O espaço de Ciência abriga experimentos interativos sobre física, "
            "química, biologia e astronomia. Ideal para todas as idades, "
            "com demonstrações ao vivo realizadas por mediadores três vezes ao dia."
        ),
        "destaques": [
            "Planetário Digital — Piso 1, Ala Sul (sessões às 11h, 14h e 16h)",
            "Laboratório de Experimentos Abertos — Piso 2",
            "Exposição 'DNA: A Vida em Código' — Piso 3",
        ],
        "horario": "Segunda a domingo, das 9h às 19h.",
        "dica": "Dica: as sessões do planetário esgotam rápido — retire seu ingresso no balcão ao chegar.",
    },
    "historia": {
        "descricao": (
            "A ala de História apresenta a trajetória da civilização humana "
            "desde as primeiras sociedades até o século XXI, com acervos de "
            "artefatos originais, reproduções e painéis interativos com "
            "linha do tempo navegável."
        ),
        "destaques": [
            "Linha do Tempo Interativa — Piso 1 (do Paleolítico ao presente)",
            "Acervo de Documentos Históricos Brasileiros — Piso 2",
            "Exposição 'Grandes Civilizações' — Piso 3",
        ],
        "horario": "Terça a domingo, das 10h às 17h.",
        "dica": "Dica: o guia de áudio está disponível gratuitamente no app do museu.",
    },
    "tecnologia": {
        "descricao": (
            "O setor de Tecnologia é o mais recente do espaço e apresenta "
            "a evolução da computação, inteligência artificial, robótica e "
            "internet das coisas. Conta com protótipos funcionais e "
            "demonstrações de IA em tempo real — incluindo este próprio tótem!"
        ),
        "destaques": [
            "Arena de Robótica — Piso 1 (demos às 11h, 14h e 17h)",
            "Exposição 'História da Computação' — Piso 2",
            "Lab de IA Interativa — Piso 3 (onde você está agora!)",
        ],
        "horario": "Segunda a sábado, das 9h às 20h.",
        "dica": "Dica: a Arena de Robótica aceita visitantes para participar das demos — basta chegar 10 min antes.",
    },
}

INFOS_GERAIS = {
    "ingressos": (
        "Ingressos: entrada gratuita para crianças até 12 anos e idosos acima de 60. "
        "Para demais visitantes: R$ 25 (inteira) e R$ 12,50 (meia-entrada com documento). "
        "Compra antecipada disponível no site oficial."
    ),
    "horario_geral": (
        "O espaço funciona de terça a domingo, das 9h às 19h. "
        "Às segundas-feiras o espaço está fechado para manutenção."
    ),
    "acessibilidade": (
        "O espaço é totalmente acessível: rampas, elevadores e banheiros adaptados "
        "em todos os pisos. Cadeiras de rodas disponíveis gratuitamente na recepção."
    ),
    "estacionamento": (
        "Estacionamento conveniado a 100m da entrada principal. "
        "Primeiras 2 horas: R$ 10. Hora adicional: R$ 5. "
        "Moto: R$ 5 o dia inteiro."
    ),
    "alimentacao": (
        "Café e lanchonete no Piso 1 (abertos das 10h às 17h). "
        "Restaurante no Piso 2 com opções de almoço executivo (12h às 15h). "
        "É permitido trazer lanches próprios para a área externa."
    ),
    "loja": (
        "A loja do museu fica na saída principal e oferece livros, "
        "réplicas de obras, camisetas e souvenirs. "
        "Funcionamento: terça a domingo, das 10h às 18h."
    ),
}


# ─────────────────────────────────────────────────────────────
# DETECÇÃO DE INTENÇÃO
# ─────────────────────────────────────────────────────────────

def _normalizar(texto: str) -> str:
    """Remove acentos e converte para minúsculas para facilitar a correspondência."""
    substituicoes = {
        "á": "a", "à": "a", "ã": "a", "â": "a",
        "é": "e", "ê": "e",
        "í": "i", "î": "i",
        "ó": "o", "õ": "o", "ô": "o",
        "ú": "u", "û": "u",
        "ç": "c",
    }
    texto = texto.lower()
    for orig, sub in substituicoes.items():
        texto = texto.replace(orig, sub)
    return texto


INTENCOES = {
    "saudacao": [
        r"\boi\b", r"\bola\b", r"\bhello\b", r"\bboa tarde\b",
        r"\bbom dia\b", r"\bboa noite\b", r"\btudo bem\b", r"\bei\b",
    ],
    "despedida": [
        r"\btchau\b", r"\bate logo\b", r"\baté logo\b", r"\bfui\b",
        r"\bate mais\b", r"\baté mais\b", r"\bobrigad", r"\bvaleu\b",
    ],
    "ajuda": [
        r"\bajuda\b", r"\bhelp\b", r"\bsocorro\b", r"\bpreciso de\b",
        r"\bo que voce faz\b", r"\bo que voce pode\b", r"\bfuncoes\b",
        r"\bcomo funciona\b", r"\bo que e isso\b",
    ],
    "arte": [
        r"\barte\b", r"\bgaleria\b", r"\bpintura\b", r"\bescultura\b",
        r"\binstalacao\b", r"\bmodernista\b", r"\bartista\b", r"\bexposicao de arte\b",
    ],
    "ciencia": [
        r"\bciencia\b", r"\bfisica\b", r"\bquimica\b", r"\bbiologia\b",
        r"\bplanetario\b", r"\bexperimento\b", r"\blaservatório\b",
        r"\blaboratorio\b", r"\bastronomia\b", r"\bdna\b",
    ],
    "historia": [
        r"\bhistoria\b", r"\bacervo\b", r"\bartifato\b", r"\bdocumento\b",
        r"\bcivil", r"\blinha do tempo\b", r"\bcivilizacao\b", r"\barqueologia\b",
    ],
    "tecnologia": [
        r"\btecnologia\b", r"\brobotica\b", r"\binteligencia artificial\b",
        r"\bia\b", r"\bcomputacao\b", r"\binternet\b", r"\brobo\b",
        r"\btotem\b", r"\bsistema\b", r"\bdigital\b",
    ],
    "ingressos": [
        r"\bingresso\b", r"\bpreco\b", r"\bvalor\b", r"\bpagar\b",
        r"\bgratuito\b", r"\bgratis\b", r"\bmeia entrada\b", r"\bcusto\b",
    ],
    "horario": [
        r"\bhorario\b", r"\bfecha\b", r"\babre\b", r"\bfuncionamento\b",
        r"\bquando\b", r"\bque horas\b",
    ],
    "acessibilidade": [
        r"\bacessib", r"\bcadeira de rodas\b", r"\bdeficiente\b",
        r"\belevador\b", r"\brampa\b",
    ],
    "estacionamento": [
        r"\bestacionamento\b", r"\bvaga\b", r"\bcarro\b", r"\bparkig\b",
        r"\bparkig\b", r"\bmoto\b",
    ],
    "alimentacao": [
        r"\bcomer\b", r"\bcomida\b", r"\blanche\b", r"\brestaurante\b",
        r"\bcafe\b", r"\balmoco\b", r"\bbeber\b", r"\bfome\b",
    ],
    "loja": [
        r"\bloja\b", r"\bsouvenir\b", r"\bpresente\b", r"\bcomprar\b",
        r"\blivro\b", r"\bcamiseta\b",
    ],
}


def _detectar_intencao(texto: str) -> str:
    """Retorna a intenção com maior número de correspondências no texto."""
    texto_norm = _normalizar(texto)
    pontuacoes = {}

    for intencao, padroes in INTENCOES.items():
        score = sum(1 for p in padroes if re.search(p, texto_norm))
        if score > 0:
            pontuacoes[intencao] = score

    if not pontuacoes:
        return "desconhecida"
    return max(pontuacoes, key=pontuacoes.get)


# ─────────────────────────────────────────────────────────────
# GERAÇÃO DE RESPOSTA
# ─────────────────────────────────────────────────────────────

def _resposta_categoria(categoria: str, subtipo: str = None) -> str:
    """Monta resposta completa sobre uma categoria temática."""
    info = CONTEUDO[categoria]

    if subtipo == "destaques":
        destaques = "\n".join(f"  • {d}" for d in info["destaques"])
        return f"Os principais destaques de {categoria.title()} são:\n\n{destaques}"

    if subtipo == "horario":
        return f"Horário de funcionamento — {categoria.title()}: {info['horario']}"

    # Resposta completa padrão
    destaques = "\n".join(f"  • {d}" for d in info["destaques"])
    return (
        f"{info['descricao']}\n\n"
        f"**Destaques:**\n{destaques}\n\n"
        f"🕐 {info['horario']}\n\n"
        f"💡 {info['dica']}"
    )


def _resposta_ajuda() -> str:
    return (
        "Posso te ajudar com as seguintes informações:\n\n"
        "  • **Arte** — galerias, pinturas e instalações\n"
        "  • **Ciência** — planetário, laboratórios e experimentos\n"
        "  • **História** — acervos, artefatos e linha do tempo\n"
        "  • **Tecnologia** — robótica, IA e computação\n"
        "  • **Ingressos** — preços e formas de compra\n"
        "  • **Horários** — funcionamento do espaço\n"
        "  • **Acessibilidade** — recursos para visitantes com necessidades especiais\n"
        "  • **Estacionamento** — valores e localização\n"
        "  • **Alimentação** — café, lanchonete e restaurante\n"
        "  • **Loja** — souvenirs e publicações\n\n"
        "Basta me perguntar sobre qualquer um desses temas! 😊"
    )


# ─────────────────────────────────────────────────────────────
# FUNÇÕES PÚBLICAS
# ─────────────────────────────────────────────────────────────

def iniciar_conversa(nome: str) -> str:
    """
    Retorna a mensagem de boas-vindas personalizada.
    Chamada pelo app.py ao iniciar uma nova sessão de chat.
    """
    hora = datetime.now().hour
    if hora < 12:
        saudacao = "Bom dia"
    elif hora < 18:
        saudacao = "Boa tarde"
    else:
        saudacao = "Boa noite"

    return (
        f"{saudacao}, **{nome}**! 👋 Seja bem-vindo(a) ao Tótem Inteligente FlexMedia.\n\n"
        "Estou aqui para te ajudar a aproveitar ao máximo sua visita. "
        "Você pode me perguntar sobre nossas exposições de **Arte**, **Ciência**, "
        "**História** e **Tecnologia**, ou sobre **ingressos**, **horários**, "
        "**alimentação** e muito mais.\n\n"
        "O que você gostaria de explorar hoje? 🎯"
    )


def processar_mensagem(mensagem: str, contexto: dict) -> tuple[str, dict]:
    """
    Processa a mensagem do visitante e retorna a resposta e o contexto atualizado.

    Parâmetros:
        mensagem  — texto digitado pelo visitante
        contexto  — dicionário de estado da sessão (última categoria, turno, etc.)

    Retorna:
        (resposta: str, contexto_atualizado: dict)

    Exemplo:
        resposta, ctx = processar_mensagem("me fale sobre ciência", {})
        resposta, ctx = processar_mensagem("quais são os destaques?", ctx)
    """
    if not contexto:
        contexto = {"ultima_categoria": None, "turno": 0}

    contexto["turno"] = contexto.get("turno", 0) + 1
    intencao = _detectar_intencao(mensagem)

    # ── Saudação ──
    if intencao == "saudacao":
        resposta = (
            "Olá! 😊 Como posso te ajudar?\n\n"
            "Me pergunte sobre nossas exposições ou serviços — "
            "estou aqui para tornar sua visita ainda melhor!"
        )

    # ── Despedida ──
    elif intencao == "despedida":
        resposta = (
            "Foi um prazer te ajudar! Espero que aproveite muito a visita. "
            "Qualquer dúvida, é só chamar. Até logo! 👋"
        )
        contexto["ultima_categoria"] = None

    # ── Ajuda ──
    elif intencao == "ajuda":
        resposta = _resposta_ajuda()

    # ── Categorias temáticas ──
    elif intencao in CONTEUDO:
        contexto["ultima_categoria"] = intencao
        resposta = _resposta_categoria(intencao)

    # ── Informações gerais ──
    elif intencao in INFOS_GERAIS:
        resposta = INFOS_GERAIS[intencao]
        # Mantém a última categoria no contexto

    # ── Pergunta de acompanhamento (ex: "e os destaques?") ──
    elif intencao == "desconhecida" and contexto.get("ultima_categoria"):
        cat = contexto["ultima_categoria"]
        texto_norm = _normalizar(mensagem)

        if any(p in texto_norm for p in ["destaque", "o que tem", "o que ha", "principal"]):
            resposta = _resposta_categoria(cat, subtipo="destaques")
        elif any(p in texto_norm for p in ["horario", "hora", "quando", "abre", "fecha"]):
            resposta = _resposta_categoria(cat, subtipo="horario")
        elif any(p in texto_norm for p in ["dica", "conselho", "sugestao", "recomend"]):
            resposta = f"💡 {CONTEUDO[cat]['dica']}"
        else:
            resposta = (
                f"Não entendi muito bem. Ainda estamos falando sobre "
                f"**{cat.title()}**. Você quer saber os **destaques**, "
                f"os **horários** ou alguma **dica** específica?"
            )

    # ── Intenção desconhecida sem contexto ──
    else:
        resposta = (
            "Hmm, não tenho certeza sobre isso. 🤔\n\n"
            "Posso te ajudar com informações sobre nossas exposições "
            "(Arte, Ciência, História, Tecnologia) ou serviços como "
            "ingressos, horários e alimentação.\n\n"
            "Digite **ajuda** para ver tudo que posso fazer!"
        )

    return resposta, contexto
