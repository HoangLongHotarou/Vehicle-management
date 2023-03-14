// ignore_for_file: unrelated_type_equality_checks

import 'dart:ffi';
import 'dart:io';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:license_plate_detect/core/models/Token.dart';
import 'package:license_plate_detect/core/models/checkAndDetail.dart';
import 'package:license_plate_detect/feature/home/presention/HomePage.dart';
import 'package:license_plate_detect/services/api/app_api.dart';
import 'package:license_plate_detect/services/localstorage/localStorage.dart';
import 'package:license_plate_detect/ultis/dialog/alertDialog.dart';

import '../../core/models/User.dart';

class Authenticate {
  Future<bool> checkLogin() async {
    return await LocalStorage.checkToken();
  }

  static Future<bool> login(String username, String password) async {
    bool check = true;
    check = await AppAPI.Login(username, password);
    // bool login = await checkLogin();
    // if (login == false) {
      
    // }
    return check;
  }

  static Future<CheckAndDetail> register(String email, String username,
      String phonenumber, String password) async {
    CheckAndDetail reg =
        await AppAPI.signup(email, username, phonenumber, password);
    return reg;
  }

  static Future<CheckAndDetail> otp(String email, String otp) async {
    CheckAndDetail reg = await AppAPI.otp(email, otp);
    return reg;
  }

  static Future<CheckAndDetail> forgotpassword(String email) async {
    CheckAndDetail reg = await AppAPI.forgotpassword(email);
    return reg;
  }

  static Future<CheckAndDetail> otpResetPassword(
      String email, String otp) async {
    CheckAndDetail reg = await AppAPI.otpResetPassword(email, otp);
    return reg;
  }

  static Future<CheckAndDetail> resetPassword(
      String token, String password) async {
    CheckAndDetail reg = await AppAPI.resetpassword(token, password);
    return reg;
  }

  static Future<CheckAndDetail> updateImage(File imageFile) async {
    CheckAndDetail cks = await AppAPI.UpdateAvatar(imageFile);
    return cks;
  }

  static Future<CheckAndDetail> updateProfile(
      String firstName, String lastName, String phoneNumber) async {
    CheckAndDetail cks =
        await AppAPI.updateProfile(firstName, lastName, phoneNumber);
    return cks;
  }

  static Future<CheckAndDetail> registerVehicle(String platenumber, String vehicletype) async {
    CheckAndDetail cks = await AppAPI.RegisterVehicle(platenumber, vehicletype);
    return cks; 
  }

  static Future<void> logout() async {
    LocalStorage.deleteToken();
    LocalStorage.deleteUser();
  }
}
