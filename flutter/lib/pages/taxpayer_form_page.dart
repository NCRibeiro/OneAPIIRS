import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../services/api_service.dart';

class TaxpayerFormPage extends StatefulWidget {
  const TaxpayerFormPage({super.key});

  @override
  State<TaxpayerFormPage> createState() => _TaxpayerFormPageState();
}

class _TaxpayerFormPageState extends State<TaxpayerFormPage> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  final _incomeController = TextEditingController();

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;

    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('access_token') ?? '';

    final payload = {
      'name': _nameController.text,
      'status': 'ativo',
      'income': double.tryParse(_incomeController.text) ?? 0.0,
    };

    await ApiService().createTaxpayer(payload, token);
    if (!mounted) return;
    Navigator.pop(context, true); // retorna true se bem-sucedido
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Novo Contribuinte')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: Column(
            children: [
              TextFormField(
                controller: _nameController,
                decoration: const InputDecoration(labelText: 'Nome'),
                validator: (v) => v == null || v.isEmpty ? 'Obrigatório' : null,
              ),
              TextFormField(
                controller: _incomeController,
                decoration: const InputDecoration(labelText: 'Renda'),
                keyboardType: TextInputType.number,
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: _submit,
                child: const Text("Salvar"),
              )
            ],
          ),
        ),
      ),
    );
  }
}
