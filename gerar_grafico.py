# Agregar vendas por data
vendas_por_data = df.groupby('data_venda')['valor_venda'].sum().reset_index()

# Criar gráfico
plt.figure(figsize=(12, 6))
plt.plot(vendas_por_data['data_venda'], vendas_por_data['valor_venda'], marker='o')
plt.title('Vendas ao Longo do Tempo')
plt.xlabel('Data')
plt.ylabel('Valor de Vendas (R$)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(True, alpha=0.3)

# Salvar como PNG
plt.savefig('grafico_vendas.png', dpi=300, bbox_inches='tight')
print('Gráfico salvo como grafico_vendas.png')
