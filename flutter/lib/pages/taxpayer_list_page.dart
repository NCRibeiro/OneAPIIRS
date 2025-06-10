import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../services/api_service.dart';

class TaxpayerListPage extends StatefulWidget {
  const TaxpayerListPage({super.key});

  @override
  State<TaxpayerListPage> createState() => _TaxpayerListPageState();
}

class _TaxpayerListPageState extends State<TaxpayerListPage> {
  final ApiService _apiService = ApiService();
  List<dynamic> _taxpayers = [];
  bool _isLoading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _loadTaxpayers();
  }

  Future<void> _loadTaxpayers() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('access_token') ?? '';
      final data = await _apiService.getTaxpayers(token);
      setState(() {
        _taxpayers = data;
      });
    } catch (e) {
      setState(() {
        _error = e.toString();
      });
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Contribuintes")),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _error != null
              ? Center(
                  child:
                      Text(_error!, style: const TextStyle(color: Colors.red)))
              : ListView.builder(
                  itemCount: _taxpayers.length,
                  itemBuilder: (context, index) {
                    final tp = _taxpayers[index];
                    return ListTile(
                      leading: const Icon(Icons.person),
                      title: Text(tp['name']),
                      subtitle: Text('Renda: R\$ ${tp['income'] ?? '-'}'),
                      onTap: () {
                        Navigator.pushNamed(
                          context,
                          '/taxpayer-detail',
                          arguments: tp,
                        );
                      },
                    );
                  },
                ),
      floatingActionButton: FloatingActionButton(
        onPressed: () async {
          final result = await Navigator.pushNamed(context, '/new-taxpayer');
          if (result == true) {
            _loadTaxpayers(); // atualiza após novo cadastro
          }
        },
        tooltip: "Adicionar contribuinte",
        child: const Icon(Icons.add),
      ),
    );
  }
}
