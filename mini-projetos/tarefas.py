import json
import os

class GerenciadorDeTarefas:
    def __init__(self, arquivo="tarefas.json"):
        self.arquivo = arquivo
        self.tarefas = []
        self._carregar_do_disco()

    def _carregar_do_disco(self):
        if not os.path.exists(self.arquivo):
            return
        try:
            with open(self.arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)
                self.tarefas = dados if isinstance(dados, list) else []
        except (json.JSONDecodeError, IOError):
            self.tarefas = []

    def _salvar_no_disco(self):
        temp_file = f"{self.arquivo}.tmp"
        try:
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(self.tarefas, f, indent=4, ensure_ascii=False)
            os.replace(temp_file, self.arquivo)
        except IOError as e:
            # Erro crítico de permissão ou disco cheio
            raise IOError(f"Falha ao salvar no disco: {e}")

    def adicionar(self, titulo, legenda=""):
        titulo = titulo.strip()
        if not titulo:
            raise ValueError("O título da tarefa não pode ser vazio.")
        
        # Uso de gerador para performance
        novo_id = max((t["id"] for t in self.tarefas), default=0) + 1
        
        nova_tarefa = {
            "id": novo_id,
            "titulo": titulo,
            "legenda": legenda.strip()
        }
        self.tarefas.append(nova_tarefa)
        self._salvar_no_disco()
        return novo_id

    def concluir(self, id_tarefa):
        for i, tarefa in enumerate(self.tarefas):
            if tarefa["id"] == id_tarefa:
                del self.tarefas[i]
                self._salvar_no_disco()
                return True
        raise KeyError(f"ID {id_tarefa} não encontrado.")

def exibir_interface():
    gerenciador = GerenciadorDeTarefas()
    
    while True:
        print("\n--- GERENCIADOR PROFISSIONAL ---")
        if not gerenciador.tarefas:
            print("Lista vazia.")
        else:
            for t in gerenciador.tarefas:
                legenda = f" | {t['legenda']}" if t['legenda'] else ""
                print(f"{t['id']}. {t['titulo']}{legenda}")
            
        print("\n1. Adicionar | 2. Concluir/Remover | 3. Sair")
        opcao = input("Opção: ")
        
        try:
            if opcao == "1":
                titulo = input("Título: ")
                legenda = input("Legenda (opcional): ")
                gerenciador.adicionar(titulo, legenda)
                print("Tarefa adicionada com sucesso.")
            elif opcao == "2":
                id_input = input("ID da tarefa: ")
                if not id_input.isdigit():
                    raise ValueError("O ID deve ser um número inteiro.")
                gerenciador.concluir(int(id_input))
                print("Tarefa removida com sucesso.")
            elif opcao == "3":
                break
            else:
                print("Opção inválida.")
        except (ValueError, KeyError, IOError) as e:
            print(f"Erro: {e}")

if __name__ == "__main__":
    exibir_interface()