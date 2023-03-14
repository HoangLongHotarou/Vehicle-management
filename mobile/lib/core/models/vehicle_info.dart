class VehicleInfo {
  String? sId;
  String? plate;
  String? userId;
  String? type;

  VehicleInfo({this.sId, this.plate, this.userId, this.type});

  VehicleInfo.fromJson(Map<String, dynamic> json) {
    sId = json['_id'];
    plate = json['plate'];
    userId = json['user_id'];
    type = json['type'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['_id'] = this.sId;
    data['plate'] = this.plate;
    data['user_id'] = this.userId;
    data['type'] = this.type;
    return data;
  }
}
