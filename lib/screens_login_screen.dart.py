import 'package:flutter/material.dart';
import '../services/supabase_service.dart';
import 'dashboard_screen.dart';

class LoginScreen extends StatefulWidget {
  @override
  _LoginScreenState createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final TextEditingController _userCtrl = TextEditingController();
  final TextEditingController _passCtrl = TextEditingController();
  bool _isRegister = false;

  void _submit() async {
    String username = _userCtrl.text.trim();
    String password = _passCtrl.text.trim();
    if (username.isEmpty || password.isEmpty) return;

    if (_isRegister) {
      bool ok = await SupabaseService.register(username, password);
      if (ok) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Account created. Please login.')));
        setState(() { _isRegister = false; });
      } else {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Username taken')));
      }
    } else {
      String? role = await SupabaseService.login(username, password);
      if (role != null) {
        Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => DashboardScreen(username: username, role: role)));
      } else {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Invalid credentials')));
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: Center(
        child: SingleChildScrollView(
          padding: EdgeInsets.all(24),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(Icons.show_chart, size: 80, color: Colors.green),
              SizedBox(height: 20),
              Text('SAI Forex Intelligence', style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: Colors.white)),
              SizedBox(height: 40),
              TextField(controller: _userCtrl, decoration: InputDecoration(labelText: 'Username', filled: true, fillColor: Colors.grey[900])),
              SizedBox(height: 12),
              TextField(controller: _passCtrl, obscureText: true, decoration: InputDecoration(labelText: 'Password', filled: true, fillColor: Colors.grey[900])),
              SizedBox(height: 24),
              ElevatedButton(
                onPressed: _submit,
                child: Text(_isRegister ? 'Register' : 'Login'),
                style: ElevatedButton.styleFrom(minimumSize: Size(double.infinity, 50), backgroundColor: Colors.green),
              ),
              TextButton(
                onPressed: () => setState(() { _isRegister = !_isRegister; }),
                child: Text(_isRegister ? 'Already have an account? Login' : "Don't have an account? Register"),
              ),
            ],
          ),
        ),
      ),
    );
  }
}