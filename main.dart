import 'package:flutter/material.dart';
import 'package:path_provider/path_provider.dart';
import 'package:sqflite/sqflite.dart';
import 'dart:io';

void main() => runApp(MyApp());

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
  Database? db;
  List<Map> rooms = [];

  TextEditingController roomNameController = TextEditingController();

  @override
  void initState() {
    super.initState();
    initializeDatabase();
  }

  Future<void> initializeDatabase() async {
    final Directory documentsDirectory = await getApplicationDocumentsDirectory();
    final String path = "${documentsDirectory.path}/rooms.db";
    db = await openDatabase(
      path,
      version: 1,
      onCreate: (Database db, int version) async {
        await db.execute("CREATE TABLE IF NOT EXISTS rooms (id INTEGER PRIMARY KEY, name TEXT)");
      },
    );
    loadData();
  }

  Future<void> loadData() async {
    final List<Map> results = await db!.query("rooms");
    setState(() {
      rooms = results;
    });
  }

  Future<void> addRoom(String name) async {
    await db!.insert("rooms", {"name": name});
    loadData();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Room Manager')),
      body: rooms.isEmpty
          ? Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text("방이 없습니다."),
                  ElevatedButton(
                    onPressed: () {
                      showAddRoomDialog();
                    },
                    child: Text("Room 추가"),
                  ),
                ],
              ),
            )
          : ListView.builder(
              itemCount: rooms.length,
              itemBuilder: (context, index) {
                return ListTile(title: Text(rooms[index]["name"].toString()));
              },
            ),
    );
  }

  void showAddRoomDialog() {
    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: Text('Room 추가'),
          content: TextField(
            controller: roomNameController,
            decoration: InputDecoration(labelText: '방 이름'),
          ),
          actions: [
            ElevatedButton(
              onPressed: () async {
                await addRoom(roomNameController.text);
                roomNameController.clear();
                Navigator.pop(context);
              },
              child: Text('추가'),
            ),
          ],
        );
      },
    );
  }
}
