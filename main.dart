import 'dart:io';
import 'package:image_picker/image_picker.dart';

// 기존의 _HomeScreenState 클래스 내에 추가
File? pickedImage;

void showAddRoomDialog() {
  showDialog(
    context: context,
    builder: (context) {
      return AlertDialog(
        title: Text('Room 추가'),
        content: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              TextField(
                controller: roomNameController,
                decoration: InputDecoration(labelText: '방 이름'),
              ),
              ElevatedButton(
                onPressed: () async {
                  final ImagePicker _picker = ImagePicker();
                  final XFile? image = await _picker.pickImage(source: ImageSource.gallery);

                  if (image != null) {
                    setState(() {
                      pickedImage = File(image.path);
                    });
                  }
                },
                child: Text("사진 선택"),
              ),
              pickedImage != null ? Image.file(pickedImage!) : Container(),
            ],
          ),
        ),
        actions: [
          ElevatedButton(
            onPressed: () async {
              await addRoom(roomNameController.text, pickedImage);
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
