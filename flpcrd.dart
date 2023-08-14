import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flip_card/flip_card.dart';
import 'package:http/http.dart' as http;
String ipandport = 000.000.000.000:0000;
void main() {
  runApp(MyApp());
}

class DeviceInfo {
  final String sensorid;
  final int expid;
  final String timestamp;
  final double sapflow;
  final double soilmoisture;
  final int sunlight;
  final double temperature;
  final double humidity;
  final int errorcode;
  DeviceInfo({
    required this.sensorid,
    required this.expid,
    required this.timestamp,
    required this.sapflow,
    required this.soilmoisture,
    required this.sunlight,
    required this.temperature,
    required this.humidity,
    required this.errorcode,
  });
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: HomeScreen(),
    );
  }
}

class HomeScreen extends StatefulWidget {
  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  late List<GlobalKey<FlipCardState>> cardKeys;
  late Timer updateTimer;
  List<DeviceInfo> deviceData = [];

  @override
  void initState() {
    super.initState();
    cardKeys = List.generate(8, (index) => GlobalKey<FlipCardState>());
    for (int i = 0; i < 8; i++) {
      cardKeys[i].currentState?.toggleCard(); // 첫 번째 뒤집기
      cardKeys[i].currentState?.toggleCard(); // 두 번째 뒤집기
    }
    fetchInitialDeviceData(); // 초기 기기 정보 가져오기
    startUpdateTimer();
  }

  @override
  void dispose() {
    updateTimer.cancel();
    super.dispose();
  }

  void fetchInitialDeviceData() async {
    final response = await http
        .get(Uri.parse('http://$ipandport/get_initial_devices'));
    if (response.statusCode == 200) {
      final List<dynamic> data = json.decode(response.body);
      setState(() {
        deviceData = data
            .map((device) => DeviceInfo(
                sensorid: device['sensorid'],
                expid: device['expid'],
                timestamp: device['timestamp'],
                sapflow: device['sapflow'],
                soilmoisture: device['soilmoisture'],
                sunlight: device['sunlight'],
                temperature: device['temperature'],
                humidity: device['humidity'],
                errorcode: device['errorcode']))
            .toList();
      });
    }
  }

  void startUpdateTimer() {
    updateTimer = Timer.periodic(Duration(seconds: 5), (timer) {
      updateFlipCards();
    });
  }

  void updateFlipCards() async {
    final updatedDevicesResponse = await http
        .get(Uri.parse('http://$ipandport/get_updated_devices'));
    if (updatedDevicesResponse.statusCode == 200) {
      List<dynamic> updatedData = json.decode(updatedDevicesResponse.body);
      List<DeviceInfo> updatedDevices = updatedData
          .map((device) => DeviceInfo(
              sensorid: device['sensorid'],
              expid: device['expid'],
              timestamp: device['timestamp'],
              sapflow: device['sapflow'],
              soilmoisture: device['soilmoisture'],
              sunlight: device['sunlight'],
              temperature: device['temperature'],
              humidity: device['humidity'],
              errorcode: device['errorcode']))
          .toList();

      setState(() {
        for (DeviceInfo updatedDevice in updatedDevices) {
          deviceData[updatedDevice.expid - 1] =
              updatedDevice; // 기기 데이터를 업데이트된 데이터로 갱신
        }
      });

      for (DeviceInfo updatedDevice in updatedDevices) {
        int card_index = updatedDevice.expid - 1;
        cardKeys[card_index].currentState?.toggleCard(); // 앞면인 경우에만 뒤집기
        await Future.delayed(Duration(milliseconds: 500)); // 0.5초 대기
        cardKeys[card_index].currentState?.toggleCard(); // 뒷면으로 다시 뒤집기
        await Future.delayed(Duration(milliseconds: 500)); // 0.5초 대기
        cardKeys[card_index].currentState?.toggleCard(); // 앞면으로 다시 뒤집기
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Flip Card Example')),
      body: Center(
        child: Container(
          padding: EdgeInsets.all(30),
          alignment: Alignment.center,
          width: MediaQuery.of(context).size.width,
          height: MediaQuery.of(context).size.height,
          child: GridView.builder(
            itemCount: deviceData.length, //item 개수
            gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
              crossAxisCount: 8, //1 개의 행에 보여줄 item 개수
              childAspectRatio: 1 / 4.3, //item 의 가로 1, 세로 2 의 비율
              // mainAxisSpacing: 5, //수평 Padding
              // crossAxisSpacing: 5, //수직 Padding
            ),
            itemBuilder: (BuildContext context, int index) {
              //item 의 반목문 항목 형성
              return Container(
                padding: EdgeInsets.fromLTRB(10, 0, 10, 0),
                child: FlipCard(
                  key: cardKeys[index],
                  direction: FlipDirection.VERTICAL,
                  // front of the card
                  front: Container(
                    decoration: BoxDecoration(
                      color: Color(0xFF006666),
                      borderRadius: BorderRadius.all(Radius.circular(20)),
                    ),
                    alignment: Alignment.center,
                    // color: Colors.red,
                    child: Text(
                      '$index',
                      style: TextStyle(
                          fontSize: 50,
                          color: Color.fromARGB(255, 216, 241, 241)),
                    ),
                  ),
                  // back of the card
                  back: Container(
                    decoration: BoxDecoration(
                      color: Color.fromARGB(255, 216, 241, 241),
                      borderRadius: BorderRadius.all(Radius.circular(20)),
                    ),
                    alignment: Alignment.center,
                    // color: Colors.red,
                    child: Text(
                      '${deviceData.isNotEmpty ? deviceData[index].sapflow : ''}',
                      style: TextStyle(fontSize: 50),
                    ),
                  ),
                ),
              );
            },
          ),
        ),
      ),
    );
  }
}
