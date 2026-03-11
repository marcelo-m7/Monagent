from abstra.forms import (
    TextInput,
    EmailInput,
    PhoneInput,
    DateInput,
    DropdownInput,
    NumberInput,
    TextareaInput,
    MarkdownOutput,
    run
)
from abstra.tables import insert
from datetime import datetime

print("=== Iniciando Formulário de Cadastro de Cliente ===")

# Página 1: Informações Pessoais
pagina_dados_pessoais = [
    MarkdownOutput("""
# 📝 Cadastro de Cliente

Preencha as informações abaixo para cadastrar um novo cliente.
    """),
    TextInput(
        key="nome",
        label="Nome Completo",
        placeholder="Digite o nome completo",
        required=True
    ),
    EmailInput(
        key="email",
        label="E-mail",
        placeholder="exemplo@email.com",
        required=True
    ),
    PhoneInput(
        key="telefone",
        label="Telefone",
        placeholder="(00) 00000-0000",
        required=True
    ),
    DateInput(
        key="data_nascimento",
        label="Data de Nascimento",
        required=False
    )
]

# Página 2: Informações Profissionais
pagina_dados_profissionais = [
    MarkdownOutput("""
# 💼 Informações Profissionais
    """),
    TextInput(
        key="empresa",
        label="Empresa",
        placeholder="Nome da empresa",
        required=False
    ),
    DropdownInput(
        key="cargo",
        label="Cargo",
        options=[
            "Analista",
            "Gerente",
            "Diretor",
            "CEO",
            "Estagiário",
            "Outro"
        ],
        required=False
    ),
    NumberInput(
        key="salario",
        label="Faixa Salarial (R$)",
        placeholder="5000.00",
        required=False
    )
]

# Página 3: Endereço
pagina_endereco = [
    MarkdownOutput("""
# 📍 Endereço
    """),
    TextInput(
        key="cep",
        label="CEP",
        placeholder="00000-000",
        required=False
    ),
    TextInput(
        key="logradouro",
        label="Logradouro",
        placeholder="Rua, Avenida, etc.",
        required=False
    ),
    TextInput(
        key="numero",
        label="Número",
        placeholder="123",
        required=False
    ),
    TextInput(
        key="complemento",
        label="Complemento",
        placeholder="Apto, Bloco, etc.",
        required=False
    ),
    TextInput(
        key="cidade",
        label="Cidade",
        placeholder="São Paulo",
        required=False
    ),
    TextInput(
        key="estado",
        label="Estado",
        placeholder="SP",
        required=False
    )
]

# Página 4: Observações
pagina_observacoes = [
    MarkdownOutput("""
# 📝 Observações
    """),
    TextareaInput(
        key="observacoes",
        label="Observações Adicionais",
        placeholder="Digite aqui qualquer informação complementar...",
        required=False
    )
]

# Executa o formulário com múltiplas páginas
state = run([
    pagina_dados_pessoais,
    pagina_dados_profissionais,
    pagina_endereco,
    pagina_observacoes
], state={})

print(f"Dados coletados: {state}")

# Extrai o valor do telefone (PhoneResponse ou string)
telefone = state["telefone"]
if hasattr(telefone, 'raw'):
    telefone = telefone.raw

# Extrai o valor da data de nascimento (date ou None)
data_nascimento = state.get("data_nascimento")
if data_nascimento is not None:
    data_nascimento = str(data_nascimento)

# Salva os dados no banco de dados
cliente_id = insert("clientes", {
    "nome": state["nome"],
    "email": state["email"],
    "telefone": telefone,
    "data_nascimento": data_nascimento,
    "empresa": state.get("empresa"),
    "cargo": state.get("cargo"),
    "salario": state.get("salario"),
    "cep": state.get("cep"),
    "logradouro": state.get("logradouro"),
    "numero": state.get("numero"),
    "complemento": state.get("complemento"),
    "cidade": state.get("cidade"),
    "estado": state.get("estado"),
    "observacoes": state.get("observacoes"),
    "data_cadastro": datetime.now()
})

print(f"Cliente cadastrado com ID: {cliente_id}")

# Página de confirmação
pagina_confirmacao = [
    MarkdownOutput(f"""
# ✅ Cadastro Realizado com Sucesso!

O cliente **{state['nome']}** foi cadastrado com sucesso.

**Resumo do cadastro:**
- 📧 E-mail: {state['email']}
- 📱 Telefone: {state['telefone']}
- 🏢 Empresa: {state.get('empresa', 'Não informado')}
- 💼 Cargo: {state.get('cargo', 'Não informado')}

Obrigado por utilizar nosso sistema!
    """)
]

run([pagina_confirmacao])

print("=== Formulário Finalizado ===")
