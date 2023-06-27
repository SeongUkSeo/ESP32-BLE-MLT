import 'dart:async';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Sensor Dashboard',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: SensorDashboard(),
    );
  }
}

class SensorDashboard extends StatefulWidget {
  @override
  _SensorDashboardState createState() => _SensorDashboardState();
}

class _SensorDashboardState extends State<SensorDashboard> {
  List<dynamic> sensorData = [];

  @override
  void initState() {
    super.initState();
    fetchSensorData();
  }

  Future<void> fetchSensorData() async {
    final response = await http.get(Uri.parse('API_URL'));
    if (response.statusCode == 200) {
      setState(() {
        sensorData = json.decode(response.body);
      });
    } else {
      throw Exception('Failed to fetch sensor data');
    }
  }

  Future<void> refreshSensorData() async {
    await fetchSensorData();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Sensor Dashboard'),
      ),
      body: ListView.builder(
        itemCount: sensorData.length,
        itemBuilder: (BuildContext context, int index) {
          return Card(
            child: ListTile(
              title: Text('Sensor ${index + 1}'),
              subtitle: Text('Value: ${sensorData[index]['value']}'),
            ),
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: refreshSensorData,
        child: Icon(Icons.refresh),
      ),
    );
  }
}
