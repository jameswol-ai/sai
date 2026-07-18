import 'package:flutter/material.dart';
import '../services/supabase_service.dart';
import '../services/market_service.dart';
import 'trading_screen.dart';
import 'history_screen.dart';

class DashboardScreen extends StatefulWidget {
  final String username;
  final String role;

  DashboardScreen({required this.username, required this.role});

  @override
  _DashboardScreenState createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  double _balance = 0;
  double _risk = 2;
  bool _botRunning = false;

  @override
  void initState() {
    super.initState();
    _loadBalance();
  }

  void _loadBalance() async {
    double bal = await SupabaseService.getBalance(widget.username);
    setState(() { _balance = bal; });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(title: Text('SAI Dashboard'), backgroundColor: Colors.green[800]),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Welcome, ${widget.username}', style: TextStyle(fontSize: 18, color: Colors.greenAccent)),
            SizedBox(height: 20),
            _balanceCard(),
            SizedBox(height: 20),
            Text('Risk Level: ${_risk.toInt()}%', style: TextStyle(color: Colors.white)),
            Slider(
              value: _risk,
              min: 1, max: 20, divisions: 19,
              onChanged: (val) => setState(() { _risk = val; }),
            ),
            SwitchListTile(
              title: Text('Auto Trading Bot', style: TextStyle(color: Colors.white)),
              value: _botRunning,
              onChanged: (val) => setState(() { _botRunning = val; }),
              activeColor: Colors.green,
            ),
            SizedBox(height: 30),
            Text('Live Market', style: TextStyle(fontSize: 18, color: Colors.white)),
            SizedBox(height: 10),
            _marketGrid(),
          ],
        ),
      ),
      bottomNavigationBar: BottomAppBar(
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: [
            IconButton(
              icon: Icon(Icons.trending_up), color: Colors.green,
              onPressed: () {
                Navigator.push(context, MaterialPageRoute(builder: (_) => TradingScreen(username: widget.username, risk: _risk)));
              },
            ),
            IconButton(
              icon: Icon(Icons.history), color: Colors.green,
              onPressed: () {
                Navigator.push(context, MaterialPageRoute(builder: (_) => HistoryScreen(username: widget.username)));
              },
            ),
          ],
        ),
      ),
    );
  }

  Widget _balanceCard() {
    return Container(
      padding: EdgeInsets.all(20),
      decoration: BoxDecoration(color: Colors.grey[900], borderRadius: BorderRadius.circular(10)),
      child: Column(
        children: [
          Text('Balance', style: TextStyle(color: Colors.grey)),
          SizedBox(height: 8),
          Text('\$ ${_balance.toStringAsFixed(2)}', style: TextStyle(fontSize: 32, fontWeight: FontWeight.bold, color: Colors.greenAccent)),
          SizedBox(height: 8),
          Text('Bot: ${_botRunning ? "RUNNING" : "STOPPED"}', style: TextStyle(color: _botRunning ? Colors.green : Colors.red)),
        ],
      ),
    );
  }

  Widget _marketGrid() {
    final rates = MarketService.getMarket();
    return GridView.builder(
      shrinkWrap: true,
      physics: NeverScrollableScrollPhysics(),
      itemCount: rates.length,
      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount: 3, childAspectRatio: 2.5),
      itemBuilder: (ctx, index) {
        String key = rates.keys.elementAt(index);
        return Card(
          color: Colors.grey[800],
          child: Center(child: Text('$key\n${rates[key]}', textAlign: TextAlign.center, style: TextStyle(color: Colors.white))),
        );
      },
    );
  }
}