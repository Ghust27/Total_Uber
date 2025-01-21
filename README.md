# API Total Gasto Uber

## Descrição
Esta API permite obter um resumo dos gastos no Uber, incluindo o total gasto e o período das viagens. O projeto é baseado no Flask e interage com a API do Uber para coletar as informações.

## Funcionalidades
- **Obter Total Gasto no Uber**: Recebe cookies como entrada e retorna o total gasto, moeda utilizada e o período (primeira e última viagem).

## Tecnologias Utilizadas
- Python
- Flask
- Requests
- Datetime
- Urllib3

## Uso

1. **Execute a aplicação:**
  ```sh
    python main.py
  ```
2. **Faça uma requisição POST para o endpoint:**
  ```sh
    http://127.0.0.1:5000/get_total_uber
  ```
  Com o seguinte payload JSON:
  ``` sh
    {
      "cookies": "SEUS_COOKIES_ENCODED"
    }
  ```
##Exemplo de Resposta:
```sh
{
  "coin": "BRL",
  "total_spent": 1234.56,
  "first_date": "Jan 2023",
  "final_date": "Dec 2023"
}

