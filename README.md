## **Contexto:**

Na era da transformação digital, dados precisos são essenciais para empresas como a "DncInsight Solutions", especializada em análise e processamento de dados. A empresa enfrenta desafios com a qualidade e organização dos dados recebidos, muitas vezes inconsistentes e incompletos. Para resolver isso, "DncInsight Solutions" iniciou um desafio interno para desenvolver um sistema robusto e automatizado para o processamento de dados.

Como engenheiro de dados na "DncInsight Solutions", você é responsável por desenvolver um pipeline de dados usando Apache Airflow. Este pipeline transformará dados brutos em insights valiosos através de um processo que inclui a limpeza e agregação de dados. Diferentemente da abordagem tradicional com AWS S3, você simulará um ambiente de produção usando pastas locais para armazenamento de dados.

## Como começar?

Sua tarefa é projetar e implementar um pipeline de dados que ingere dados brutos, os processa e os armazena em três camadas distintas (bronze, prata e ouro) . O pipeline deve ser orquestrado usando o Apache Airflow. Lembre-se, o Windows não suporta o Airflow, sugerimos a utilização de Docker para executar o Airflow.

## **Etapa 01) Configuração Inicial**

Configure o Apache Airflow usando Docker para criar um ambiente uniforme e controlado. Esta configuração inicial garante consistência nas dependências e facilita o gerenciamento de seu pipeline de dados.

### **Passos Rápidos para Configuração:**

- **Instale o Docker Desktop**: Disponível para [download](https://www.docker.com/products/docker-desktop/) no site oficial do Docker.
- **Organize as Pastas de Dados**: Estruture pastas locais para Bronze, Prata e Ouro para simular as camadas de armazenamento de dados.
- **Configure e Inicie o Airflow com Docker Compose**: Defina o serviço do Airflow no Docker Compose e inicie-o para acessar a interface web em `http://localhost:8080`.


💡 **Dica**: Instale bibliotecas essenciais como **`pandas`** dentro do contêiner do Airflow para a manipulação de dados.



## **Etapa 02) Criando o DAG no Airflow**

**Desenvolvimento do DAG:**

- Criar um DAG no Airflow que irá orquestrar todas as operações do pipeline de dados desde o carregamento até a transformação final.
- Definir tarefas sequenciais dentro do DAG para manipulação dos dados em cada camada.

<aside>
💡 **Dica:** Ao configurar o DAG, mantenha a legibilidade e a manutenibilidade em mente. Nomeie claramente cada tarefa e certifique-se de que as dependências entre as tarefas estão bem definidas para evitar ciclos e erros de execução.

</aside>

## Etapa 03) Processamento e Limpeza de dados

- **Carregar Dados Brutos na Camada Bronze:**
    - Implementar a função `upload_raw_data_to_bronze` para carregar dados brutos nos formatos CSV para a camada Bronze.
- **Limpeza de Dados para a Camada Prata:**
    - Utilizar a função `process_bronze_to_silver` para ler e limpar os dados da camada Bronze:
        - Remover registros com campos nulos (nome, email, data de nascimento).
        - Corrigir formatos de email inválidos. (para ser um email valido é necessário ter o caracter “@”)
        - Calcular a idade dos usuários com base na data de nascimento.
     
## **Etapa 04) Transformação e Armazenamento de Dados**

1. **Transformações para a Camada Ouro:**
    - Com a função `process_silver_to_gold`, ler os dados da camada Prata.
    - Executar transformações adicionais:
        - Agregar os dados por faixa etária e status (ativo ou inativo), facilitando análises demográficas e comportamentais.
        - Crie um dataset que mostre o número de usuários por faixa etária (0 a 10, 11 a 20, 21 a 30 anos…) e por status (“active” ou “inactive”)
    - Salvar os dados transformados na camada Ouro, prontos para análise e uso em decisões estratégicas.
