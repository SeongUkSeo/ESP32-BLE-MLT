import 'package:flip_card/flip_card.dart';
import 'package:flutter/material.dart';
import 'package:web_socket_channel/io.dart';

final channel = IOWebSocketChannel.connect('ws://10.0.2.2:5000');

// main function calling
// to the MyFlipCard class.
void main() {
  runApp(MyFlipCard());
}

final bearItem = [
  {"image": "assets/images/img_blue.png", "name": "파랑이"},
  {"image": "assets/images/img_mint.png", "name": "민트트"},
  {"image": "assets/images/img_skyblue.png", "name": "하늘이"},
  {"image": "assets/images/img_white.png", "name": "하양이"},
  {"image": "assets/images/img_pink.png", "name": "분홍이"},
  {"image": "assets/images/img_yellow.png", "name": "노랑이"},
  {"image": "assets/images/img_purple.png", "name": "보라라"},
  {"image": "assets/images/img_mix.png", "name": "믹스스"}
];

// Class MyFlipCard is stateful class.
class MyFlipCard extends StatefulWidget {
  const MyFlipCard({Key? key}) : super(key: key);

  @override
  State<MyFlipCard> createState() => _MyFlipCardState();
}

class _MyFlipCardState extends State<MyFlipCard> {
  @override
  Widget build(BuildContext context) {
    // returning MaterialApp
    channel.stream.listen(
      (message) {
        debugPrint('Received: $message');
      },
      onError: (error) {
        debugPrint('Error: $error');
      },
      onDone: () {
        debugPrint('WebSocket disconnected');
      },
    );
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: Scaffold(
        appBar: AppBar(
          title: Text("Flip Card"),
        ),
        // body has a center with row child.
        body: Center(
          child: Container(
            padding: EdgeInsets.all(30),
            alignment: Alignment.center,
            width: MediaQuery.of(context).size.width,
            height: MediaQuery.of(context).size.height,
            child: GridView.builder(
              itemCount: bearItem.length, //item 개수
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
                        bearItem[index]['name'].toString(),
                        style: TextStyle(fontSize: 30),
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
                        bearItem[index]['name'].toString(),
                        style: TextStyle(fontSize: 30),
                      ),
                    ),
                  ),
                );
              },
            ),
          ),
        ),
      ),
    );
  }
}
