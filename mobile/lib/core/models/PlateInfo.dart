class PlateInfo {
  String? plate;
  Coordinate? coordinate;

  PlateInfo({this.plate, this.coordinate});

  PlateInfo.fromJson(Map<String, dynamic> json) {
    plate = json['plate'];
    coordinate = json['coordinate'] != null
        ? new Coordinate.fromJson(json['coordinate'])
        : null;
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['plate'] = this.plate;
    if (this.coordinate != null) {
      data['coordinate'] = this.coordinate!.toJson();
    }
    return data;
  }
}

class Coordinate {
  int? x0;
  int? y0;
  int? x1;
  int? y1;

  Coordinate({this.x0, this.y0, this.x1, this.y1});

  Coordinate.fromJson(Map<String, dynamic> json) {
    x0 = json['x0'];
    y0 = json['y0'];
    x1 = json['x1'];
    y1 = json['y1'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['x0'] = this.x0;
    data['y0'] = this.y0;
    data['x1'] = this.x1;
    data['y1'] = this.y1;
    return data;
  }
}
