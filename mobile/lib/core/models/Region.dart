class Region {
  String? sId;
  String? region;
  String? type;
  Coordinate? coordinate;
  List<Cameras>? cameras;

  Region({this.sId, this.region, this.type, this.coordinate, this.cameras});

  Region.fromJson(Map<String, dynamic> json) {
    sId = json['_id'];
    region = json['region'];
    type = json['type'];
    coordinate = json['coordinate'] != null
        ? new Coordinate.fromJson(json['coordinate'])
        : null;
    if (json['cameras'] != null) {
      cameras = <Cameras>[];
      json['cameras'].forEach((v) {
        cameras!.add(new Cameras.fromJson(v));
      });
    }
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['_id'] = this.sId;
    data['region'] = this.region;
    data['type'] = this.type;
    if (this.coordinate != null) {
      data['coordinate'] = this.coordinate!.toJson();
    }
    if (this.cameras != null) {
      data['cameras'] = this.cameras!.map((v) => v.toJson()).toList();
    }
    return data;
  }
}

class Coordinate {
  String? longitude;
  String? latitude;

  Coordinate({this.longitude, this.latitude});

  Coordinate.fromJson(Map<String, dynamic> json) {
    longitude = json['longitude'];
    latitude = json['latitude'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['longitude'] = this.longitude;
    data['latitude'] = this.latitude;
    return data;
  }
}

class Cameras {
  String? name;
  String? rtspUrl;
  String? type;

  Cameras({this.name, this.rtspUrl, this.type});

  Cameras.fromJson(Map<String, dynamic> json) {
    name = json['name'];
    rtspUrl = json['rtsp_url'];
    type = json['type'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['name'] = this.name;
    data['rtsp_url'] = this.rtspUrl;
    data['type'] = this.type;
    return data;
  }
}
