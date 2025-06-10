import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'taxpayer_list_page.dart';
import 'login_page.dart';

class DashboardPage extends StatelessWidget {
  const DashboardPage({super.key});

  Future<void> _logout(BuildContext context) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('access_token');

    if (!context.mounted) return; // ✅ Verifica se o widget ainda está vivo

    Navigator.of(context).pushReplacement(
      MaterialPageRoute(builder: (_) => const LoginPage()),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Painel Principal'),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            tooltip: 'Sair',
            onPressed: () => _logout(context),
          ),
        ],
      ),
      body: Center(
        child: ElevatedButton.icon(
          icon: const Icon(Icons.people),
          label: const Text("Ver Contribuintes"),
          onPressed: () {
            Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => const TaxpayerListPage()),
            );
          },
        ),
      ),
    );
  }
}
