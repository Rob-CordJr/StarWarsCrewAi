from langchain_google_vertexai import VertexAI, ChatVertexAI
from crewai import Agent, Process, Task, Crew
from crewai_tools import tool
from langchain_community.llms.ollama import Ollama

# Configurações do modelo
gemini = VertexAI(model_name="gemini-1.0-pro-002", temperature=0.2)



# Ferramentas
@tool("millennium_falcon")
def millennium_falcon():
    """
    Simulação das funcionalidades de uma Millennium Falcon para proteger o Luke.
    Retorna um texto que indica que a Millennium Falcon está atacando o inimigo e protegendo a rota de Luke.
    """
    return "Millennium Falcon atacando o inimigo, protegendo a rota de Luke na X-Wing"

@tool("x_wing")
def x_wing():
    """
    Simulação das funcionalidades de uma X-Wing para a missão de destruir a estrela da morte.
    Retorna um texto que indica que a X-Wing está pronta para o ataque final com sistemas de mira ativados.
    """
    return "X-Wing pronta para o ataque final, sistemas de mira ativados. Atacando!!!"

# Agentes
luke = Agent(
    role='Piloto Heroico',
    goal='Destruir a Estrela da Morte',
    backstory='O jovem piloto destinado a ser um Jedi, convocado para destruir a estrela da morte',
    tools=[x_wing],
    llm=gemini,
    verbose=True,
    
)

han = Agent(
    role='Protetor Audaz',
    goal='Protetor do Luke durante a missão',
    backstory='O contrabandista ousado que se torna um heroi, protegendo seu amigo',
    tools=[millennium_falcon],
    llm=gemini,
    verbose=True,
    
)

leia = Agent(
    role='Estrategista',
    goal='Coordenar o ataque a estrela da morte',
    backstory='A princesa líder da rebelião, essencial para estratégia e comunicação',
    llm=gemini,
    verbose=True,
)

# Tarefas
coordenar_ataque = Task(
    description="""Leia deve coordenar a missão,
    mantendo comunicação e fornecendo suporte estratégico.
    Leia deve ordenar primeiro que Han defenda o Luke, possibilitando um caminho seguro para ele.""",
    expected_output="""Ataque coordenado com sucesso,
    estrela da morte destruída. Todas as unidades informadas e alinhadas""",
    agent=leia,
    allow_delegation=True
)

proteger_luke = Task(
    description="Han deve atacar naves inimigas e proteger Luke de ser atacado durante a missão.",
    expected_output="Luke protegido com sucesso, caminho livre para estrela da morte.",
    agent=han
)

destruir_estrela = Task(
    description="Luke deve pilotar a sua X-Wing e atirar no ponto fraco da estrela da morte para destruí-la.",
    expected_output="Estrela da Morte destruída com sucesso, missão bem-sucedida.",
    agent=luke
)

# Crew
alianca_rebelde = Crew(
    agents=[leia, luke, han],
    tasks=[coordenar_ataque, proteger_luke, destruir_estrela],
    process=Process.hierarchical,
    manager_llm=gemini,
    max_rpm=30,
    language='pt-br'
    
)

# Função kickoff revisada para prevenção de loops infinitos
def kickoff_with_timeout(max_attempts=1, task_max_iterations=3):
    for attempt in range(1, max_attempts + 1):
        print(f"Tentativa {attempt}: Iniciando o processo de kickoff")
        for iteration in range(1, task_max_iterations + 1):
            try:
                result = alianca_rebelde.kickoff()
                print(f"Iteração {iteration}: Resultado do kickoff: {result}")
                if "Estrela da Morte destruída com sucesso" in result and "missão bem-sucedida" in result:
                    print("Missão concluída com sucesso")
                    print("VENCEMOS")
                    return result
            except TypeError as e:
                print(f"Erro encontrado: {e}")
                if "is_blocked" in str(e):
                    # Se o erro for relacionado à chave is_blocked, tente resolver de forma específica
                    continue
                else:
                    raise e

            if iteration == task_max_iterations:
                print("Atingido o número máximo de iterações para a tarefa do Luke.")
                break

        print(f"Falha na missão. Tentando novamente ({attempt}/{max_attempts})")

    print("Falha na missão após várias tentativas.")
    return "Falha na missão"

# Chama a função kickoff com prevenção de loops infinitos
resultado = kickoff_with_timeout()
print(resultado)
