import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/get_chart')
def get_chart():
    # 예시 데이터
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    temps_seoul = [22, 24, 25, 23, 22, 21, 22]
    temps_busan = [24, 25, 26, 24, 25, 24, 25]

    # Seaborn 스타일로 차트 생성
    sns.set_style("whitegrid")
    plt.figure(figsize=(10, 5))
    sns.lineplot(x=days, y=temps_seoul, label='Seoul', marker='o')
    sns.lineplot(x=days, y=temps_busan, label='Busan', marker='o')
    plt.title("Weekly Temperatures")
    plt.xlabel("Day")
    plt.ylabel("Temperature (°C)")
    plt.legend()

    # 이미지로 저장
    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)

    # 이미지를 Base64로 인코딩
    encoded_img = base64.b64encode(img.getvalue()).decode('utf-8')

    return jsonify({'image': encoded_img})

if __name__ == "__main__":
    app.run(debug=True)


import 'package:flutter/material.dart';
import 'dart:convert';

void main() => runApp(MaterialApp(home: MyChartApp()));

class MyChartApp extends StatefulWidget {
  @override
  _MyChartAppState createState() => _MyChartAppState();
}

"""
class _MyChartAppState extends State<MyChartApp> {
  // 예시 데이터 (실제로는 API에서 가져와야 함)
  String base64Image = "BASE64_ENCODED_IMAGE_DATA_HERE";

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("기온 차트 이미지")),
      body: Center(
        child: Image.memory(base64Decode(base64Image)),
      ),
    );
  }
}
"""
