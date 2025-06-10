import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

import 'pages/dashboard_page.dart';
import 'pages/login_page.dart';
import 'pages/taxpayer_form_page.dart';
import 'pages/taxpayer_detail_page.dart';

Future<void> main() async {
  // Necessário para inicialização de plugins e async em Flutter Web/Desktop
  WidgetsFlutterBinding.ensureInitialized();

  // Carrega as variáveis do arquivo .env
  await dotenv.load(fileName: ".env");

  runApp(const OneApiIRSApp());
}

// Funções utilitárias para acessar usuário e senha do .env
String get defaultUser => dotenv.env['FLUTTER_DEFAULT_USER'] ?? 'admin';
String get defaultPassword => dotenv.env['FLUTTER_DEFAULT_PASSWORD'] ?? 'supersecreta123';

class OneApiIRSApp extends StatelessWidget {
  const OneApiIRSApp({super.key});

  Future<Widget> _getInitialScreen() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('access_token');
    return token != null ? const DashboardPage() : const LoginPage();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'OneAPIIRS',
      theme: ThemeData(primarySwatch: Colors.indigo),
      debugShowCheckedModeBanner: false,
      routes: {
        '/new-taxpayer': (_) => const TaxpayerFormPage(),
        '/taxpayer-detail': (context) {
          final taxpayer = ModalRoute.of(context)!.settings.arguments as Map<String, dynamic>;
          return TaxpayerDetailPage(taxpayer: taxpayer);
        },
      },
      home: FutureBuilder<Widget>(
        future: _getInitialScreen(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.done && snapshot.hasData) {
            return snapshot.data!;
          } else {
            return const Scaffold(
              body: Center(child: CircularProgressIndicator()),
            );
          }
        },
      ),
    );
  }
}
