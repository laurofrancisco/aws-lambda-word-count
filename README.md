# Desafio AWS Lambda – Contagem de Palavras

Este projeto foi desenvolvido como parte de um laboratório do **AWS reStart**, com o objetivo de criar uma solução **serverless orientada a eventos** utilizando serviços da AWS.

O desafio consiste em desenvolver uma função no **AWS Lambda** capaz de contar o número de palavras em um arquivo de texto enviado para um bucket do **Amazon S3**. Após o processamento do arquivo, o resultado deve ser enviado por e-mail utilizando um tópico do **Amazon SNS (Simple Notification Service)**.

## Objetivo do Laboratório

O objetivo deste laboratório é praticar a criação e integração de serviços da AWS para construir uma solução automatizada que:

- Conte o número de palavras em um arquivo de texto
- Execute automaticamente quando um arquivo for enviado para um bucket do Amazon S3
- Envie o resultado da contagem por e-mail utilizando o Amazon SNS

## Serviços AWS Utilizados

Os seguintes serviços da AWS foram utilizados para a implementação da solução:

| Serviço | Descrição |
|-------|-----------|
| **AWS Lambda** | Executa a função responsável por processar o arquivo e contar as palavras |
| **Amazon S3** | Armazena os arquivos de texto enviados e dispara o evento que aciona a função Lambda |
| **Amazon SNS** | Envia a notificação por e-mail com o resultado da contagem de palavras |
| **Amazon CloudWatch** | Registra logs e monitora a execução da função Lambda |
| **AWS IAM** | Gerencia as permissões necessárias para que a função Lambda acesse os outros serviços |

---

## Arquitetura da Solução

A solução segue um modelo de **arquitetura serverless orientada a eventos**, onde a execução da função é acionada automaticamente após o upload de um arquivo.

```
Fluxo de funcionamento:

Upload de arquivo (.txt)
↓
Amazon S3 (evento ObjectCreated)
↓
AWS Lambda (função Python)
↓
Processamento do arquivo
↓
Contagem de palavras
↓
Amazon SNS
↓
Envio de e-mail com o resultado
```

## Funcionamento da Função Lambda

A função Lambda desenvolvida em **Python** executa as seguintes etapas:

1. Recebe o evento gerado pelo upload de um arquivo no bucket do Amazon S3
2. Identifica o nome do bucket e o nome do arquivo enviado
3. Recupera o arquivo armazenado no S3
4. Lê o conteúdo do arquivo de texto
5. Realiza a contagem das palavras presentes no arquivo
6. Publica o resultado em um tópico do Amazon SNS
7. O SNS envia uma notificação por e-mail com o resultado da contagem

## Lambda Function Code

```python
import json
import boto3
import urllib.parse

s3 = boto3.client('s3')
sns = boto3.client('sns')

SNS_TOPIC_ARN = "YOUR_SNS_TOPIC_ARN"

def lambda_handler(event, context):

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])

    response = s3.get_object(Bucket=bucket, Key=key)
    content = response['Body'].read().decode('utf-8')

    word_count = len(content.split())

    message = f"The word count in the {key} file is {word_count}."

    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=message,
        Subject="Word Count Result"
    )

    return {
        'statusCode': 200,
        'body': json.dumps(message)
    }
``` 
O formato da mensagem enviada por e-mail segue o padrão solicitado no desafio:
The word count in the "textFileName¨ file is nnn.

O assunto do e-mail enviado é: Word Count Result

## Evento de Teste da Função Lambda

Para testar a função Lambda diretamente pelo console da AWS, foi utilizado um evento de teste simulando o evento gerado pelo **Amazon S3** quando um arquivo é enviado para o bucket.

Exemplo de evento utilizado no teste:

```json
{
  "Records": [
    {
      "s3": {
        "bucket": {
          "name": "bucket-name"
        },
        "object": {
          "key": "file-bucket-name.txt"
        }
      }
    }
  ]
}
``` 

## Configuração do Ambiente

Para a realização do laboratório foram realizadas as seguintes configurações:

### 1. Criação da Função AWS Lambda

Foi criada uma função Lambda utilizando o runtime **Python**, responsável por:

- Processar o evento recebido do Amazon S3
- Ler o conteúdo do arquivo enviado
- Contar o número de palavras
- Publicar o resultado no Amazon SNS

### 2. Configuração do Bucket Amazon S3

Foi criado um bucket no Amazon S3 para armazenar os arquivos de texto.

O bucket foi configurado para gerar um **evento de criação de objeto (ObjectCreated)** sempre que um novo arquivo `.txt` for enviado, acionando automaticamente a função Lambda.

### 3. Criação do Tópico Amazon SNS

Foi criado um tópico no Amazon SNS responsável por enviar notificações por e-mail contendo o resultado da contagem de palavras.

Foi configurada uma **assinatura de e-mail (subscription)** para receber as notificações enviadas pelo SNS.

### 4. Permissões IAM

A função Lambda foi configurada para utilizar o papel (**IAM Role**) `LambdaAccessRole`, que fornece permissões para:

- Acessar o Amazon S3
- Publicar mensagens no Amazon SNS
- Registrar logs no Amazon CloudWatch

---

## Teste da Solução

Para testar o funcionamento da solução, foram realizados os seguintes passos:

1. Criar um arquivo de texto (`.txt`) contendo algumas palavras.
2. Enviar o arquivo para o bucket configurado no Amazon S3.
3. O upload do arquivo gera automaticamente um evento no S3.
4. Esse evento aciona a função AWS Lambda.
5. A função realiza a contagem de palavras no arquivo.
6. O resultado é publicado em um tópico do Amazon SNS.
7. O SNS envia um e-mail com o resultado da contagem.

---

## Exemplo de Resultado

Arquivo enviado: example.txt
```
Conteúdo do arquivo:
AWS Lambda is a serverless compute service
``` 
E-mail recebido:
``` 
Subject: Word Count Result
The word count in the example.txt file is 7.
```
## Aprendizados

Este laboratório permitiu praticar conceitos importantes de computação em nuvem, incluindo:

- Arquitetura **serverless**
- Integração entre serviços AWS
- Processamento de eventos utilizando **AWS Lambda**
- Automação baseada em eventos do **Amazon S3**
- Envio de notificações utilizando **Amazon SNS**
- Monitoramento com **Amazon CloudWatch**
