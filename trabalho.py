import matplotlib.pyplot as plt
import networkx as nx

def desenhar_AFD(Q, delta, q0, F, title):
    G = nx.MultiDiGraph()

    
    for estado in Q:
        if estado in F:
            G.add_node(estado, color='green', style='filled', label=f"{estado} (final)")
        else:
            G.add_node(estado, color='lightblue', style='filled')

   
    for (q_atual, simbolo), q_proximo in delta.items():
        G.add_edge(q_atual, q_proximo, label=simbolo)

    
    pos = nx.spring_layout(G)
    
    
    node_colors = ['green' if node in F else 'lightblue' for node in G.nodes()]
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=2000, font_size=12, font_color='black', font_weight='bold')


    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12)

    # Mostrar o gráfico
    plt.title(title)
    plt.show()

    
#Implementação Automatos Finitos Deterministicos

def AFD(M, cadeia):
    (Q, Sigma, delta, q0, F) = M
    qA = q0
    for x in cadeia:
        if (qA, x) in delta:
            qA = delta[(qA, x)]
        else:
            return False  
    return qA in F


# Definindo o autômato da Figura 1

delta1 = {
    ('q0', 'a'): 'q1', 
    ('q1', 'a'): 'q2', 
    ('q2', 'b'): 'q3', 
    ('q3', 'b'): 'q4', 
    ('q4', 'c'): 'q5', 
    ('q5', 'c'): 'q6'
}

Q1 = ['q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6']
F1 = ['q6']  # Estados finais
Sigma1 = ['a', 'b', 'c']





# Definindo o autômato da Figura 2

delta2 = {
    ('q0', 'a'): 'q1', 
    ('q1', 'a'): 'q2', 
    ('q2', 'a'): 'q3', 
    ('q3', 'c'): 'q4', 
    ('q4', 'd'): 'q5', 
    ('q5', 'c'): 'q3'
}

Q2 = ['q0', 'q1', 'q2', 'q3', 'q4', 'q5']
F2 = ['q5']  # Estado final
Sigma2 = ['a', 'c', 'd']

# Testar o autômato da Figura 1

print("Automato Finito  Deterministico da Figura 1 \n:")
print(AFD((Q1, Sigma1, delta1, 'q0', F1), 'aabbcc'))  # retornar True
print(AFD((Q1, Sigma1, delta1, 'q0', F1), 'aabbbc'))  #  retornar False
print(AFD((Q1, Sigma1, delta1, 'q0', F1), 'aabbcccc'))   #  retornar False

print("\nAutomato Finito  Deterministico da Figura 2 \n:")


# Testar o autômato da Figura 2

print(AFD((Q2, Sigma2, delta2, 'q0', F2), 'aaacd'))  #  retornar True 
print(AFD((Q2, Sigma2, delta2, 'q0', F2), 'aaacdc'))  # retornar False 
print(AFD((Q2, Sigma2, delta2, 'q0', F2), 'aac'))     #  retornar False


#Visualizar figura 1
#desenhar_AFD(Q1, delta1, 'q0', F1, "Figura 1: Autômato com 7 estados")

#Visualizar figura 1
#desenhar_AFD(Q2, delta2, 'q0', F2, "Figura 2: Autômato com 6 estados")



#Implementação Automatos Finitos Não Deterministicos ->  Walbens
def AFN(N, cadeia):
    (Q, Sigma, delta, q0, F) = N
    QA = E({q0}, delta)
    for x in cadeia:
        novos = set()
        for q in QA:
            if (q, x) in delta:
                novos.update(E(delta[(q, x)], delta))
        QA = novos  
    return len(QA.intersection(F)) != 0

def E(estados, delta):
    S = set(estados)
    nao_explorados = list(estados)
    while nao_explorados:
        q = nao_explorados.pop()
        if (q, 'epsilon') in delta:
            novos = delta[(q, 'epsilon')].difference(S)
            S.update(novos)
            nao_explorados.extend(novos)
    return S


Q1 = ['q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6']  
Sigma1 = ['a', 'b', 'c', 'epsilon']  
delta1 = {
    ('q0', 'a'): {'q1'},
    ('q1', 'a'): {'q2'},
    ('q2', 'b'): {'q3'},
    ('q3', 'b'): {'q4'},
    ('q4', 'c'): {'q5'},
    ('q4', 'a'): {'q2'},
    ('q5', 'c'): {'q6'},
    ('q2', 'epsilon'): {'q3'},
}
F1 = ['q6'] 

# Definindo o autômato da Figura 2

delta2 = {
    ('q0', 'a'): {'q1'},
    ('q0', 'epsilon'): {'q0'},
    ('q1', 'a'): {'q2'},
    ('q2', 'a'): {'q3'},
    ('q3', 'c'): {'q4'},
    ('q4', 'd'): {'q5'},
    ('q4', 'a'): {'q1'},
}

Q2 = ['q0', 'q1', 'q2', 'q3', 'q4', 'q5']
F2 = ['q5']  # Estado final
Sigma2 = ['a', 'c', 'd', 'epsilon']



print("Automato Finito Nao Deterministico da Figura 1 :\n")
print(AFN((Q1, Sigma1, delta1, 'q0', F1), 'aabbcc'))  #verdadeiro
print(AFN((Q1, Sigma1, delta1, 'q0', F1),'aabbbc' )) #falso
print(AFN((Q1, Sigma1, delta1, 'q0', F1), 'aabbcccc')) #falso


# Testar o autômato da Figura 2
print("\nAutomato Finito nao Deterministico da Figura 2 :\n")
print(AFN((Q2, Sigma2, delta2, 'q0', F2), 'aaacd'))  #  verdadeiro 
print(AFN((Q2, Sigma2, delta2, 'q0', F2), 'aaacdc'))  # falso 
print(AFN((Q2, Sigma2, delta2, 'q0', F2), 'aac')) #falso
