import 'package:flutter/material.dart';

class TaxpayerDetailPage extends StatelessWidget {
  final Map<String, dynamic> taxpayer;

  const TaxpayerDetailPage({super.key, required this.taxpayer});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Detalhes: ${taxpayer['name']}')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text("Nome: ${taxpayer['name']}"),
            Text("CPF: ${taxpayer['cpf'] ?? '-'}"),
            Text("Nascimento: ${taxpayer['birth_date'] ?? '-'}"),
            Text("Renda: R\$ ${taxpayer['income'] ?? '0'}"),
            Text("Status: ${taxpayer['status'] ?? 'N/D'}"),
          ],
        ),
      ),
    );
  }
}
