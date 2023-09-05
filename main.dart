import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'dart:io';

void main() {
  runApp(MyApp());
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
  File? _backgroundImage;

  _pickImage() async {
    final pickedFile = await ImagePicker().getImage(source: ImageSource.gallery);

    if (pickedFile != null) {
      setState(() {
        _backgroundImage = File(pickedFile.path);
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Room App'),
        leading: IconButton(
          icon: Icon(Icons.menu),
          onPressed: () {
            // Drawer를 여는 코드 추가
          },
        ),
      ),
      drawer: Drawer(
        child: ListView(
          children: [
            ListTile(
              title: Text("Room 1"),
              onTap: () {
                Navigator.pop(context);
                // Room 1 선택 처리
              },
            ),
            // 다른 Room들 추가
            ListTile(
              title: Icon(Icons.add),
              onTap: () {
                Navigator.pop(context);
                // Room 추가 처리
              },
            ),
          ],
        ),
      ),
      body: GestureDetector(
        onTap: _pickImage,
        child: Container(
          decoration: BoxDecoration(
            image: _backgroundImage == null
                ? DecorationImage(
                    image: AssetImage('assets/add_icon.png'),
                    fit: BoxFit.cover,
                  )
                : DecorationImage(
                    image: FileImage(_backgroundImage!),
                    fit: BoxFit.cover,
                  ),
          ),
        ),
      ),
    );
  }
}
