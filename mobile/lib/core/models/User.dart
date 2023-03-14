import 'dart:convert';

class User {
  String? sId;
  String? email;
  String? username;
  String? phoneNumber;
  String? firstName;
  String? lastName;
  String? avatar;

  User(
      {this.sId,
      this.email,
      this.username,
      this.phoneNumber,
      this.firstName,
      this.lastName,
      this.avatar});

  User.fromJson(Map<String, dynamic> json) {
    sId = json['_id'];
    email = json['email'];
    username = json['username'];
    phoneNumber = json['phone_number'];
    firstName = json['first_name'];
    lastName = json['last_name'];
    avatar = json['avatar'];
  }

  Map<String, dynamic> toJson() {
    final Map<String, dynamic> data = new Map<String, dynamic>();
    data['_id'] = this.sId;
    data['email'] = this.email;
    data['username'] = this.username;
    data['phone_number'] = this.phoneNumber;
    data['first_name'] = this.firstName;
    data['last_name'] = this.lastName;
    data['avatar'] = this.avatar;
    return data;
  }

  // Map<String, dynamic> register() {
  //   final Map<String, dynamic> data = new Map<String, dynamic>();
  //   data['email'] = this.email;
  //   data['username'] = this.username;
  //   data['phone_number'] = this.phoneNumber;
  //   return data;
  // }
}
