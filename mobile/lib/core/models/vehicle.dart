class Vehicle {
  String? username;
  String? plate;
  Information? information;
  String? turn;

  Vehicle({this.username, this.plate, this.information, this.turn});

  Vehicle.fromJson(Map<String, dynamic> json) {
    username = json['username'];
    plate = json['plate'];
    information = json['information'] != null
        ? new Information.fromJson(json['information'])
        : null;
    turn = json['turn'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['username'] = this.username;
    data['plate'] = this.plate;
    if (this.information != null) {
      data['information'] = this.information!.toJson();
    }
    data['turn'] = this.turn;
    return data;
  }
}

class Information {
  String? date;
  String? time;

  Information({this.date, this.time});

  Information.fromJson(Map<String, dynamic> json) {
    date = json['date'];
    time = json['time'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['date'] = this.date;
    data['time'] = this.time;
    return data;
  }
}

